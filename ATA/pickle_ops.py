import pickle

from ATA.models import Course

# Path to the pickle file storing course data
DATA_FILEPATH = "data/data.pkl"


def save_data(course: Course):
    """Save course data to pickle file.
    
    Args:
        course: Course object to save.
    """
    with open(DATA_FILEPATH, "wb") as f:
        pickle.dump(course, f)


def load_data() -> Course:
    """Load course data from pickle file.
    
    Returns:
        Course object loaded from the pickle file.
        
    Raises:
        FileNotFoundError: If the pickle file doesn't exist.
        pickle.UnpicklingError: If the file is corrupted or not a valid pickle file.
    """
    with open(DATA_FILEPATH, "rb") as f:
        return pickle.load(f)