base_dir = r'' # 训练集根目录。只需改路径，不要碰那个字母r。

# 勿动下方代码 ——————————————————————————————————————————————————————————————————

import os
import json

def check_and_generate_json(base_dir, output_file):
    source_dir = os.path.join(base_dir, 'source')
    target_dir = os.path.join(base_dir, 'target')
    source_files = {f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))}
    target_files = {f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))}
    unmatched_files = []
    data = []
    for file_name in source_files:
        if file_name.endswith('.png') or file_name.endswith('.jpg'):
            base_name = os.path.splitext(file_name)[0]
            target_image_png = base_name + '.png'
            target_image_jpg = base_name + '.jpg'
            target_text = base_name + '.txt'
            if target_image_png in target_files and target_text in target_files:
                image_extension = '.png'
            elif target_image_jpg in target_files and target_text in target_files:
                image_extension = '.jpg'
            else:
                unmatched_files.append(base_name)
                continue
            with open(os.path.join(target_dir, target_text), 'r') as txt_file:
                prompt = txt_file.read().strip()
                data.append({
                    "source": f"source/{base_name}{image_extension}",
                    "target": f"target/{base_name}{image_extension}",
                    "prompt": prompt
                })
    if unmatched_files:
        print("Unmatched files found:", unmatched_files)
        return False
    with open(os.path.join(base_dir, output_file), 'w') as json_file:
        for entry in data:
            json_file.write(json.dumps(entry) + "\n")
    return True
output_file = 'prompt.json'
result = check_and_generate_json(base_dir, output_file)
if result:
    print("JSON file generated successfully.")
else:
    print("Failed to generate JSON file due to unmatched files.")