import pandas as pd 
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import os, sys
import pickle

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig
    
    def get_data_transformer_object(self):
        try:
            numerical_columns = ['carat', 'depth', 'table', 'x', 'y', 'z']
            cut_category = ["Fair","Good","Very Good","Premium","Ideal"]
            color_category = ["D","E","F","G","H","I","J"]
            clarity_category = ["I1","SI2","SI1","VS2","VS1","VVS2","VVS1","IF"]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("ordinalencoder", OrdinalEncoder(categories=[cut_category, color_category, clarity_category])),
                    ("scaler", StandardScaler())
                ]
            )


            logging.info(f"Categorical columns: {cut_category}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, cut_category),
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_transformation(self, train_path, test_path):
       try:
           train_data = pd.read_csv(train_path)
           test_data = pd.read_csv(test_path)

           input_train_data = train_data.drop(columns=['id', "price"])
           input_test_data = test_data.drop(columns=['id', "price"])

           preprocessor_obj = self.get_data_transformer_object()
           preprocessor_obj.fit_transform(input_train_data)
           preprocessor_obj.transform(input_test_data)

           pickle.dump(preprocessor_obj, open(self.data_transformation_config.preprocessor_obj_file_path, 'wb'))

           

       except Exception as e:
            raise CustomException(e,sys)