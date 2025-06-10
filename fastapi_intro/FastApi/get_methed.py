# Import necessary modules from FastAPI and standard libraries
from fastapi import FastAPI, Path, HTTPException, Query  # Import FastAPI, path/query parameter handling, and exception handling
import uvicorn  # For running the server
import json  # For reading JSON files

# Create FastAPI app instance
app = FastAPI()

# Function to load patient data from a JSON file
def load_data():
    """Load data from a JSON file."""
    # Open and read the patients.json file
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

# Root endpoint: returns a welcome message
@app.get("/")
def home():
    return {"message": "patient management system"}

# About endpoint: provides information about the system
@app.get("/about")
def about():
    return {"message": "This is a patient management system built with FastAPI."}

# View endpoint: returns all patient data
@app.get("/view")
def view():
    """View all patients."""
    data = load_data()
    return data

# View patient endpoint: returns data for a specific patient by ID
@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient IN the database", example="P005")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    # Raise 404 error if patient not found
    raise HTTPException(status_code=404, detail="Patient not found")

# Sort patients endpoint: returns sorted patient data by a given field and order
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort patients by 'Height', 'Weight', or 'BMI'"),
    order: str = Query("asc", description="Order of sorting: 'asc' for ascending, 'desc' for descending")
):
    valid_fields = ["Height", "Weight", "BMI"]  # Allowed fields for sorting

    # Validate sort_by field
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {valid_fields}")
    # Validate order value
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'desc'")

    data = load_data()  # Load patient data
    sort_oder = True if order == "desc" else False  # Determine sorting order
    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),  # Default to 0 if the key is not found
        reverse=sort_oder
    )
    return sorted_data

# Run the FastAPI app using uvicorn server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)