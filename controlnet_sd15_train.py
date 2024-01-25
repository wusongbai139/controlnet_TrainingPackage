from share import *
import os
import yaml  
import random

from tqdm import tqdm  # 進度條
from pytorch_lightning.callbacks import ProgressBarBase # 進度條

# 获取当前脚本文件的绝对路径
current_script_path = os.path.dirname(os.path.abspath(__file__))
# 构建到 'createcon.yaml' 文件的路径
config_file_path = os.path.join(current_script_path,  'par', 'controlnet_train.yaml')
with open(config_file_path, 'r', encoding='utf-8') as f:
    training_parameters = yaml.safe_load(f)

# 设置cuda环境变量
# os.environ["PATH"] += os.pathsep + "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1\\bin"
# os.environ["PATH"] += os.pathsep + "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v12.1\\lib"

import pytorch_lightning as pl
from torch.utils.data import DataLoader
from dataset_img import MyDataset
from cldm.logger import ImageLogger
from cldm.model import create_model, load_state_dict

from transformers import CLIPTokenizer, CLIPTextModel
from pytorch_lightning.callbacks import ModelCheckpoint, Callback # Callback 保存其他格式

# 训练日志
from pytorch_lightning.loggers import TensorBoardLogger

# 训练中断自动保存模型
from pytorch_lightning import Trainer, LightningModule

import torch
from torch.utils.data import Sampler # 对训练集图片多次采样
# 添加学习率调度器和优化器
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR, CosineAnnealingWarmRestarts
from torch.optim import Adam, AdamW
from torch.optim.lr_scheduler import LambdaLR # 常量预热调度器
from torch.utils.data import Dataset
from torch import nn  # Lion
from lion_pytorch import Lion # Lion
from prodigyopt import Prodigy # Prodigy
import safetensors.torch
from datetime import datetime  # 时间戳

# 用您保存文件的本地路径替换下面的路径
local_model_path = './clip-vit-large-patch14' # training_parameters['local_model_path']
tokenizer = CLIPTokenizer.from_pretrained(local_model_path)  # local_model_path
model = CLIPTextModel.from_pretrained(local_model_path)

# 设置 TensorBoardLogger
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # 设置时间
custom_version_name = f"{current_time}"
tensorboard_logger = TensorBoardLogger(
    training_parameters["log_dir"],  # 日志文件夹
    name=training_parameters['log_name'], # 日志名
    version=custom_version_name +'-'+ training_parameters['log_name'] # 文件名
    )
logger_freq = training_parameters['logger_freq']  # 日志记录频率

resume_path = training_parameters['pretrained_model_path']  # 预训练模型位置
batch_size = training_parameters['batch_size'] 
learning_rate = 1e-5 

sd_locked = training_parameters['sd_locked']  
only_mid_control = training_parameters['only_mid_control']  

# file_extension = training_parameters.get('format') # 保存不同格式
modelname = training_parameters['ModelName']  
checkpoint_callback = ModelCheckpoint(
    save_top_k=-1, # 保存每一个模型
    every_n_epochs=training_parameters['every_n_epochs'], # 每多少epoch保存一个模型
    dirpath=training_parameters['model_dir'],
    filename=modelname + '-{epoch:02d}',
    # save_last=True 保存最后的模型（当训练被中断时，可以得到最后的模型，但是正常训练完之后，会多出一个新模型）
)

# First use cpu to load models. Pytorch Lightning will automatically move it to GPUs.
model = create_model('./models/cldm_v15.yaml').cpu()

model.load_state_dict(load_state_dict(resume_path, location='cpu'), strict=False)
model.learning_rate = learning_rate # 学习率不起作用
model.sd_locked = training_parameters['sd_locked'] # sd_locked
model.only_mid_control = training_parameters['only_mid_control']  # only_mid_control

class RepeatSampler(Sampler):  # 每张图片训练次数
    def __init__(self, data_source, times, shuffle=False):
        self.data_source = data_source
        self.times = times
        self.shuffle = shuffle

    def __iter__(self):
        indices = list(range(len(self.data_source))) * self.times
        if self.shuffle:
            random.shuffle(indices)
        return iter(indices)

    def __len__(self):
        return len(self.data_source) * self.times

# 这里使用从配置文件中读取的实际路径
source_dir = training_parameters['Datadir'] + '\\source'
target_dir = training_parameters['Datadir'] + '\\target'
json_path = training_parameters['Datadir'] + '\\prompt.json'

dataset = MyDataset()
data_dir = training_parameters['Datadir']

train_times = training_parameters['train_times']
sample_shuffle = training_parameters.get('sampleshuffle', False)
# 根据train_times的值设置DataLoader的shuffle参数
shuffle = True if train_times == 1 else False
# 创建RepeatSampler实例时传入sample_shuffle参数
repeat_sampler = RepeatSampler(dataset, times=train_times, shuffle=sample_shuffle)

