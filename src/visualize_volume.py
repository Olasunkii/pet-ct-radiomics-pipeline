import os
import SimpleITK as sitk
import matplotlib.pyplot as plt
from config_loader import load_config


def visualize_volume(volume_path):
    """
    Display middle slice of a CT volume.
    """

    image = sitk.ReadImage(volume_path)
    volume = sitk.GetArrayFromImage(image)

    mid_slice = volume.shape[0] // 2

    plt.imshow(volume[mid_slice], cmap="gray")
    plt.title(f"Middle slice: {os.path.basename(volume_path)}")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":

    config = load_config()

    processed_path = config["data"]["processed_path"]

    volumes = os.listdir(processed_path)

    for vol in volumes:
        if vol.endswith(".nii.gz"):

            path = os.path.join(processed_path, vol)

            print(f"Visualizing {vol}")

            visualize_volume(path)