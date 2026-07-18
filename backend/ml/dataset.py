from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


ACTIVE_DATASET = (
    BASE_DIR
    / "ml"
    / "data"
    / "processed"
    / "database_training_data.csv"
)


def get_active_dataset():
    return str(ACTIVE_DATASET)