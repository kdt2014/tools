import os

# 设置文件夹路径
folder_path = "E:\img\post-HA0089_20201028_112322_anonz"

# 获取文件夹中的所有文件
files = os.listdir(folder_path)

# 过滤出以"3DSlice"开头并以".dcm"结尾的文件
dcm_files = [file for file in files if file.startswith("3DSlice") and file.endswith(".dcm")]

# 对文件按照数字部分进行排序
dcm_files.sort(key=lambda x: int(x[7:-4]))

# 遍历文件并重命名
for i, file in enumerate(dcm_files, start=1):
    old_path = os.path.join(folder_path, file)
    new_name = f"p2_{i}.dcm"
    new_path = os.path.join(folder_path, new_name)
    os.rename(old_path, new_path)
    print(f"Renamed: {file} -> {new_name}")