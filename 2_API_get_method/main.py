from fastapi import FastAPI, HTTPException, Path, Query
import json

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Welcome to Patient Management App"}

@app.get("/about")
def about():
    return {"message":" We are here to maintain the handling of patient for better Treatement"}

def load_data():
     with open('patient.json','r') as f:
         data = json.load(f)

     return data
    
@app.get("/view")
def view():
    data = load_data()

    return data

@app.get("/patient/{patient_id}")
def patient(patient_id : str = Path(..., description = "Patient id is required :", example = "P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code = 404, detail = "patient not found")

@app.get("/sort")
def sort(sort_by:str = Query(..., description = "Sort_by is required in weight,height and bmi", example = "weight"), 
         order:str = Query('asc',description = "order is option, by default it is asc. You cab choose from asc or desc")):
    
     validation_field = ['weight', 'height', 'bmi']
     if sort_by not in validation_field:
         raise HTTPException(status_code= 400, description= "WRong entry")
     if order not in ['asc','desc']:
         raise HTTPException(status_code= 400, description=" Not in asc and desc")
     
     data = load_data()
    
     order_by = True if order =='desc' else False

     sort_data = sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=order_by)

     return sort_data 