import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

# 读取Nii文件
nii_file = 'E:\\CBCTandannotation\\myannotation\\p1\\DCBCTImageSet.nii'
image = sitk.ReadImage(nii_file)
image_array = sitk.GetArrayFromImage(image)

# 提供的三个点
point1 = np.array([-15.034228302882678, -30.2137484248086, -22.84246285093691])
point2 = np.array([-14.089678248570625, -28.263273122123387, -14.914172739473898])
point3 = np.array([-16.688125349924306, -25.396670932765616, -36.30480886717598])


# 将物理坐标转换为图像坐标
def physical_to_index(physical_point, image):
    return np.array(image.TransformPhysicalPointToIndex(physical_point))


index1 = physical_to_index(point1, image)
index2 = physical_to_index(point2, image)
index3 = physical_to_index(point3, image)

print("Index 1:", index1)
print("Index 2:", index2)
print("Index 3:", index3)

# 计算平面法向量
vec1 = index2 - index1
vec2 = index3 - index1
normal = np.cross(vec1, vec2)
normal = normal / np.linalg.norm(normal)


# 定义提取平面的函数
def extract_plane(image_array, normal, point, size=(512, 512)):
    d = -np.dot(normal, point)

    # 创建平面上的网格
    xx, yy = np.meshgrid(range(size[0]), range(size[1]), indexing='ij')
    zz = (-normal[0] * xx - normal[1] * yy - d) / normal[2]

    plane_points = np.vstack((xx.ravel(), yy.ravel(), zz.ravel())).T

    # 将平面点映射到图像坐标
    plane_points = np.round(plane_points).astype(int)

    print("Plane points shape:", plane_points.shape)
    print("Plane points min:", np.min(plane_points, axis=0))
    print("Plane points max:", np.max(plane_points, axis=0))

    # 只保留在图像范围内的点
    valid_mask = (
            (plane_points[:, 0] >= 0) & (plane_points[:, 0] < image_array.shape[2]) &
            (plane_points[:, 1] >= 0) & (plane_points[:, 1] < image_array.shape[1]) &
            (plane_points[:, 2] >= 0) & (plane_points[:, 2] < image_array.shape[0])
    )
    plane_points = plane_points[valid_mask]

    # 使用双线性插值提取平面上的像素值
    plane_image = np.zeros(size)
    for point in plane_points:
        x, y, z = point
        plane_image[x, y] = image_array[z, y, x]

    return plane_image


# 提取平面并显示
plane_image = extract_plane(image_array, normal, index1)
plt.imshow(plane_image, cmap='gray')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Extracted Plane')
plt.colorbar()
plt.show()