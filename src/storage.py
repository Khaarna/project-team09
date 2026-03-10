import os
import hashlib
import pickle

from models import AddressBook, NotesBook

_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATA_FILE = os.path.join(_DATA_DIR, "data.pkl")
HASH_FILE = os.path.join(_DATA_DIR, "data.hash")


def save_data(
    book: AddressBook,
    notes: NotesBook,
    filename: str = DATA_FILE,
    hash_filename: str = HASH_FILE,
) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data_bytes = pickle.dumps({"book": book, "notes": notes})
    temp_file = filename + ".tmp"
    with open(temp_file, "wb") as f:
        f.write(data_bytes)
    os.replace(temp_file, filename)
    with open(hash_filename, "w") as f:
        f.write(hashlib.sha256(data_bytes).hexdigest())


def load_data(
    filename: str = DATA_FILE,
    hash_filename: str = HASH_FILE,
) -> tuple[AddressBook, NotesBook]:
    try:
        with open(filename, "rb") as f:
            data_bytes = f.read()
        with open(hash_filename, "r") as f:
            saved_hash = f.read().strip()
        if hashlib.sha256(data_bytes).hexdigest() != saved_hash:
            print("Warning: data integrity check failed. Starting fresh.")
            return AddressBook(), NotesBook()
        data = pickle.loads(data_bytes)
        return data["book"], data["notes"]
    except FileNotFoundError:
        return AddressBook(), NotesBook()
    except (AttributeError, pickle.UnpicklingError, KeyError):
        print("Warning: could not load data. Starting fresh.")
        return AddressBook(), NotesBook()
