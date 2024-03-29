import os
import json
import mlflow
import uvicorn
import numpy as np
from pydantic import BaseModel
from fastapi import FastAPI


class FetalHealthData(BaseModel):
    accelerations: float
    fetal_movement: float
    uterine_contractions: float
    severe_decelerations: float


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


def load_model():
    print('reading model...')
    mlflow_tracking_uri = 'https://dagshub.com/matheusperches/mlops-ead-experimentos.mlflow'
    mlflow_tracking_username = 'matheusperches'
    mlflow_tracking_password = '2729db17bcd0f4f9e72aacd86945d7374be88fda'
    os.environ['mlflow_tracking_username'] = mlflow_tracking_username
    os.environ['mlflow_tracking_password'] = mlflow_tracking_password
    print('setting mlflow...')
    mlflow.set_tracking_uri(mlflow_tracking_uri)
    print('Creating client...')
    client = mlflow.MlflowClient(tracking_uri=mlflow_tracking_uri)
    print('getting the registered model')
    registered_model = client.get_registered_model('Fetal_Health_estudo')
    print('reading model...')
    run_id = registered_model.latest_versions[-1].run_id
    logged_model = f'runs:/{run_id}/model'
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    print(loaded_model)
    return loaded_model


@app.on_event(event_type='startup')
def startup_event():
    global loaded_model
    loaded_model = load_model()

@app.get(path='/',
         tags=['Health'])
def api_health():
    return {"status": "healthy"}


@app.post(path='/predict',
          tags=['Prediction'])
def predict(request: FetalHealthData):
    global local_model

    received_data = np.array([
        request.accelerations,
        request.fetal_movement,
        request.uterine_contractions,
        request.severe_decelerations,
    ]).reshape(1, -1)
    print(received_data)
    prediction = loaded_model.predict(received_data)
    print(prediction)
    return {"prediction": str(np.argmax(prediction[0]))}
