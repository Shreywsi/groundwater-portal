import subprocess
import os


def retrain_model():

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    train_file = os.path.join(
        BASE_DIR,
        "ml",
        "train.py"
    )

    result = subprocess.run(
        [
            "python",
            train_file
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(result.stderr)


    return {
        "success": True,
        "message": "Model retrained successfully"
    }