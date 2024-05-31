import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

# Read NIfTI file
nii_file = 'E:\\CBCTandannotation\\myannotation\\p1\\DCBCTImageSet.nii'
image = sitk.ReadImage(nii_file)
image_array = sitk.GetArrayFromImage(image)

# Provided points in physical coordinates
point1 = np.array([-15.034228302882678, -30.2137484248086, -22.84246285093691])
point2 = np.array([-14.089678248570625, -28.263273122123387, -14.914172739473898])
point3 = np.array([-16.688125349924306, -25.396670932765616, -36.30480886717598])

# Convert physical coordinates to image indices
def physical_to_index(physical_point, image):
    return np.array(image.TransformPhysicalPointToIndex(physical_point))

index1 = physical_to_index(point1, image)
index2 = physical_to_index(point2, image)
index3 = physical_to_index(point3, image)

print("Index 1:", index1)
print("Index 2:", index2)
print("Index 3:", index3)

# Calculate the plane normal vector
vec1 = index2 - index1
vec2 = index3 - index1
normal = np.cross(vec1, vec2)
normal = normal / np.linalg.norm(normal)

# Get image spacing
spacing = image.GetSpacing()

# Function to extract plane from image array
def extract_plane(image_array, normal, point, spacing, size=(512, 512)):
    d = -np.dot(normal, point)
    xx, yy = np.meshgrid(np.arange(size[0]), np.arange(size[1]), indexing='ij')
    zz = (-normal[0] * xx - normal[1] * yy - d) / normal[2]

    plane_points = np.vstack((xx.ravel(), yy.ravel(), zz.ravel())).T
    plane_points = plane_points * np.array(spacing)

    plane_points = np.round(plane_points).astype(int)
    plane_points[:, 0] = np.clip(plane_points[:, 0], 0, image_array.shape[1] - 1)
    plane_points[:, 1] = np.clip(plane_points[:, 1], 0, image_array.shape[0] - 1)
    plane_points[:, 2] = np.clip(plane_points[:, 2], 0, image_array.shape[2] - 1)

    plane_coords = np.vstack((plane_points[:, 1], plane_points[:, 0], plane_points[:, 2]))
    plane_image = ndimage.map_coordinates(image_array, plane_coords, order=1)
    plane_image = plane_image.reshape(size)

    return plane_image

# Extract and display the plane
plane_image = extract_plane(image_array, normal, index1, spacing)

plt.imshow(plane_image, cmap='gray')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Extracted Plane')
plt.colorbar()
plt.show()

# Display the middle slice of the image
mid_slice = image_array.shape[2] // 2
plt.imshow(image_array[:, :, mid_slice], cmap='gray')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Middle Slice of Image')
plt.colorbar()
plt.show()
