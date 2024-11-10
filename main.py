import pickle
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ModelInput(BaseModel):
    pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int

# Get the model path from the environment variable
model_path = os.getenv("MODEL_PATH", "trained_model/diabetes_model.pkl")
diabetes_model = pickle.load(open(model_path, 'rb'))

@app.post('/diabetes_prediction')
def diabetes_pred(input_parameters: ModelInput):
    preg = input_parameters.pregnancies
    glu = input_parameters.Glucose
    bp = input_parameters.BloodPressure
    skin = input_parameters.SkinThickness
    insulin = input_parameters.Insulin
    bmi = input_parameters.BMI
    dpf = input_parameters.DiabetesPedigreeFunction
    age = input_parameters.Age

    input_list = [preg, glu, bp, skin, insulin, bmi, dpf, age]
    prediction = diabetes_model.predict([input_list])

    if prediction[0] == 0:
        result = {"label": 0, "result": "The person is not diabetic"}
    else:
        result = {"label": 1, "result": "The person is diabetic"}

    return result
