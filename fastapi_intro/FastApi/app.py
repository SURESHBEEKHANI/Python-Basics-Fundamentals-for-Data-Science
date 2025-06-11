# Import necessary modules from FastAPI, Pydantic, and standard libraries
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
import uvicorn

# Initialize the FastAPI app
app = FastAPI()

# --------- Pydantic Models ---------
class Patient(BaseModel):
    """
    Schema for patient information.
    Includes fields for ID, name, city, age, gender, height, weight, and computed properties for BMI and health verdict.
    """
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kilograms')]

    @computed_field
    @property
    def bmi(self) -> float:
        """
        Calculate Body Mass Index (BMI).
        BMI = weight (kg) / (height (m))^2
        """
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        """
        Provide a health verdict based on BMI.
        """
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        return 'Obese'

class PatientUpdate(BaseModel):
    """
    Schema for updating patient information.
    Allows partial updates with optional fields.
    """
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

# --------- Utility Functions ---------
def load_data() -> dict:
    """
    Load patient data from a JSON file.
    """
    with open('patients.json', 'r') as f:
        return json.load(f)

def save_data(data: dict) -> None:
    """
    Save patient data to a JSON file.
    """
    with open('patients.json', 'w') as f:
        json.dump(data, f)

# --------- API Routes ---------
@app.get("/")
def hello():
    """
    Root endpoint: Welcome message for the API.
    """
    return {'message': 'Patient Management System API'}

@app.get('/about')
def about():
    """
    About endpoint: Provides information about the API.
    """
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    """
    View all patients in the database.
    """
    return load_data()

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    """
    View details of a specific patient by ID.
    """
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description='Sort on the basis of height, weight, or BMI'),
    order: str = Query('asc', description='Sort in ascending or descending order')
):
    """
    Sort patients by a specified field and order.
    """
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field. Select from {valid_fields}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order. Select between asc and desc')

    data = load_data()
    sorted_list = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=(order == 'desc')
    )
    return sorted_list

@app.post('/create')
def create_patient(patient: Patient):
    """
    Create a new patient record.
    """
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    """
    Update an existing patient's information.
    """
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_obj.model_dump(exclude=['id'])

    data[patient_id] = existing_patient_info
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    """
    Delete a patient record by ID.
    """
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})

# --------- Run the App ---------
if __name__ == "__main__":
    """
    Run the FastAPI app using uvicorn.
    """
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
# To run the app, use the command: uvicorn app:app --reload