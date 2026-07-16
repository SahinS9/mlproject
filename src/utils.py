import os 
import pickle
from typing import Any


def save_object(file_path: str, obj: Any) -> None:
    directory = os.path.dirname(file_path)

    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(file_path, "wb") as file:
        pickle.dump(obj, file)
    

def laod_object(file_path: str) -> Any:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No file found at: {file_path}")
    
    with open(file_path, "rb") as file:
        return pickle.load(file)