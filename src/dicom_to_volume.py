import os
import SimpleITK as sitk
from config_loader import load_config

def dicom_series_to_volume(series_path, output_path):
    """
    Convert a DICOM series into a 3D NIfTI volume.
    """

    reader = sitk.ImageSeriesReader()

    dicom_names = reader.GetGDCMSeriesFileNames(series_path)
    reader.SetFileNames(dicom_names)

    image = reader.Execute()

    sitk.WriteImage(image, output_path)

    print(f"Saved volume to {output_path}")


def process_dataset(data_root, output_root):

    patients = os.listdir(data_root)

    for patient in patients:

        dicom_path = os.path.join(data_root, patient, "dicom")

        if not os.path.exists(dicom_path):
            continue

        series_list = os.listdir(dicom_path)

        for series in series_list:

            if "CT" not in series:
                continue

            series_path = os.path.join(dicom_path, series)

            output_file = os.path.join(
                output_root,
                f"{patient}_ct.nii.gz"
            )

            dicom_series_to_volume(series_path, output_file)


if __name__ == "__main__":

    config = load_config()

    data_path = config["data"]["raw_path"]
    output_path = config["data"]["processed_path"]

    os.makedirs(output_path, exist_ok=True)

    process_dataset(data_path, output_path)