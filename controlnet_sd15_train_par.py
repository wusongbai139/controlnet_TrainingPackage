pretrained_model_path = r'H:\AIGC\lora\controlnet.ckpt' # 预训练模型位置。只需改路径，不要碰那个字母r。
ModelName = 'controlnet_sd15' # 模型名
model_dir = r'H:\AIGC\lora\controlnet' # 模型保存路径。只需改路径，不要碰那个字母r。
Datadir = r'H:\AIGC\lora\1\fill50k' # 训练集路径。只需改路径，不要碰那个字母r。
train_times = 1 # 每张图片训练次数
num_workers = 0 # 多进程，降低训练时间。建议是0就行，不要改。
precision = 'bf16' # 训练精度。可选：'fp16'、'32'
max_epochs = 20 # 最大训练轮数
every_n_epochs = 4  # 每多少epoch保存一个模型
batch_size = 1 # 每步训练几张
accumulate_grad_batches = 4 # 梯度累加,减少显存使用。
randomimage = True # 随机图片顺序True或False都可以

sd_locked = True # 选择False时将训练Decoder层，默认True以避免数据集质量低影响模型性能
only_mid_control = False # 选择True训练的架构将只在中间层，而不是整体，速度较快，资源占用较低，效果未必好

scheduler = 'constant_warmup' # 调度器。可选：'constant_warmup'(常量预热)、'CosineAnnealingLR'（余弦）、'CosineAnnealingWarmRestarts'(余弦重启)
T_0 = 2 # 重启次数。搭配'CosineAnnealingWarmRestarts'使用。训练周期中的重启次数。
num_warmup_steps = 10 # 定义预热期的步数，搭配'constant_warmup'使用 。
T_max = 20 # 学习率最高轮数。搭配'CosineAnnealingLR'使用。

general_lr = 0.00005 # 通用学习率
general_wd = 0 # 通用权重衰减
unet_lr = 0.00005 # Unet学习率
unet_wd = 0.000005 # Unet权重衰减
text_encoder_lr = 0.00005 # 文本编码学习率
text_encoder_wd = 0 # 文本编码权重衰减

optimizer = 'Prodigy' # 优化器。可选参数：'AdamW'、'Adam'、'Lion'、'Prodigy'
d_coef = 1 # 学习率估计系数。搭配Prodigy使用
safeguard_warmup = False # 搭配Prodigy使用，在调度器是constant_warmup时可以选择True。其他情况填False。

log_dir = r'H:\AIGC\log' # 日志文件夹
log_name = '1111' # 日志名
logger_freq = 300 # 日志记录频率

# ———————————————————————————————————————————————————————————————————————————— #

from share import *
import os
from pathlib import Path 
import random
from tqdm import tqdm  # 進度條
from pytorch_lightning.callbacks import ProgressBarBase # 進度條

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
local_model_path = './clip-vit-large-patch14' 
tokenizer = CLIPTokenizer.from_pretrained(local_model_path)  
model = CLIPTextModel.from_pretrained(local_model_path)

# 设置 TensorBoardLogger
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # 设置时间
custom_version_name = f"{current_time}"
tensorboard_logger = TensorBoardLogger(
    log_dir,  # 日志文件夹
    name = log_name, # 日志名
    version=custom_version_name +'-'+ log_name # 文件名
    )

learning_rate = 1e-5 
checkpoint_callback = ModelCheckpoint(
    save_top_k=-1, # 保存每一个模型
    every_n_epochs=every_n_epochs, # 每多少epoch保存一个模型
    dirpath=model_dir,
    filename=ModelName + '-{epoch:02d}',
    # save_last=True 保存最后的模型（当训练被中断时，可以得到最后的模型，但是正常训练完之后，会多出一个新模型）
)

model = create_model('./models/cldm_v15.yaml').cpu()

model.load_state_dict(load_state_dict(pretrained_model_path, location='cpu'), strict=False)
model.learning_rate = learning_rate # 学习率不起作用
model.sd_locked = sd_locked 
model.only_mid_control = only_mid_control

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
source_dir = Datadir + '\\source'
target_dir = Datadir + '\\target'
json_path = Datadir + '\\prompt.json'
data_dir = Datadir

dataset = MyDataset()

sample_shuffle = randomimage
# 根据train_times的值设置DataLoader的shuffle参数
shuffle = randomimage if train_times == 1 else False
# 创建RepeatSampler实例时传入sample_shuffle参数
repeat_sampler = RepeatSampler(dataset, times=train_times, shuffle=sample_shuffle)

