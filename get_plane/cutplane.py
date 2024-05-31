import nibabel as nib
import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk


def load_nifti_image(file_path):
    nifti_img = nib.load(file_path)
    return nifti_img.get_fdata(), nifti_img.affine


def create_vtk_image_from_numpy(data):
    vtk_data = numpy_to_vtk(num_array=data.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(data.shape)
    vtk_image.GetPointData().SetScalars(vtk_data)
    return vtk_image


def create_reslice_matrix(p1, p2, p3):
    # Create a plane using three points
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    # Calculate the normal vector of the plane
    v1 = p2 - p1
    v2 = p3 - p1
    normal = np.cross(v1, v2)
    normal = normal / np.linalg.norm(normal)

    # Create the transformation matrix
    matrix = vtk.vtkMatrix4x4()
    for i in range(3):
        matrix.SetElement(i, 0, v1[i])
        matrix.SetElement(i, 1, v2[i])
        matrix.SetElement(i, 2, normal[i])
        matrix.SetElement(i, 3, p1[i])
    return matrix


def reslice_image(image, reslice_matrix):
    reslice = vtk.vtkImageReslice()
    reslice.SetInputData(image)
    reslice.SetResliceAxes(reslice_matrix)
    reslice.SetInterpolationModeToLinear()
    reslice.Update()
    return reslice.GetOutput()


def apply_colormap(image):
    color_map = vtk.vtkImageMapToColors()
    color_map.SetInputData(image)
    colormap = vtk.vtkLookupTable()
    colormap.SetNumberOfTableValues(256)
    colormap.Build()

    # Hot colormap (from black to red, orange, yellow, white)
    for i in range(256):
        r = min(1.0, i / 255.0 * 2)
        g = min(1.0, i / 255.0 * 2) if i > 127 else 0.0
        b = 0.0
        colormap.SetTableValue(i, r, g, b, 1.0)

    color_map.SetLookupTable(colormap)
    color_map.Update()
    return color_map.GetOutput()


def visualize_image(image):
    viewer = vtk.vtkImageViewer2()
    viewer.SetInputData(image)
    viewer.SetColorWindow(255)
    viewer.SetColorLevel(127.5)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    viewer.SetupInteractor(render_window_interactor)
    viewer.Render()
    viewer.GetRenderer().ResetCamera()
    viewer.Render()
    render_window_interactor.Start()


# 使用示例
nii_file = 'E:\\CBCTandannotation\\myannotation\\p1\\DCBCTImageSet.nii'
point1 = [-15.034228302882678, -30.2137484248086, -22.84246285093691]
point2 = [-14.089678248570625, -28.263273122123387, -14.914172739473898]
point3 = [-16.688125349924306, -25.396670932765616, -36.30480886717598]

data, affine = load_nifti_image(nii_file)
vtk_image = create_vtk_image_from_numpy(data)
reslice_matrix = create_reslice_matrix(point1, point2, point3)
resliced_image = reslice_image(vtk_image, reslice_matrix)
colored_image = apply_colormap(resliced_image)
visualize_image(colored_image)


