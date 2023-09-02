#!/usr/bin/python3
""" Handles generation of result and creating of the pdf file """

from backend.utils import plots
from backend.models.predictor import get_prediction, preprocess


def generate_results(data):
    """ generate results and pass in dict form """

    name = data['Name']
    diag = "Diabetic" if get_prediction(data) else "Non-diabetic"
    bmi = preprocess(data)['BMI']
    diag_plot = plots.plot_diag_by_bmi_sex(diag, data['Sex'])[1]
    bmi_cat_plot = plots.plot_bmi_category(bmi)[1]
    bmi_dist_plot = plots.plot_bmi_dist(bmi)[1]

    results = {
        "name": name,
        "bmi": bmi,
        "diagnosis": diag,
        "diagnosis_plot": diag_plot,
        "bmi_category_plot": bmi_cat_plot,
        "bmi_distribution_plot": bmi_dist_plot
    }

    return (results)

if __name__=="__main__":
    data = {
        "Name": "Jane Doe", "HighBP": 1, "HighChol": 1, "Height": 2.0, "Weight": 87.0,
        "SticksDay": 10, "YearsSmoked": 12, "HeartDiseaseorAttack": 1, "PhysActivity": 1,
        "Fruits": 1, "Veggies": 0, "HvyAlcoholConsump": 1, "GenHlth": 2, "MentHlth": 23,
        "PhysHlth": 27, "DiffWalk": 1, "Age": 45, "Education": 5, "Income": 5, "Stroke":0, "Sex":1}
    print(type(generate_results(data)))
