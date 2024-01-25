import os
import json
import yaml
# 指定源文件夹路径
# 加载 YAML 配置文件
with open(os.path.join('par', 'promptcreate.yaml'), 'r') as file:
    promptname = yaml.safe_load(file)

# 从配置中获取路径
base_dir = promptname['PromptCreate'].replace('\\', '/')


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

            # Check if corresponding files exist in target
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

    # Check for unmatched files
    if unmatched_files:
        print("Unmatched files found:", unmatched_files)
        return False

    # Write to JSON file
    with open(os.path.join(base_dir, output_file), 'w') as json_file:
        for entry in data:
            json_file.write(json.dumps(entry) + "\n")

    return True

output_file = 'prompt.json'  # Output JSON file name

result = check_and_generate_json(base_dir, output_file)
if result:
    print("JSON file generated successfully.")
else:
    print("Failed to generate JSON file due to unmatched files.")
