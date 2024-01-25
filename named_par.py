source_folder = r'' # 图片目录。只需改路径，不要碰那个字母r。

# 勿动下方代码 ——————————————————————————————————————————————————————————
import os

files = os.listdir(source_folder)
for index, file_name in enumerate(files):
    file_name_body, file_extension = os.path.splitext(file_name)
    if file_extension.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
        new_name = f"{index + 1}{file_extension}"
        old_file = os.path.join(source_folder, file_name)
        new_file = os.path.join(source_folder, new_name)
        counter = 1
        while os.path.exists(new_file):
            new_name = f"{index + 1}_{counter}{file_extension}"
            new_file = os.path.join(source_folder, new_name)
            counter += 1
        os.rename(old_file, new_file)
        print(f"重命名文件：{file_name} -> {new_name}")
print("批量重命名完成。")