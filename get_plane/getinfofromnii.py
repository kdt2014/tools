import nibabel as nib

# 读取NIfTI文件
nii_file_path = 'E:\\CBCTandannotation\\myannotation\\p1\\DCBCTImageSet.nii'
img = nib.load(nii_file_path)

# 提取头信息
header = img.header

# 提取元数据并打印
print("Full NIfTI Header Information:")

# 打印所有头信息字段和值
for key in header.keys():
    value = header[key]
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    print(f"{key}: {value}")
