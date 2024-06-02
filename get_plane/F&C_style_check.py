###########################################################################################
#               这个实验结果表明：
#               相同的物理坐标转换成像素坐标后，如果数据存储风格不同（F和C风格）
#               那么对应的像素值也不同
###########################################################################################

import numpy as np
import vtk
from vtk.util import numpy_support

# 创建 vtkNIFTIImageReader 实例
reader = vtk.vtkNIFTIImageReader()

# 设置要读取的 NIfTI 文件的路径
nii_file = r'E:\CBCTandannotation\myannotation\p1\DCBCTImageSet.nii'
reader.SetFileName(nii_file)

# 更新读取器以读取文件
reader.Update()

# 获取读取的图像数据
image_data = reader.GetOutput()

# 获取图像数据中的点数据
point_data = image_data.GetPointData().GetScalars()

# 将 vtkDataArray 转换为 NumPy 数组
array = numpy_support.vtk_to_numpy(point_data)

# 获取图像数据的维度
dimensions = image_data.GetDimensions()
print("vtkImg shape:", dimensions)

# 重塑为不同排序方式的数组
array_f = array.reshape(dimensions, order='F')
array_c = array.reshape(dimensions, order='C')

# 假设 p1 是物理坐标
p1 = np.array([-9.69734348599805, -33.08485126446559, -22.749778244595152])

# 函数：将物理坐标转换为像素坐标
def physical_to_pixel(image_data, physical_point):
    # 获取图像的方向矩阵和原点
    direction_matrix = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            direction_matrix[i, j] = image_data.GetDirectionMatrix().GetElement(i, j)
    origin = np.array(image_data.GetOrigin())
    spacing = np.array(image_data.GetSpacing())

    # 计算相对坐标
    relative_point = physical_point - origin

    # 将物理坐标转换为像素坐标
    pixel_point = np.linalg.inv(direction_matrix).dot(relative_point / spacing)
    return np.round(pixel_point).astype(int)

# 获取像素坐标
pixel_coords = physical_to_pixel(image_data, p1)

print("Pixel coordinates:", pixel_coords)

# 在不同存储顺序下获取该像素坐标的值
value_f = array_f[tuple(pixel_coords)]
value_c = array_c[tuple(pixel_coords)]

print("Value at pixel coordinates (F-order):", value_f)
print("Value at pixel coordinates (C-order):", value_c)

# 验证不同存储顺序下的值是否相同
print("Values match:", value_f == value_c)


