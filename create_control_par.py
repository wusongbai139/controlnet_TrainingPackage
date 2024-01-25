input_path = r'H:\AIGC\lora\1\v1-5-pruned-emaonly.ckpt' # 输入模型位置。只需改路径，不要碰那个字母r。
output_path = r'H:\AIGC\lora\controlnet.ckpt' # 输出模型位置。只需改路径，不要碰那个字母r，切记加上最后的“.ckpt”。

# ——————————————————————————————————————————————————————————————————————————

import os
import torch
from share import *
from cldm.model import create_model

assert os.path.exists(input_path), '输入模型不存在'
assert not os.path.exists(output_path), '输出文件名已经存在'
assert os.path.exists(os.path.dirname(output_path)), '输出路径不存在'

def get_node_name(name, parent_name):
    if len(name) <= len(parent_name):
        return False, ''
    p = name[:len(parent_name)]
    if p != parent_name:
        return False, ''
    return True, name[len(parent_name):]

config_path = os.path.join('models', 'cldm_v15.yaml')
model = create_model(config_path=config_path)

pretrained_weights = torch.load(input_path)
if 'state_dict' in pretrained_weights:
    pretrained_weights = pretrained_weights['state_dict']

scratch_dict = model.state_dict()
target_dict = {}
for k in scratch_dict.keys():
    is_control, name = get_node_name(k, 'control_')
    if is_control:
        copy_k = 'model.diffusion_' + name
    else:
        copy_k = k
    if copy_k in pretrained_weights:
        target_dict[k] = pretrained_weights[copy_k].clone()
    else:
        target_dict[k] = scratch_dict[k].clone()
        print(f'These weights are newly added: {k}')
model.load_state_dict(target_dict, strict=True)
torch.save(model.state_dict(), output_path)
print('Done.')