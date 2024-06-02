import vtk
import numpy as np
from PIL import Image
from vtkmodules.util import numpy_support
import json
import os

# 读取输出组数据
output_groups_file = r'E:\\CBCTandannotation\\myannotation\\p1\\output_groups.json'
with open(output_groups_file, 'r') as file:
    output_groups = json.load(file)

# 读取NIfTI文件
nii_file = r'E:\CBCTandannotation\myannotation\p2\DCBCTImageSet.nii'
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(nii_file)
reader.Update()

# 获取图像数据
image_data = reader.GetOutput()

# 将vtkImageData转换为NumPy数组
point_data = image_data.GetPointData().GetScalars()
array = numpy_support.vtk_to_numpy(point_data)
array = array.reshape(image_data.GetDimensions(), order='F')

# 定义重新取向的仿射变换矩阵
reorient_affine = np.array([
    [0, 0, 1, 0],  # 转置 (2, 1, 0)
    [0, 1, 0, 0],  # 保持Y轴不变
    [1, 0, 0, 0],  # 交换X和Z轴
    [0, 0, 0, 1]   # 齐次坐标保持不变
])

# 应用仿射变换
transform = vtk.vtkTransform()
transform.SetMatrix(reorient_affine.flatten())

reslice = vtk.vtkImageReslice()
reslice.SetInputData(image_data)
reslice.SetResliceTransform(transform)
reslice.SetInterpolationModeToLinear()
reslice.SetOutputExtent(image_data.GetExtent())
reslice.Update()

# 获取旋转后的输出
rotated_image_data = reslice.GetOutput()

# 获取数据范围
extent = rotated_image_data.GetExtent()
spacing = rotated_image_data.GetSpacing()
origin = rotated_image_data.GetOrigin()

# 检查并创建plane_slicer文件夹
output_dir = os.path.join(os.path.dirname(nii_file), 'plane_slicer')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 遍历output_groups中的每一组
for group, points in output_groups.items():
    if len(points) < 3:
        print(f"Group {group} does not have enough points for plane definition.")
        continue

    # 提取前三个点的坐标
    p1, p2, p3 = points[:3]

    # 计算平面的法向量
    v1 = np.array(p2) - np.array(p1)
    v2 = np.array(p3) - np.array(p1)
    normal = np.cross(v1, v2)
    normal = normal / np.linalg.norm(normal)  # 归一化

    # 设置平面的原点为数据中心
    center = [
        origin[0] + spacing[0] * 0.5 * (extent[0] + extent[1]),
        origin[1] + spacing[1] * 0.5 * (extent[2] + extent[3]),
        origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])
    ]

    # 创建reslice对象以截取平面
    cut_reslice = vtk.vtkImageReslice()
    cut_reslice.SetInputData(rotated_image_data)
    cut_reslice.SetOutputDimensionality(2)

    # 设置reslice参数
    cut_reslice.SetResliceAxesOrigin(center)
    cut_reslice.SetResliceAxesDirectionCosines(
        normal[0], normal[1], normal[2],
        -normal[1], normal[0], 0,
        0, 0, 1)
    cut_reslice.SetInterpolationModeToLinear()
    cut_reslice.Update()

    # 获取reslice输出
    cut_reslice_output = cut_reslice.GetOutput()
    cut_reslice_extent = cut_reslice_output.GetExtent()

    # 将reslice输出转换为NumPy数组
    cut_reslice_array = numpy_support.vtk_to_numpy(cut_reslice_output.GetPointData().GetScalars())
    cut_reslice_array = cut_reslice_array.reshape((cut_reslice_extent[3] - cut_reslice_extent[2] + 1,
                                                   cut_reslice_extent[1] - cut_reslice_extent[0] + 1))

    # 旋转图像90度顺时针
    rotated_image_array = np.rot90(cut_reslice_array, k=-1)

    # 将CT值映射到0-255范围
    min_value = np.min(rotated_image_array)
    max_value = np.max(rotated_image_array)
    scaled_array = np.uint8(255 * (rotated_image_array - min_value) / (max_value - min_value))

    # 使用PIL保存灰度图像
    image = Image.fromarray(scaled_array)
    image_name = group.replace('.mrk', '') + '.png'  # 去掉.mrk后缀并添加.png
    image_path = os.path.join(output_dir, image_name)
    image.save(image_path)

    print(f"Image saved as '{image_path}'")