dataloader = DataLoader(dataset, 
                        num_workers=int(training_parameters['num_workers']), # 0到2。提升训练时间
                        batch_size=batch_size, 
                        sampler=repeat_sampler if train_times > 1 else None,  # 当train_times>1时使用自定义sampler
                        shuffle=shuffle  # 使用动态设置的shuffle参数
                        )
logger = ImageLogger(batch_frequency=logger_freq)

trainer = pl.Trainer(
    gpus=1, 
    precision=training_parameters['precision'], # 32(全精度)、16（fp16）、bf16 
    callbacks=[logger,checkpoint_callback],
    max_epochs=training_parameters['max_epochs'], # 最大训练轮数
    accumulate_grad_batches=training_parameters['accumulate_grad_batches'], # 梯度累加,减少显存使用
    logger=tensorboard_logger,  # 使用 TensorBoardLogger
    )

if training_parameters['scheduler'] == "constant_warmup":
    num_warmup_steps = training_parameters['num_warmup_steps']  # 定义预热期的步数（常量预热）
    def warmup_constant(d_current_step):   # 定义 lambda 函数
        if d_current_step < num_warmup_steps:
            return float(d_current_step) / float(max(1, num_warmup_steps))
        return 1.0
else:
    pass

class MyModel(LightningModule):

    def configure_optimizers(self):
        general_lr = training_parameters['general_lr']  # 总体学习率
        unet_lr = training_parameters['unet_lr']     # unet 部分的学习率
        text_encoder_lr = training_parameters['text_encoder_lr']  # text_encoder 部分的学习率

        general_wd = training_parameters['general_wd']
        unet_wd = training_parameters['unet_wd']
        text_encoder_wd = training_parameters['text_encoder_wd']
        # 优化器
        if training_parameters['optimizer'] == 'AdamW':
            optimizer_general = AdamW(self.general_parameters, lr=general_lr, weight_decay = general_wd)
            optimizer_unet = AdamW(self.unet_parameters, lr=unet_lr, weight_decay = unet_wd)
            optimizer_text_encoder = AdamW(self.text_encoder_parameters, lr=text_encoder_lr, weight_decay = text_encoder_wd)
        elif training_parameters['optimizer'] == 'Adam':
            optimizer_general = Adam(self.general_parameters, lr=general_lr, weight_decay = general_wd)
            optimizer_unet = Adam(self.unet_parameters, lr=unet_lr, weight_decay = unet_wd)
            optimizer_text_encoder = Adam(self.text_encoder_parameters, lr=text_encoder_lr, weight_decay = text_encoder_wd)
        elif training_parameters['optimizer'] == 'Lion':
            optimizer_general = Lion(self.general_parameters, lr=general_lr, weight_decay = general_wd)
            optimizer_unet = Lion(self.unet_parameters, lr=unet_lr, weight_decay = unet_wd)
            optimizer_text_encoder = Lion(self.text_encoder_parameters, lr=text_encoder_lr, weight_decay = text_encoder_wd)
        elif training_parameters['optimizer'] == 'Prodigy':
            optimizer_general = Prodigy(self.general_parameters, 
                                        lr = training_parameters['general_lr'], 
                                        weight_decay = training_parameters['weight_decay'],
                                        d_coef = training_parameters['d_coef'],
                                        safeguard_warmup = training_parameters['safeguard_warmup']
                                        )   

        # 根据 scheduler_type 选择不同的调度器
        if training_parameters['scheduler_type'] == "CosineAnnealingWarmRestarts":
            scheduler_general = CosineAnnealingWarmRestarts(optimizer_general, training_parameters['T_0'])
            scheduler_unet = CosineAnnealingWarmRestarts(optimizer_unet, training_parameters['T_0'])
            scheduler_text_encoder = CosineAnnealingWarmRestarts(optimizer_text_encoder, training_parameters['T_0'])
        elif training_parameters['scheduler_type']  == "constant_warmup":
            scheduler_general = LambdaLR(optimizer_general, lr_lambda=warmup_constant)
            scheduler_unet = LambdaLR(optimizer_unet, lr_lambda=warmup_constant)
            scheduler_text_encoder = LambdaLR(optimizer_text_encoder, lr_lambda=warmup_constant)
        elif training_parameters['scheduler_type'] == "CosineAnnealingLR":
            scheduler_general = CosineAnnealingLR(optimizer_general, training_parameters['T_max'])
            scheduler_unet = CosineAnnealingLR(optimizer_unet, T_max=2)
            scheduler_text_encoder = CosineAnnealingLR(optimizer_text_encoder, training_parameters['T_max'])
        
        # 返回所有优化器和调度器
        return [optimizer_general, optimizer_unet, optimizer_text_encoder], [scheduler_general,scheduler_unet,scheduler_text_encoder]



# Train!
trainer.fit(model, dataloader)