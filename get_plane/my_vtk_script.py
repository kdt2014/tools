import vtk

# 创建一个示例的vtkImageData对象
image_data = vtk.vtkImageData()
image_data.SetDimensions(10, 10, 10)
image_data.AllocateScalars(vtk.VTK_FLOAT, 1)

# 填充一些示例数据
for z in range(10):
    for y in range(10):
        for x in range(10):
            image_data.SetScalarComponentFromFloat(x, y, z, 0, x + y + z)

# 定义一个切割平面
plane = vtk.vtkPlane()
plane.SetOrigin(5, 5, 5)  # 设置平面原点
plane.SetNormal(1, 0, 0)  # 设置平面法向量

# 创建并设置切割器
cutter = vtk.vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputData(image_data)
cutter.Update()

# 获取切割结果
cut_data = cutter.GetOutput()

# 打印切割结果中的点
for i in range(cut_data.GetNumberOfPoints()):
    point = cut_data.GetPoint(i)
    print(f"Point {i}: {point}")

# 可视化切割结果（可选）
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(cut_data)

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.3)  # 设置背景颜色

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

render_window.Render()
render_window_interactor.Start()
