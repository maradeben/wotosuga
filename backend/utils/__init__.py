""" Utility/Helper objects and functions """
import os
import pandas as pd

dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                                            'models', 'storage', 'diabetes_012_health_indicators_BRFSS2015.csv')
c_palette = ['#2980b9', '#558b2f', '#d9f0e3', '#ffffff']


def process_df(filepath):
    df = pd.read_csv(filepath)

    # convert diabetes to binary
    df['Diabetes_01'] = df['Diabetes_012'].copy()
    df['Diabetes_01'][df['Diabetes_012'] == 2] = 1
    df.head()

    # fix datatypes
    for col in df.columns:
        try:
            df[col] = df[col].astype(int)
        except:
            pass
        order = df[col].value_counts().index.sort_values()
        ordered_var = pd.api.types.CategoricalDtype(ordered=True,
                                                    categories = order)
        df[col] = df[col].astype(ordered_var)
    
    df['Diabetes_01'] = df['Diabetes_01'].astype(int)
    df['Diabetes_012'] = df['Diabetes_012'].astype(int)
    df['BMI'] = df['BMI'].astype(int)

    return (df)

# process age encodings
def do_age_encodings():
    age_encodings = []
    age_categories = df.Age.unique().sort_values()

    lower, upper = 18, 24
    for age in age_categories:
        if age==1:
            pass
        elif age==2:
            lower+=7
            upper+=5
        else:
            lower+=5
            upper+=5
        age_encodings.append(f'{lower}-{upper}')

    # adjust the last range to capture all values greater than 80
    age_encodings[-1] = '>=80'
    return (age_encodings)


df = process_df(dataset_path)
age_encodings = do_age_encodings()
