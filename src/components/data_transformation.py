import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import os
import sys
from src.utils import save_obj
@dataclass
class DataTransformConfig:
    preprocessor_path : str = os.path.join('artefacts','pre_procc.pkl')

class DataTransformer:
    def __init__(self):
        self.preprocc = DataTransformConfig()
        
    def data_transform_object(self,train_data,target_col):
        try:
            train_set = pd.read_csv(train_data)
            cat_col = []
            num_col = []
            for c in train_set.columns:
                if train_set[c].dtype=='object':
                    cat_col.append(c)
                else:
                    num_col.append(c)
            num_col.remove(target_col)
            num_pipeline = Pipeline(
                steps=[
                    ("Imputer",SimpleImputer(strategy='mean')),
                    ("Scaler", StandardScaler())
                ]
            )
            cat_pipline = Pipeline(
                steps=[
                    ("Imputer",SimpleImputer(strategy='most_frequent')),
                    ("Encoder", OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            pre_processor = ColumnTransformer(
                [
                    ("Categorical Transform",cat_pipline,cat_col),
                    ("Numerical_Transform", num_pipeline,num_col),
                ]
            )

            return pre_processor
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transform(self,train_data,test_data):
        logging.info("Initiating Data Transform")
        try:
            train_set = pd.read_csv(train_data)
            test_set = pd.read_csv(test_data)
            logging.info("Successfully Read Train And Test Data")
            target_col = 'math_score'

            train_target = train_set[target_col]
            test_target = test_set[target_col]

            train_set.drop(columns=[target_col],inplace=True)
            test_set.drop(columns=[target_col],inplace=True)

            
            logging.info("Creating Pre_processing Object")
            procc = self.data_transform_object(train_data,target_col)

            logging.info("Applying Transform")
            train_arr = procc.fit_transform(train_set)
            test_arr  = procc.transform(test_set)

            logging.info("Transform Done")

            
            logging.info("Saving Pickle File ....")

            save_obj(self.preprocc.preprocessor_path,procc)
            logging.info("Pickle File Saved")
            trans_train = np.c_[train_arr,train_target]
            trans_test = np.c_[test_arr,test_target]

            return (trans_train,trans_test,procc)
        except Exception as e:
            raise CustomException(e,sys)




