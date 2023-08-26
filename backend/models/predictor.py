#!/usr/bin/python3
"""
Module for the prediction feature using model,
and other ML-related functionalities
"""

import os
import sys
import json
import pickle
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# define file paths
model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                            'storage', 'gradboost_model.pkl')
dataset_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                            'storage', 'diabetes_012_health_indicators_BRFSS2015.csv')

# load model
with open(model_path, 'rb') as file:
    pred_model = pickle.load(file)

# extract the values (options) of the variables from the dataset
var_names = {}
df = pd.read_csv(dataset_path)
for col in df.columns:
    var_names[col] = df[col].unique()


def preprocess(dataset: dict) -> dict:
    """ Preporcess the data for wrangle function

    Converts height and weight into BMI
    Converts sticks/day and yearsomked into packyears
    Preprocess Age into appropriate category

    Args:
        dataset: dictionary of values
    
    Return:
        the processed data (dict)
    """

    dataset['BMI'] = dataset['Weight'] / (dataset['Height'] ** 2)

    # compute pack years
    pack_years = (dataset['SticksDay'] * dataset['YearsSmoked']) / 20
    if pack_years > 10:
        dataset['Smoker'] = 1
    else:
        dataset['Smoker'] = 0

    # preprocess age
    # helper function to group age, this should only apply if it's coming from form/dict
    def categorize_age(age):
        if age < 25:
            return (1)
        elif age < 30:
            return (2)
        elif age < 35:
            return (3)
        elif age < 40:
            return (4)
        elif age < 45:
            return (5)
        elif age < 50:
            return (6)
        elif age < 55:
            return (7)
        elif age < 60:
            return (8)
        elif age < 65:
            return (9)
        elif age < 70:
            return (10)
        elif age < 75:
            return (11)
        elif age < 80:
            return (12)
        else:
            return (13)
    dataset['Age'] = categorize_age(dataset['Age'])

    return(dataset)

# define wrangle function
def wrangle(dataset):
    """ Perform the wrangling operation on data

    Args:
        dataset([str, dict/json]): data can be passed from a file with name as str,
            or from a dictionary with key:value pairs as col_name:col_value
    
    Return:
        pd.DataFrame
    """

    try:
        df = pd.read_csv(dataset)
    except:
        processed_data =  preprocess(dataset)
        df = pd.DataFrame(processed_data, index=[0])
    
    # create new df with selected features
    f_df = df[['HighBP', 'HighChol', 'BMI', 'Smoker', 'Stroke',
                  'HeartDiseaseorAttack', 'PhysActivity',
                  'HvyAlcoholConsump', 'GenHlth', 'MentHlth',
                  'PhysHlth', 'DiffWalk', 'Age', 'Education', 'Income']]
    
    # if there's a Diabetes_012 column, convert to binary,
    # else, ignore it
    try:
        df['Diabetes_012'][df['Diabetes_012']==2]=1

        # copy to new features df
        f_df['Diabetes_01'] = df['Diabetes_012']
    except KeyError:
        pass

    # drop duplicates
    f_df.drop_duplicates(inplace=True)

    return (f_df)


def get_prediction(dataset):
    """ Does the prediction
    
    Args:
        dataset: the dataset to predict on
    
    Returns:
        the value of the prediction
    """

    wrangled_data = wrangle(dataset)
    prediction = pred_model.predict(wrangled_data)

    return (prediction)

if __name__ == "__main__":
    dataset = json.loads(sys.argv[1])
    # print(type(dataset))
    # print(len(dataset))
    # print(wrangle(dataset))
    # print(dataset['MentHlth'])
    print(int(get_prediction(dataset)))
