from src.logger import logging
from src.exception import CustomException
import pickle
import os
import sys


def save_obj(file_path, obj):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as wght_file:
            pickle.dump(obj,wght_file)
    except Exception as e:
        raise CustomException (e,sys)