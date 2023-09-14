#!/usr/bin/python3
"""
Main entry point of the app
"""

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Union, Any, Dict
from pydantic import BaseModel
from dataclasses import dataclass
import os
import json
import base64
import io
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt

from backend.models.schemas import FormData
# from backend.models.predictor import get_prediction
from backend.utils.result_generator import generate_results
from backend.utils import static_dir


app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir),
                name="static")
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

    results["request"] = request
    return templates.TemplateResponse('results.html', context=results)


    name: str = Form(...)
    said: str = Form(...)
    nick: str = Form(...)

@app.get('/blog')
def blog(request: Request):
    """ Blog Page """
    return templates.TemplateResponse('blog.html', context={'request': request})
    
    name: str = Form(...)
    said: str = Form(...)
    nick: str = Form(...)

@app.get('/specialists')
def specialists(request: Request):
    """ Healthcare Specialists Page """
    return templates.TemplateResponse('specialists.html', context={'request': request})

@app.get('/profile')
def profile(request: Request):
    """ Home Page """
    return templates.TemplateResponse('profile.html', context={'request': request})

    name: str = Form(...)
    said: str = Form(...)
    nick: str = Form(...)

@app.get('/dev')
def dev(request: Request):
    """ Home Page """
    return templates.TemplateResponse('dev.html', context={'request': request})
