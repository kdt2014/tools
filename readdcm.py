import pydicom

# 读取DICOM文件
dicom_file_path = 'E:\dataset\CBCT\post-FA1714_20210303_110310_anonz/3DSlice1.dcm'
dataset = pydicom.dcmread(dicom_file_path)

# 打印DICOM文件的基本信息
print("Patient's Name:", dataset.PatientName)
print("Patient ID:", dataset.PatientID)
print("Modality:", dataset.Modality)
print("Study Date:", dataset.StudyDate)

# 打印所有的元数据
print("\nFull DICOM dataset:")
print(dataset)