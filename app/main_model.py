import os
import json
import mlflow
import numpy as np
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI(title="Fetal Health API",
              openapi_tags=[
                  {
                      "name": "Health",
                      "description": "Get API Health"

                  },
                  {
                      "name": "Prediction",
                      "description": "Model prediction"
                  }
              ])


@app.get(path='/',
         tags=['Health'])
def api_health():
    return {"status": "healthy"}


@app.post(path='/predict',
          tags=['Prediction'])
def predict():
    return {"prediction": 0}
