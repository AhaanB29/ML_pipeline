from src.exception import CustomException
from src.logger import logging
from src.utils import load_obj
import pandas as pd
import sys
class CustomPipeline:
    def __init__(self):
        pass

    def process_data (self,gender,race_ethnicity,parental_level_of_education,lunch,
                      test_preparation_course,reading_score,writing_score):
        try:
            self.gender = gender
            self.race_eth = race_ethnicity
            self.parent_loe = parental_level_of_education
            self.lunch = lunch
            self.test_prepare = test_preparation_course
            self.reading_score = reading_score
            self.writing_score = writing_score
            logging.info("Creating Data Frame...")
            data_dict = {'gender':[self.gender],'race_ethnicity':[self.race_eth]
                         ,'parental_level_of_education':[self.parent_loe],
                         'lunch':[self.lunch],'test_preparation_course':[self.test_prepare],
                         'reading_score':[self.reading_score],'writing_score':[self.writing_score]}
            return pd.DataFrame(data_dict)
        except Exception as e:
            raise CustomException (e,sys)
    
    def predict_data(self,data):
        try:
            model_file_path = 'artefacts/best_model.pkl'
            pre_processor_path= 'artefacts/pre_procc.pkl'

            model = load_obj(model_file_path)
            pre_processor = load_obj(pre_processor_path)
            logging.info("Model File and Pre_processor Loaded Successfully")
            data_trans= pre_processor.transform(data)
            results = model.predict(data_trans)
            logging.info(f"Reults Compiled and returned {results}")
            return results
        
        except Exception as e:
            raise CustomException(e,sys)


