#!/usr/bin/python3
"""
Main entry point of the app
"""

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from typing import Union, Any, Dict, Annotated
from pydantic import BaseModel
from dataclasses import dataclass
import os
import json
import base64
import io
import matplotlib
matplotlib.use('AGG')

from backend.models.schemas import FormData
# from backend.models.predictor import get_prediction
from backend.utils.result_generator import generate_results


app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.getcwd(), "frontend", "templates"))

@dataclass
class TestData:
    name: str = Form(...)
    said: str = Form(...)
    nick: str = Form(...)

@app.get('/')
def home(request: Request):
    """ Home Page """
    return templates.TemplateResponse('home.html', context={'request': request})

@app.get('/test')
def test(request: Request):
    """ Test for form """
    result = ""
    return templates.TemplateResponse('test.html',
                                        context={'request': request, 'result':result})

@app.post('/test')
def test(request: Request, form_data: TestData = Depends()):
# def test(request: Request, name: str = Form(...), said: str = Form(...)):
    """ Test for result """
    data = form_data.__dict__
    nick = data.pop('nick')
    # del data['nick']
    # resp = f"{data['name']}, you said {data['said']}. I know your nick is {nick}"
    resp = f"{data} from nick {nick}"
    return templates.TemplateResponse('test_result.html',
                                        context={'request': request, 'result':resp})

@app.get('/predict')
def predict(request: Request):
    """ The prediction function

    Args:
        request: Request - request object
        form_data: FormData - schema for the form data
    """
    return templates.TemplateResponse('predictor.html',
                                        context={'request':request})

@app.post('/predict')
def predict(request: Request, form_data: FormData = Depends()):
    """
    Get data from prediction function
    """
    dataset = form_data.__dict__
    # # result = dataset
    # name = dataset.pop('Name')
    results = generate_results(dataset)

    image_keys = ['diagnosis_plot', 'bmi_category_plot', 'bmi_distribution_plot']
    for image in image_keys:
        buf = io.BytesIO()
        results[image].savefig(buf, format="png")
        encoded = base64.encodebytes(buf.getvalue())
        decoded = base64.decodebytes(encoded)
        results[image] = decoded
        # buf.close()

    # encode images
    # results['diagnosis_plot'] = base64.b64encode(results['diagnosis_plot']).decode('utf-8')
    # results['bmi_category_plot'] = base64.b64encode(results['bmi_category_plot']).decode('utf-8')
    # results['bmi_distribution_plot'] = base64.b64encode(results['bmi_distribution_plot']).decode('utf-8')

    results["request"] = request
    return templates.TemplateResponse('results.html', context=results)
