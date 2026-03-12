import subprocess
import logging
import os
from datetime import datetime


LOG_DIR = "outputs/logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)


def run_step(step_name, command):
    logging.info(f"Starting step: {step_name}")

    try:
        subprocess.run(command, check=True)
        logging.info(f"Finished step: {step_name}\n")

    except subprocess.CalledProcessError:
        logging.error(f"Step failed: {step_name}")
        raise


def main():

    pipeline_steps = [

        ("Scan DICOM dataset",
         ["python", "src/dicom_scanner.py"]),

        ("Convert DICOM to CT volumes",
         ["python", "src/dicom_to_volume.py"]),

        ("Preprocess CT volumes",
         ["python", "src/preprocess_ct.py"]),

        ("Visualize CT volumes",
         ["python", "src/visualize_volume.py"])
    ]

    for step_name, command in pipeline_steps:
        run_step(step_name, command)

    logging.info("Pipeline completed successfully.")


if __name__ == "__main__":
    main()