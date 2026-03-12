import os
import pydicom
import pandas as pd
from tqdm import tqdm
from config_loader import load_config

def detect_series(series_path):
    """
    Detect modality (CT or PET) from a DICOM series.
    """
    files = [f for f in os.listdir(series_path) if f.endswith(".dcm")]

    if len(files) == 0:
        return None, 0

    first_file = os.path.join(series_path, files[0])

    try:
        dcm = pydicom.dcmread(first_file, stop_before_pixels=True)
        #modality = dcm.Modality
        modality = getattr(dcm, "Modality", )
    except:
        modality = "UNKNOWN"

    return modality, len(files)


def scan_dataset(data_root):
    """
    Scan dataset and build CT/PET summary.
    """

    records = []

    patients = os.listdir(data_root)

    for patient in tqdm(patients):

        patient_path = os.path.join(data_root, patient, "dicom")

        if not os.path.exists(patient_path):
            continue

        series_folders = os.listdir(patient_path)

        for series in series_folders:

            series_path = os.path.join(patient_path, series)

            modality, num_files = detect_series(series_path)

            records.append({
                "patient_id": patient,
                "series_name": series,
                "modality": modality,
                "num_slices": num_files
            })

    df = pd.DataFrame(records)

    return df


if __name__ == "__main__":

    config = load_config()

    data_path = config["data"]["raw_path"]
    output_file = config["data"]["dataset_index"]

    df = scan_dataset(data_path)

    print(df)

    df.to_csv(output_file, index=False)

    print(f"\nDataset index saved to {output_file}")