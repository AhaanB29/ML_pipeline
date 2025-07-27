from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
import os
import sys
import xgboost as xgb
import catboost as catb
from sklearn import linear_model
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from src.utils import save_obj,evaluate_models
@dataclass
class ModelTrainerConfig:
    model_trainer_file_path :str =  os.path.join('artefacts','best_model.pkl')


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def model_trainer_initiater(self,train_data,test_data):
        logging.info("Initiating Model Training")
        try:
            logging.info("Splitting the Data to get Target and Input.")
            X_train,y_train,X_test,y_test = train_data[:,:-1],train_data[:,-1],test_data[:,:-1],test_data[:,-1]

            logging.info("Creating Model Objects")
            models ={
            'LinearRegression':linear_model.LinearRegression(),
            'Lasso': linear_model.Lasso(),
            'Ridge': linear_model.Ridge(),
            'XGB': xgb.XGBRegressor(),
            'CatBoost':catb.CatBoostRegressor(verbose=False),
            'SVR': svm.SVR()
                            }
            
            logging.info("Models Initiated")
            results={}
            best_model = None
            best_r2_score = 0.0
            for i in models.keys():
                models[i].fit(X_train,y_train)
                y_pred_train,y_pred_test = models[i].predict(X_train),models[i].predict(X_test)
                r_score_test,r_score_train= evaluate_models(y_pred_train,y_train,y_pred_test,y_test)
                results[i] = r_score_test

                if(r_score_test>best_r2_score):
                    best_model = models[i]
                    best_r2_score = r_score_test

            logging.info(f"Best Model is {best_model} With R2 score {best_r2_score}")
            save_obj(self.model_trainer_config.model_trainer_file_path,best_model)
            return (self.model_trainer_config.model_trainer_file_path,best_r2_score)

        except Exception as e:
            raise CustomException(e,sys)