dataloader = DataLoader(dataset, 
                        num_workers = num_workers, # 0到2。降低训练时间
                        batch_size=batch_size, 
                        sampler=repeat_sampler if train_times > 1 else None,  # 当train_times>1时使用自定义sampler
                        shuffle=shuffle  # 使用动态设置的shuffle参数
                        )
logger = ImageLogger(batch_frequency=logger_freq)

trainer = pl.Trainer(
    gpus=1, 
    precision=precision, # 32(全精度)、16（fp16）、bf16 
    callbacks=[logger,checkpoint_callback],
    max_epochs=max_epochs, # 最大训练轮数
    accumulate_grad_batches=accumulate_grad_batches, # 梯度累加,减少显存使用
    logger=tensorboard_logger,  # 使用 TensorBoardLogger
    )

if scheduler == "constant_warmup":
    num_warmup_steps = num_warmup_steps  # 定义预热期的步数（常量预热）
    def warmup_constant(d_current_step):   # 定义 lambda 函数
        if d_current_step < num_warmup_steps:
            return float(d_current_step) / float(max(1, num_warmup_steps))
        return 1.0
else:
    pass

class MyModel(LightningModule):

    def configure_optimizers(self):
        general_lr = general_lr  # 总体学习率
        unet_lr = unet_lr     # unet 部分的学习率
        text_encoder_lr = text_encoder_lr  # text_encoder 部分的学习率

        general_wd = general_wd
        unet_wd = unet_wd
        text_encoder_wd = text_encoder_wd
        # 优化器
        if optimizer == 'AdamW':
            optimizer_general = AdamW(self.general_parameters, lr=general_lr, weight_decay = general_wd)
            optimizer_unet = AdamW(self.unet_parameters, lr=unet_lr, weight_decay = unet_wd)
            optimizer_text_encoder = AdamW(self.text_encoder_parameters, lr=text_encoder_lr, weight_decay = text_encoder_wd)
        elif optimizer == 'Adam':
            optimizer_general = Adam(self.general_parameters, lr=general_lr, weight_decay = general_wd)
            optimizer_unet = Adam(self.unet_parameters, lr=unet_lr, weight_decay = unet_wd)
            optimizer_text_encoder = Adam(self.text_encoder_parameters, lr=text_encoder_lr, weight_decay = text_encoder_wd)
        elif optimizer == 'Lion':
            optimizer_general = Lion(self.general_parameters, lr=general_lr, weight_decay = general_wd)
            optimizer_unet = Lion(self.unet_parameters, lr=unet_lr, weight_decay = unet_wd)
            optimizer_text_encoder = Lion(self.text_encoder_parameters, lr=text_encoder_lr, weight_decay = text_encoder_wd)
        elif optimizer == 'Prodigy':
            optimizer_general = Prodigy(self.general_parameters, 
                                        lr = general_lr, 
                                        weight_decay = unet_lr,
                                        d_coef = d_coef,
                                        safeguard_warmup = safeguard_warmup
                                        )   

        # 根据 scheduler_type 选择不同的调度器
        if scheduler == "CosineAnnealingWarmRestarts":
            scheduler_general = CosineAnnealingWarmRestarts(optimizer_general, T_0)
            scheduler_unet = CosineAnnealingWarmRestarts(optimizer_unet, T_0)
            scheduler_text_encoder = CosineAnnealingWarmRestarts(optimizer_text_encoder, T_0)
        elif scheduler  == "constant_warmup":
            scheduler_general = LambdaLR(optimizer_general, lr_lambda=warmup_constant)
            scheduler_unet = LambdaLR(optimizer_unet, lr_lambda=warmup_constant)
            scheduler_text_encoder = LambdaLR(optimizer_text_encoder, lr_lambda=warmup_constant)
        elif scheduler == "CosineAnnealingLR":
            scheduler_general = CosineAnnealingLR(optimizer_general, T_max)
            scheduler_unet = CosineAnnealingLR(optimizer_unet, T_max)
            scheduler_text_encoder = CosineAnnealingLR(optimizer_text_encoder, T_max)
        
        # 返回所有优化器和调度器
        return [optimizer_general, optimizer_unet, optimizer_text_encoder], [scheduler_general,scheduler_unet,scheduler_text_encoder]

# Train!
trainer.fit(model, dataloader)