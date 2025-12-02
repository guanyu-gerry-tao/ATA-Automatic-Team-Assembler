import pickle

from ATA.models import Course

DATA_FILEPATH = "data/data.pkl"

def save_data(course: Course):
    with open(DATA_FILEPATH, "wb") as f:
        pickle.dump(course, f)


def load_data() -> Course:
    with open(DATA_FILEPATH, "rb") as f:
        return pickle.load(f)