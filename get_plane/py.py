import vtk
import numpy as np

# 定义三个点的坐标
p1 = [-15.034228302882678, -30.2137484248086, -22.84246285093691]
p2 = [-14.089678248570625, -28.263273122123387, -14.914172739473898]
p3 = [-16.688125349924306, -25.396670932765616, -36.30480886717598]

# 定义方向矩阵
orientation = [-1.0, -0.0, -0.0,
               -0.0, -1.0, -0.0,
                0.0,  0.0,  1.0]

# 将方向矩阵转换为 numpy 数组
orientation_matrix = np.array(orientation).reshape(3, 3)

# 计算平面的法向量
v1 = np.array(p2) - np.array(p1)
v2 = np.array(p3) - np.array(p1)
normal = np.dot(orientation_matrix, np.cross(v1, v2))
normal = normal / np.linalg.norm(normal)  # 归一化

print("Normal Vector: ", normal)

# 读取nii文件
nii_file = r'E:\CBCTandannotation\myannotation\p1\DCBCTImageSet.nii'
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(nii_file)
reader.Update()

# 检查数据范围
image_data = reader.GetOutput()
extent = image_data.GetExtent()
spacing = image_data.GetSpacing()
origin = image_data.GetOrigin()

print("Data Extent: ", extent)
print("Data Spacing: ", spacing)
print("Data Origin: ", origin)

# 设置平面的原点为数据中心
center = [
    origin[0] + spacing[0] * 0.5 * (extent[0] + extent[1]),
    origin[1] + spacing[1] * 0.5 * (extent[2] + extent[3]),
    origin[2] + spacing[2] * 0.5 * (extent[4] + extent[5])
]
print("Plane Origin (Center): ", center)

# 可视化三维数据
volume_mapper = vtk.vtkSmartVolumeMapper()
volume_mapper.SetInputData(image_data)

volume_color = vtk.vtkColorTransferFunction()
volume_color.AddRGBPoint(0, 0.0, 0.0, 0.0)
volume_color.AddRGBPoint(1000, 1.0, 1.0, 1.0)

volume_scalar_opacity = vtk.vtkPiecewiseFunction()
volume_scalar_opacity.AddPoint(0, 0.00)
volume_scalar_opacity.AddPoint(1000, 0.15)

volume_property = vtk.vtkVolumeProperty()
volume_property.SetColor(volume_color)
volume_property.SetScalarOpacity(volume_scalar_opacity)

volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

renderer = vtk.vtkRenderer()
renderer.AddVolume(volume)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# 可视化三维数据
render_window.Render()

# 创建平面
plane = vtk.vtkPlane()
plane.SetOrigin(center)
plane.SetNormal(normal)

# 使用平面进行切割
cutter = vtk.vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputData(image_data)
cutter.Update()

# 检查切割结果
cutter_output = cutter.GetOutput()
print("Cutter Output Number of Points: ", cutter_output.GetNumberOfPoints())
print("Cutter Output Number of Cells: ", cutter_output.GetNumberOfCells())

# 显示切割结果
cutter_mapper = vtk.vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())

cutter_actor = vtk.vtkActor()
cutter_actor.SetMapper(cutter_mapper)
cutter_actor.GetProperty().SetColor(1, 0, 0)  # 将切割平面设置为红色

# 添加切割平面到渲染器
renderer.AddActor(cutter_actor)

# 强制重新渲染
render_window.Render()

# 将当前截面保存为 PNG 图片
window_to_image_filter = vtk.vtkWindowToImageFilter()
window_to_image_filter.SetInput(render_window)
window_to_image_filter.SetScale(1)  # 可以根据需要调整分辨率
window_to_image_filter.SetInputBufferTypeToRGBA()
window_to_image_filter.ReadFrontBufferOff()
window_to_image_filter.Update()

png_writer = vtk.vtkPNGWriter()
png_writer.SetFileName("cut_section.png")
png_writer.SetInputConnection(window_to_image_filter.GetOutputPort())
png_writer.Write()

# 启动交互
render_window_interactor.Start()

