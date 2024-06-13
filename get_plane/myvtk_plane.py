import vtk
import numpy as np
from PIL import Image
from vtkmodules.util import numpy_support

# Define the coordinates of three points
p1 = [-9.69734348599805, -33.08485126446559, -22.749778244595152]
p2 = [-8.751273757037172, -31.376424855451674, -14.821241587740474]
p3 = [-11.288699239305164, -28.993066868387096, -35.73076265650188]

# Compute the normal vector of the plane
v1 = np.array(p2) - np.array(p1)
v2 = np.array(p3) - np.array(p1)
normal = np.cross(v1, v2)
normal = normal / np.linalg.norm(normal)  # Normalize

print("Normal Vector: ", normal)

# Read the NIfTI file
nii_file = r'E:\CBCTandannotation\myannotation\p1\DCBCTImageSet.nii'
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(nii_file)
reader.Update()

# Get image data
image_data = reader.GetOutput()
image_data.SetOrigin(49.5, 49.5, -49.41)
# origin1 = image_data.GetOrigin()
# print("origin1:", origin1)

# Get the numpy array from vtkImageData
point_data = image_data.GetPointData().GetScalars()   # point_data 是1维数组

# 打印点数据
# print(point_data)
array = numpy_support.vtk_to_numpy(point_data)
# dimensions = image_data.GetDimensions()
# print("vtkImg shape:", dimensions)
array = array.reshape(image_data.GetDimensions(), order='F')
print("Array shape:", array.shape)

# ###########################################################################
# 存储风格会影响空间中点的位置
#这部分是测试验证这个结论的代码
# 重塑为不同排序方式的数组并打印部分内容
############################################################################
# array_f = array.reshape(dimensions, order='F')
# array_c = array.reshape(dimensions, order='C')
#
# print("Array shape (F-order):", array_f.shape)
# print("Array shape (C-order):", array_c.shape)
#
# # 打印一些不同位置的元素以比较不同排序方式的结果
# print("\nSample elements (F-order):")
# print("array_f[0, 0, 0]:", array_f[0, 0, 0])
# print("array_f[-329, -459, 148]:", array_f[-329, -459, 148])
# print("array_f[0, 1, 0]:", array_f[0, 1, 0])
# print("array_f[1, 0, 0]:", array_f[1, 0, 0])
# print("array_f[550, 550, 549]:", array_f[550, 550, 549])
#
# print("\nSample elements (C-order):")
# print("array_c[0, 0, 0]:", array_c[0, 0, 0])
# print("array_c[-329, -459, 148]:", array_c[-329, -459, 148])
# print("array_c[0, 1, 0]:", array_c[0, 1, 0])
# print("array_c[1, 0, 0]:", array_c[1, 0, 0])
# print("array_c[550, 550, 549]:", array_c[550, 550, 549])
#
# # 验证不同排序方式的内容是否相同
# print("\nF-order == C-order:", np.array_equal(array_f, array_c))
#
# #######################################################################


# Define the reorientation affine transformation matrix
# reorient_affine = np.array([
#     [0, 0, 1, 0],  # transpose (2, 1, 0)
#     [0, 1, 0, 0],  # keep Y axis unchanged
#     [1, 0, 0, 0],  # swap X and Z axes
#     [0, 0, 0, 1]   # Homogeneous coordinate remains unchanged
# ])

reorient_affine = np.array([
    [1, 0, 0, 0],  # transpose (2, 1, 0)
    [0, 1, 0, 0],  # keep Y axis unchanged
    [0, 0, 1, 0],  # swap X and Z axes
    [0, 0, 0, 1]   # Homogeneous coordinate remains unchanged
])

# Apply affine transformation
transform = vtk.vtkTransform()
transform.SetMatrix(reorient_affine.flatten())

reslice = vtk.vtkImageReslice()  # Creating an Instance
reslice.SetInputData(image_data)  # Setting Input Data

reslice.SetResliceTransform(transform)
reslice.SetInterpolationModeToLinear()   # SetInterpolationModeToNearestNeighbor() and SetInterpolationModeToCubic()
reslice.SetOutputExtent(image_data.GetExtent())
reslice.Update()

#################################################################

# Get the rotated output
rotated_image_data = reslice.GetOutput()

# Check data range
extent = rotated_image_data.GetExtent()
spacing = rotated_image_data.GetSpacing()
origin = rotated_image_data.GetOrigin()

print("Data Extent: ", extent)
print("Data Spacing: ", spacing)
print("Data Origin: ", origin)
print("Origin[0]: ", origin[0])
print("Origin[1]: ", origin[1])
print("Origin[2]: ", origin[2])

# Set the plane's origin to the data center
center = [
    origin[0] + spacing[0] * 0.5 * (extent[0] + extent[1]),
    origin[1] + spacing[1] * 0.5 * (extent[2] + extent[3]),
    origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])
]
print("Plane Origin (Center): ", center)

# center = image_data.GetOrigin()

# Create the reslice object for cutting the section
cut_reslice = vtk.vtkImageReslice()
cut_reslice.SetInputData(rotated_image_data)
cut_reslice.SetOutputDimensionality(2)

# Set the reslice parameters
cut_reslice.SetResliceAxesOrigin(center)
cut_reslice.SetResliceAxesDirectionCosines(
    normal[0], normal[1], normal[2],
    -normal[1], normal[0], 0,
    0, 0, 1)
cut_reslice.SetInterpolationModeToLinear()
cut_reslice.Update()

# Get the output from reslice
cut_reslice_output = cut_reslice.GetOutput()
cut_reslice_extent = cut_reslice_output.GetExtent()

# Convert the reslice output to a NumPy array
cut_reslice_array = numpy_support.vtk_to_numpy(cut_reslice_output.GetPointData().GetScalars())
cut_reslice_array = cut_reslice_array.reshape((cut_reslice_extent[3] - cut_reslice_extent[2] + 1,
                                               cut_reslice_extent[1] - cut_reslice_extent[0] + 1))

# Rotate the image by 90 degrees clockwise
# rotated_image_array = np.rot90(cut_reslice_array, k=-1)

# Map the CT values to the 0-255 range
# min_value = np.min(rotated_image_array)
# max_value = np.max(rotated_image_array)
# scaled_array = np.uint8(255 * (rotated_image_array - min_value) / (max_value - min_value))

min_value = np.min(cut_reslice_array)
max_value = np.max(cut_reslice_array)
scaled_array = np.uint8(255 * (cut_reslice_array - min_value) / (max_value - min_value))

# Save the grayscale image using PIL
image = Image.fromarray(scaled_array)
image.save("cut_section1.png")

print("Image saved as 'cut_section1.png'")









