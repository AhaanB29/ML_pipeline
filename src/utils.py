from src.logger import logging
from src.exception import CustomException
import pickle
import os
import sys
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error

def save_obj(file_path, obj):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as wght_file:
            pickle.dump(obj,wght_file)
    except Exception as e:
        raise CustomException (e,sys)

def evaluate_models(y_pred_train,y_train,y_pred_test,y_test):
    try:
        r2_train,mae_train,mse_train = r2_score(y_train,y_pred_train),mean_absolute_error(y_train,y_pred_train),mean_squared_error(y_train,y_pred_train)

        r2_test,mae_test,mse_test = r2_score(y_test,y_pred_test),mean_absolute_error(y_test,y_pred_test),mean_squared_error(y_test,y_pred_test)

        return r2_test,r2_train
    except Exception as e:
        raise CustomException(e,sys)