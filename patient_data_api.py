from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse

from utils import load_patient_data, save_patient_data
from utils import Patient, UpdatePatient


app = FastAPI()

@app.get("/API INFO")
def info():
    return {
        "name": "Patient Data API",
        "version": "1.0.0",
        "description": "API to handle patient data."
    }

@app.get("/view_patients_data")
def view():
    data = load_patient_data()
    return {
        "status": "success",
        "data": data
    }

@app.get("/patients/{patient_id}")
def get_patient(
    patient_id: str = Path(..., description="The ID of the patient in the database", example="P001")
    ):
    # Load patient data
    data = load_patient_data()
    if patient_id in data:
        return {
            "status": "success",
            "data": data[patient_id]
        }
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort_patients")
def sort_patients(
    sort_by: str = Query(..., description="Sort patient data based on height, weight, or bmi", example="height"),
    order: str = Query(..., description="Order of sorting: asc or desc", example="asc")
    ):
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Select from {valid_fields}.")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'.")
    
    # Load patient data
    data = load_patient_data()

    # Sort data
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return {
        "status": "success",
        "data": sorted_data
    }

@app.post("/add_patient")
def add_patient(patient: Patient):
    # Load existing patient data
    data = load_patient_data()

    # Check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")

    # Add new patient data
    data[patient.id] = patient.model_dump(exclude={'id'})
    
    # Save updated data
    save_patient_data(data)

    return JSONResponse(status_code=201, content={"status": "success", "message": "Patient added successfully."})

@app.put("/update_patient/{patient_id}")
def update_patient(patient_id: str, update_data: UpdatePatient):
    # Load existing patient data
    data = load_patient_data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found.")
    
    existing_patient_info = data[patient_id]
    updated_patient_info = update_data.model_dump(exclude_unset=True)

    # Update patient data
    for key, value in updated_patient_info.items():
        if value is not None:
            existing_patient_info[key] = value
    
    existing_patient_info['id'] = patient_id
    pydantic_patient = Patient(**existing_patient_info)
    existing_patient_info = pydantic_patient.model_dump(exclude={'id'})
    data[patient_id] = existing_patient_info

    # Save updated data
    save_patient_data(data)

    return JSONResponse(status_code=200, content={"status": "success", "message": "Patient updated successfully."})

@app.delete("/delete_patient/{patient_id}")
def delete_patient(patient_id: str):
    # Load existing patient data
    data = load_patient_data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found.")
    
    # Delete patient data
    del data[patient_id]

    # Save updated data
    save_patient_data(data)

    return JSONResponse(status_code=200, content={"status": "success", "message": "Patient deleted successfully."})