import os
import SimpleITK as sitk
from config_loader import load_config


def preprocess_ct(input_path, output_path):

    image = sitk.ReadImage(input_path)

    # HU clipping
    image = sitk.Clamp(image, lowerBound=-1000, upperBound=400)

    # Resample to 1mm spacing
    new_spacing = [1.0, 1.0, 1.0]
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()

    new_size = [
        int(round(osz * ospc / nspc))
        for osz, ospc, nspc in zip(original_size, original_spacing, new_spacing)
    ]

    resampler = sitk.ResampleImageFilter()
    resampler.SetOutputSpacing(new_spacing)
    resampler.SetSize(new_size)
    resampler.SetInterpolator(sitk.sitkLinear)

    resampled = resampler.Execute(image)

    sitk.WriteImage(resampled, output_path)

    print(f"Saved preprocessed CT → {output_path}")


if __name__ == "__main__":

    config = load_config()

    processed_path = config["data"]["processed_path"]
    output_dir = "data/preprocessed"

    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(processed_path):

        if file.endswith(".nii.gz"):

            input_path = os.path.join(processed_path, file)
            output_path = os.path.join(output_dir, file)

            preprocess_ct(input_path, output_path)