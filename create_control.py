import os
import torch
import yaml
from share import *
from cldm.model import create_model

# 加载 YAML 配置文件
with open(os.path.join('par', 'createcon.yaml'), 'r') as file:
    createcon = yaml.safe_load(file)

# 从配置中获取路径
input_path = createcon['input_model_path'].replace('\\', '/')
output_path = createcon['combinedOutputPath'].replace('\\', '/')

# 检查输入模型是否存在...
assert os.path.exists(input_path), 'Input model does not exist.'
assert not os.path.exists(output_path), 'Output filename already exists.'
assert os.path.exists(os.path.dirname(output_path)), 'Output path is not valid.'

def get_node_name(name, parent_name):
    if len(name) <= len(parent_name):
        return False, ''
    p = name[:len(parent_name)]
    if p != parent_name:
        return False, ''
    return True, name[len(parent_name):]

# 创建模型，确保模型配置文件的路径是相对于脚本运行的当前目录的

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