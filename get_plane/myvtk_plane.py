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

# Check data range
image_data = reader.GetOutput()
extent = image_data.GetExtent()
spacing = image_data.GetSpacing()
origin = image_data.GetOrigin()

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

# Create the reslice object
reslice = vtk.vtkImageReslice()
reslice.SetInputData(image_data)
reslice.SetOutputDimensionality(2)

# Set the reslice parameters
reslice.SetResliceAxesOrigin(center)
reslice.SetResliceAxesDirectionCosines(
    normal[0], normal[1], normal[2],
    -normal[1], normal[0], 0,
    0, 0, 1)
reslice.SetInterpolationModeToLinear()
reslice.Update()

# Get the output from reslice
reslice_output = reslice.GetOutput()
reslice_extent = reslice_output.GetExtent()

# Convert the reslice output to a NumPy array
reslice_array = numpy_support.vtk_to_numpy(reslice_output.GetPointData().GetScalars())
reslice_array = reslice_array.reshape((reslice_extent[3] - reslice_extent[2] + 1,
                                       reslice_extent[1] - reslice_extent[0] + 1))

# Map the CT values to the 0-255 range
min_value = np.min(reslice_array)
max_value = np.max(reslice_array)
scaled_array = np.uint8(255 * (reslice_array - min_value) / (max_value - min_value))

# Save the grayscale image using PIL
image = Image.fromarray(scaled_array)
image.save("cut_section.png")

print("Image saved as 'cut_section.png'")






