from src.exception import CustomException
from src.logger import logging
import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class Dataconfig:
    train_data_path :str = os.path.join('artefacts','train.csv')
    test_data_path :str  = os.path.join('artefacts','test.csv')
    raw_data_path :str   = os.path.join('artefacts','raw_data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = Dataconfig()

    def initiate_ingestion(self):
        try:
            logging.info("Reading Raw Data.")
            data = pd.read_csv("notebook/stud.csv")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            data['Total_Score'] = data['math_score']+ data['writing_score'] + data['reading_score']

            logging.info("Splitting the Data into ")
            train_data,test_data = train_test_split(data,test_size=0.3,random_state=42)

            logging.info("Saving in CSV format")
            data.to_csv(self.ingestion_config.raw_data_path,header=True,index=False)
            train_data.to_csv(self.ingestion_config.train_data_path,header=True,index=False)
            test_data.to_csv(self.ingestion_config.test_data_path,header=True,index=False)

            logging.info("Ingestion of data Successfully Completed")

            return (self.ingestion_config.train_data_path,self.ingestion_config.test_data_path)
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_set,test_set = obj.initiate_ingestion()