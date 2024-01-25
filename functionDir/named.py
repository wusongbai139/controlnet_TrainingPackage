import os
import yaml
# 指定源文件夹路径
# 加载 YAML 配置文件
with open(os.path.join('par', 'imagename.yaml'), 'r', encoding='utf-8') as file:
    imagename = yaml.safe_load(file)

# 从配置中获取路径
source_folder = imagename['imageDir'].replace('\\', '/')

# 获取source文件夹内所有文件的列表
files = os.listdir(source_folder)

# 遍历文件列表
for index, file_name in enumerate(files):
    # 分割文件名和扩展名
    file_name_body, file_extension = os.path.splitext(file_name)
    # 确保它是一个图片文件
    if file_extension.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
        new_name = f"{index + 1}{file_extension}"
        old_file = os.path.join(source_folder, file_name)
        new_file = os.path.join(source_folder, new_name)
        
        # 如果目标文件名已存在，则添加一个后缀
        counter = 1
        while os.path.exists(new_file):
            new_name = f"{index + 1}_{counter}{file_extension}"
            new_file = os.path.join(source_folder, new_name)
            counter += 1

        # 重命名文件
        os.rename(old_file, new_file)
        print(f"重命名文件：{file_name} -> {new_name}")

print("批量重命名完成。")