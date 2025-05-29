from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json


class Patient(BaseModel):

    id: Annotated[str, Field(..., description="Unique identifier for the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient", examples=["Hazel Grace"])]
    city: Annotated[str, Field(..., description="City where the patient resides", examples=["New York"])]
    age: Annotated[int, Field(..., gt=0, lt= 120, description="Age of the patient", examples=[30])]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs", examples=[1.75])]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg", examples=[70.2])]

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate Body Mass Index (BMI)"""
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        """Determine the health verdict based on BMI"""
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"
        
class UpdatePatient(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description="Name of the patient", examples=["Hazel Grace"])]
    city: Annotated[Optional[str], Field(default=None, description="City where the patient resides", examples=["New York"])]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt= 120, description="Age of the patient", examples=[30])]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None, description="Gender of the patient")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="Height of the patient in mtrs", examples=[1.75])]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="Weight of the patient in kg", examples=[70.2])]


def load_patient_data():
    with open("data/patient_details.json", "r") as file:
        data = json.load(file)
    return data

def save_patient_data(data):
    with open("data/patient_details.json", "w") as file:
        json.dump(data, file)