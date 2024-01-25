import json
import cv2
import numpy as np
from torch.utils.data import Dataset
import yaml

# 加载 YAML 配置文件
with open('./par/controlnet_train.yaml', 'r', encoding='utf-8') as f:
    training_parameters = yaml.safe_load(f)

# 创建 MyDataset 实例
Dataprompt = training_parameters['Datadir'] + '\\prompt.json'
Datadir = training_parameters['Datadir']
if not Datadir.endswith(('/', '\\')):
    Datadir += '/'

class MyDataset(Dataset):  # 定义 MyDataset 类
    def __init__(self):
        self.data = []
        with open(Dataprompt, 'rt') as f:
            for line in f:
                self.data.append(json.loads(line))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]

        source_filename = item['source']
        target_filename = item['target']
        prompt = item['prompt']

        source = cv2.imread(Datadir + source_filename)
        target = cv2.imread(Datadir + target_filename)

        # Do not forget that OpenCV read images in BGR order.
        source = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)

        # Normalize source images to [0, 1].
        source = source.astype(np.float32) / 255.0

        # Normalize target images to [-1, 1].
        target = (target.astype(np.float32) / 127.5) - 1.0

        return dict(jpg=target, txt=prompt, hint=source)