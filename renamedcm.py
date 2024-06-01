################################################################################
#                  将dcm文件的名字排序部分都补全为5位数
#                  3D SLICER先读取1，11，而不是读取1.再读取2
#
################################################################################

import os

# 文件夹路径
folder_path = r"E:\CBCTandannotation\img\P2"

# 获取文件夹中的所有文件
files = os.listdir(folder_path)

# 遍历每一个文件
for file_name in files:
    # 分割文件名和扩展名
    base_name, ext = os.path.splitext(file_name)

    # 查找下划线的位置
    underscore_index = base_name.find('_')

    if underscore_index != -1:
        # 提取文件名和编号
        name_part = base_name[:underscore_index]
        number_part = base_name[underscore_index + 1:]

        # 将编号部分变为5位数，前面补0
        new_number_part = number_part.zfill(5)

        # 组合新的文件名
        new_file_name = f"{name_part}_{new_number_part}{ext}"

        # 原文件的完整路径
        old_file_path = os.path.join(folder_path, file_name)

        # 新文件的完整路径
        new_file_path = os.path.join(folder_path, new_file_name)

        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{file_name}' to '{new_file_name}'")

print("所有文件已重命名。")
