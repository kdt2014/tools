import os

# 指定文件夹路径
folder_path = "/media/kdt/mydata/数据集/MICCAI-Tooth-Segmentation/ToothFair/ToothFairy2_Dataset/Dataset112_ToothFairy2/images"

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 检查文件名中是否包含"Fairy"
    if "Fairy" in filename:
        # 构建新的文件名
        new_filename = filename.replace("Fairy", "")

        # 构建完整的旧文件路径和新文件路径
        old_file_path = os.path.join(folder_path, filename)
        new_file_path = os.path.join(folder_path, new_filename)

        # 重命名文件
        os.rename(old_file_path, new_file_path)

        print(f"重命名文件: {filename} -> {new_filename}")

print("文件重命名完成.")