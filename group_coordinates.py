import os
import json

# 文件夹路径
folder_path = r"E:\CBCTandannotation\myannotation\p1"

# 初始化存储组的字典
groups = {}

# 获取文件夹中的所有JSON文件
files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

# 遍历每一个文件
for file_name in files:
    # 分割文件名
    base_name = os.path.splitext(file_name)[0]
    file_type, position = base_name.split('_')

    # 读取JSON文件内容
    with open(os.path.join(folder_path, file_name), 'r') as file:
        data = json.load(file)
        points = data['markups'][0]['controlPoints']

    # 初始化对应位置的组
    group_key = f'g{position}'
    if group_key not in groups:
        groups[group_key] = []

    # 添加点坐标信息到对应的组
    for point in points:
        groups[group_key].append(point['position'])

# 打印结果
for group, points in groups.items():
    print(f"{group}: {points}")

# 示例输出到文件，可以根据需要修改
output_file = os.path.join(folder_path, 'output_groups.json')
with open(output_file, 'w') as file:
    json.dump(groups, file, indent=4)

print("所有位置坐标已整理并存储。")
