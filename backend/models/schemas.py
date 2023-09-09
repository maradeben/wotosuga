#!/usr/bin/python3
""" define schema classes
FormData: form data schema, as gotten from the predictions form
"""
from dataclasses import dataclass
from fastapi import Form
import uuid


@dataclass
class TestData:
    name: str = Form(...)
    said: str = Form(...)
    nick: str = Form(...)
   

# define schema for form data
@dataclass
class FormData:
    """ This class defines the schema for the form data
    associated with the prediction form
    """
    id:                        str= uuid.uuid4()
    Name:                   str = Form(...)
    HighBP:                 int = Form(...)
    HighChol:               int = Form(...)
    # CholCheck:              int = Form(...)
    # BMI:                    float = Form(...)
    Height:                 float = Form(...)
    Weight:                 float = Form(...)
    # Smoker:                 int = Form(...)
    SticksDay:              int = Form(...)
    YearsSmoked:            int = Form(...)
    Stroke:                 int = Form(...)
    HeartDiseaseorAttack:   int = Form(...)
    PhysActivity:           int = Form(...)
    Fruits:                 int = Form(...)
    Veggies:                int = Form(...)
    HvyAlcoholConsump:      int = Form(...)
    # AnyHealthcare:          int = Form(...)
    # NoDocbcCost:            int = Form(...)
    GenHlth:                int = Form(...)
    MentHlth:               int = Form(...)
    PhysHlth:               int = Form(...)
    DiffWalk:               int = Form(...)
    Age:                    int = Form(...)
    Sex:                    int = Form(...)
    Education:              int = Form(...)
    Income:                 int = Form(...)
