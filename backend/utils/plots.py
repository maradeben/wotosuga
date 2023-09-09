#!/usr/bin/python3
"""
Contains plots to be served to upon receipt of results.
All plots highlights where user falls in the distribution
"""
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from backend.utils import df, c_palette, age_encodings, static_dir


sns.set_theme(font_scale=.9)
sns.set_palette(c_palette)
colors = sns.color_palette(c_palette)
primary = colors[1]
sns.set_style(rc={"axes.facecolor" : colors[2], 'figure.facecolor':colors[2]})
title_style = {'size':12, 'color': colors[1], 'weight':'bold'}
axes_style = {'size':10, 'color': colors[1], 'weight':'bold'}



bmi_encodings = ['Underweight', 'Healthy Weight', 'Overweight', 'Obese', 'Extremely Obese']
diab_encodings = ['Non-Diabetic', 'Pre-Diabetic', 'Diabetic']
diab_bin_encodings = ['Non-Diabetic', 'Diabetic']
sex_encodings = ['F', 'M']
age_encodings = age_encodings


def plot_bmi_dist(bmi, id):
    """ Plot BMI distribution

    Args:
        bmi(int): BMI of person
    
    Return:
        (fig, save_path) (plt.figure, str(path where file is saved))
    """

    fig = plt.figure(figsize=(5,4))
    bins = np.arange(df.BMI.min(), df.BMI.max()+1, 1)
    plt.hist(data=df, x='BMI', bins=bins);
    plt.bar(x=bmi, height=28000, width=.3, color='red', hatch='/')
    plt.xlim(15, 60);
    plt.ylim(0, 25000)
    plt.xlabel('BMI');
    plt.ylabel('Frequency');
    plt.title('Distribution of BMI', fontdict=title_style);
    plt.xlabel('BMI', fontdict=axes_style)
    plt.ylabel('Frequency', fontdict=axes_style)

    save_path = f"charts/{id}-bmi_dist.jpg"
    plt.savefig(os.path.join(static_dir, save_path), dpi=200)

    return (fig, save_path)

def plot_diag_by_bmi_sex(diag, sex, id):
    """ Plot diagnosis by BMI and Sex

    Args:
        diag(int): diagnosis, 0 is non-diabetic or 1
        sex(int): of user, 0 is Female
    
    Returns:
        figure(plt.figure)
    """

    fig = plt.figure(figsize=(5,4))
    g = sns.barplot(data=df, x='Sex', y='BMI', hue='Diabetes_01');

    idx = 0
    if sex==0 and diag==0: # female, non-diabetic
        idx = 0
    elif sex==0 and diag==1: # female, diabetic
        idx = 1
    elif sex==1 and diag==0: # male, non-diabetic
        idx = 2
    elif sex==1 and diag==1: # male, diabetic
        idx=3

    # highlight class
    g.patches[idx].set_edgecolor('red')

    plt.xticks(ticks=np.arange(2), labels=sex_encodings);
    plt.xlabel('Sex', fontdict=axes_style);
    plt.ylabel('Average BMI', fontdict=axes_style);
    plt.title('Diabetes by BMI and Sex\n', fontdict=title_style);
    plt.legend(bbox_to_anchor=[0.15,1.1], title='')
    for t,l in zip(g.legend_.texts, diab_bin_encodings):
        t.set_text(l)
    
    save_path = f"charts/{id}-diag_bmi_sex.jpg"
    plt.savefig(os.path.join(static_dir, save_path), dpi=200)
    
    return (fig, save_path)


def categorize_bmi(value):

    """This function takes a BMI value and checks which range it falls in.
    It then returns which category of BMI the given value falls in."""
    
    if value < 18.5:
        return 1
    elif value>=18.5 and value<=24.9:
        return 2
    elif value>=25.0 and value<=29.9:
        return 3
    elif value>=30.0 and value<=39.9:
        return 4
    elif value>=40.0:
        return 5

def plot_bmi_category(bmi, id):
    """ Categorize BMI

    Arg:
        bmi(float): user's BMI
    
    Return:
        fig(plt.figure)
    """

    df['BMICategory'] = df.BMI.apply(categorize_bmi)
    fig=plt.figure(figsize=(5,4))
    g = sns.countplot(data=df, y='BMICategory', color=primary, orient='h', order = [5,4,3,2,1]);

    g.patches[5 - (categorize_bmi(bmi))].set_edgecolor('red')
    # the order of patches is reversed

    plt.yticks(ticks = np.arange(5), labels=bmi_encodings[::-1]);
    plt.xlabel('Frequency', fontdict=axes_style);
    plt.ylabel('');
    plt.title('BMI Categories', fontdict=title_style);

    save_path = f"charts/{id}-bmi_cat.jpg"
    plt.savefig(os.path.join(static_dir, save_path), dpi=200)

    return (fig, save_path)


if __name__ == "__main__":
    diag, sex = sys.argv[1:]
    fig = plot_diag_by_bmi_sex(int(diag), int(sex))
    plt.savefig('diag')
    