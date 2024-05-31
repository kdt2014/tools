import vtk
import numpy as np
from PIL import Image
from vtkmodules.util import numpy_support

# Define the coordinates of three points
p1 = [-15.034228302882678, -30.2137484248086, -22.84246285093691]
p2 = [-14.089678248570625, -28.263273122123387, -14.914172739473898]
p3 = [-16.688125349924306, -25.396670932765616, -36.30480886717598]

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

# Get the numpy array from vtkImageData
point_data = image_data.GetPointData().GetScalars()
array = numpy_support.vtk_to_numpy(point_data)
array = array.reshape(image_data.GetDimensions(), order='F')

# Define the reorientation affine transformation matrix
reorient_affine = np.array([
    [0, 0, 1, 0],  # transpose (2, 1, 0)
    [0, 1, 0, 0],  # keep Y axis unchanged
    [1, 0, 0, 0],  # swap X and Z axes
    [0, 0, 0, 1]   # Homogeneous coordinate remains unchanged
])

# Apply affine transformation
transform = vtk.vtkTransform()
transform.SetMatrix(reorient_affine.flatten())

reslice = vtk.vtkImageReslice()
reslice.SetInputData(image_data)
reslice.SetResliceTransform(transform)
reslice.SetInterpolationModeToLinear()
reslice.SetOutputExtent(image_data.GetExtent())
reslice.Update()

# Get the rotated output
rotated_image_data = reslice.GetOutput()

# Check data range
extent = rotated_image_data.GetExtent()
spacing = rotated_image_data.GetSpacing()
origin = rotated_image_data.GetOrigin()

print("Data Extent: ", extent)
print("Data Spacing: ", spacing)
print("Data Origin: ", origin)

# Set the plane's origin to the data center
center = [
    origin[0] + spacing[0] * 0.5 * (extent[0] + extent[1]),
    origin[1] + spacing[1] * 0.5 * (extent[2] + extent[3]),
    origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])
]
print("Plane Origin (Center): ", center)

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

# Map the CT values to the 0-255 range
min_value = np.min(cut_reslice_array)
max_value = np.max(cut_reslice_array)
scaled_array = np.uint8(255 * (cut_reslice_array - min_value) / (max_value - min_value))

# Save the grayscale image using PIL
image = Image.fromarray(scaled_array)
image.save("cut_section.png")

print("Image saved as 'cut_section.png'")

