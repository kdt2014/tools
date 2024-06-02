import json

# 读取JSON数据
with open('output_groups.json', 'r') as f:
    data = json.load(f)

# 遍历每组数据
for group_name, group_data in data.items():
    # 赋值前三个点的坐标给p1, p2, p3
    # p1 = group_data[0]
    # p2 = group_data[1]
    # p3 = group_data[2]
    p1, p2, p3 = group_data[:3]

    # 打印当前组的点坐标
    print(f"Group: {group_name}")
    print(f"p1: {p1}")
    print(f"p2: {p2}")
    print(f"p3: {p3}")
    print()