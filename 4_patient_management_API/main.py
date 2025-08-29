from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional,Annotated

app = FastAPI()

class Patient(BaseModel):
     id : Annotated[str, Field(..., examples=["p001"])]
     name: Annotated[str, Field(..., examples=["AAA"])]
     age:  Annotated[int, Field(..., examples=[45])]
     gender: Annotated[str, Field(..., examples=["male"])]
     email: Annotated[EmailStr, Field(..., examples=["aaa@hj.com"])]
     phone: Annotated[str, Field(..., examples=["031XXXX"])]
     weight: Annotated[float, Field(..., examples=[30.2])]
     height: Annotated[float, Field(..., examples=[5.5])]
     tests: Annotated[List[str], Field(..., examples=[["a", "b"]])]
     results: Annotated[Dict[str,str], Field(..., examples=[{"a":"aaa","b":"bbb"}])]


     @computed_field
     @property
     def bmi(self) -> float:
          bmi = round(self.weight/self.height**2,2)
          return bmi
      
     @computed_field
     @property
     def verdict(self) -> str:
          if self.bmi < 18:
              return "underweight"
          if self.bmi < 25:
              return "Normal"
          if self.bmi > 25:
              return "Obese"
class PatientUpdate(BaseModel):
     id : Annotated[Optional[str], Field(None, examples=["p001"])]
     name: Annotated[Optional[str], Field(None, examples=["AAA"])]
     age:  Annotated[Optional[int], Field(None, examples=[45])]
     gender: Annotated[Optional[str], Field(None, examples=["male"])]
     email: Annotated[Optional[EmailStr], Field(None, examples=["aaa@hj.com"])]
     phone: Annotated[Optional[str], Field(None, examples=["031XXXX"])]
     weight: Annotated[Optional[float], Field(None, examples=[30.2])]
     height: Annotated[Optional[float], Field(None, examples=[5.5])]
     tests: Annotated[Optional[List[str]], Field(None, examples=[["a", "b"]])]
     results: Annotated[Optional[Dict[str,str]], Field(None, examples=[{"a":"aaa","b":"bbb"}])]

@app.get("/")
def start():
    return {"message":"Welcome to the Patient Management System"}

  
@app.get("/About/{patient_id}")
def about1(patient_id : str):

    greatings = f"hi {patient_id}, we welcome you to our Patient Managemet System:\n"
    doing = f"We do provide the facility of viewing, Craetibg, Editing and Deleting Patient from our system" 
    return (greatings,doing)

def load_data():
    with open("patient.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("patient.json","w") as f:
        json.dump(data,f)

@app.get("/view")
def show():
   data = load_data()

   return data

@app.get("/patient/{patient_id}")
def patient(patient_id:str = Path(..., description="The patieb=nt id should be unique ", example="p001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")

@app.post("/create")
def create(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail="patient already exist")
    
    data[patient.id]=patient.model_dump(exclude=['id'])

    save_data(data)

    return   JSONResponse(status_code=201,content={"message":"patient successfully created"}) 
                                

@app.put("/update/{patient_id}")
def update(patient_id :str, patient_update:PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="data not found")
    
    existing_data = data[patient_id]

    updated_data = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        existing_data[key]=value

    existing_data['id'] = patient_id

    pydanict_obj = Patient(**existing_data)

    existing_data = pydanict_obj.model_dump(exclude=['id'])

    data[patient_id]= existing_data

    save_data(data)

    return JSONResponse(status_code=201, content={"message":"Patient succesfully updated"})

@app.delete("/delete/{patient_id}")
def delete(patient_id:str = Path(..., description="give patient id to delete", example="p001")):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="data not found")
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=201, content={"message":"uccessfuly deleted"})