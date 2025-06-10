# Import necessary modules from FastAPI, Pydantic, and standard libraries
from fastapi import FastAPI, Path, HTTPException, Query 
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Literal
import json
import uvicorn

# Create FastAPI app instance
app = FastAPI()

# Function to load patient data from a JSON file
def load_data():
    """Load data from a JSON file."""
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

# Function to save patient data to a JSON file
def save_data(data):
    """Save data to a JSON file."""
    with open('patients.json', 'w') as f:
        json.dump(data, f)

# Define the Patient model
class Patient(BaseModel):
    """Model for patient data."""
    id: str = Field(..., description="ID of the patient in the database", example="P001")
    name: str = Field(..., description="Name of patient")
    city: str = Field(..., description="City of patient living")
    age: int = Field(..., gt=0, lt=120, description="Age of the patient")
    gender: Literal["Male", "Female", "Other"] = Field(..., description="Gender of the patient")
    height: float = Field(..., description="Height of the patient in meters")
    weight: float = Field(..., description="Weight of the patient in kilograms")

    @computed_field
    @property
    def bmi(self) -> float:
        """
        Calculates the Body Mass Index (BMI) based on weight and height.
        BMI = weight (kg) / (height (m))^2
        """
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        """
        Provides a health verdict based on BMI.
        """
        if self.bmi < 18:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

# Root endpoint: returns a welcome message
@app.get("/")
def home():
    """Welcome message for the patient management system."""
    return {"message": "Patient management system"}

# About endpoint: provides information about the system
@app.get("/about")
def about():
    """Information about the patient management system."""
    return {"message": "This is a patient management system built with FastAPI."}

# View endpoint: returns all patient data
@app.get("/view")
def view():
    """View all patients."""
    data = load_data()
    return data

# View patient endpoint: returns data for a specific patient by ID
@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient in the database", example="P005")):
    """View details of a specific patient by ID."""
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

# Sort patients endpoint: returns sorted patient data by a given field and order
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort patients by 'Height', 'Weight', or 'BMI'"),
    order: str = Query("asc", description="Order of sorting: 'asc' for ascending, 'desc' for descending")
):
    """Sort patients by a specified field and order."""
    valid_fields = ["Height", "Weight", "BMI"]

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'desc'")

    data = load_data()
    sort_order = True if order == "desc" else False
    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=sort_order
    )
    return sorted_data

# Create patient endpoint: adds a new patient to the database
@app.post('/create')
def create_patient(patient: Patient):
    """Create a new patient record."""
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

# Run the FastAPI app using uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)