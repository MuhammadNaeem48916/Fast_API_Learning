from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict,Optional

class Patient(BaseModel):
    name : str 
    age :int
    email : EmailStr
    history_link : AnyUrl
    tests : List[str] 
    result : Dict[str,str]
    history :Optional[str]=None

    @model_validator(mode='before')
    def model_validation(cls,values):
         print("The type of Value is :::", type(values))
         if values.get("age", 0) > 50 and "ECG" not in values.get("tests", []):
              raise ValueError("The ECG should be in the Tests")
         return values
    
    @model_validator(mode="after")
    def model_val(self):
         print(" The type of the sels is :",type(self))
         if self.age >40 and "ECG" not in self.tests:
              raise ValueError("The ECG should be in the Tests")
         
         return self

 
def show(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.history_link)
    print(patient.tests)
    print(patient.result)
    print(patient.history)

patient_dict = {
    "name": "Arsalan",
    "age": 4,
    "email": "aa@gik.com",
    "history_link" : "http://history.com",
    "tests": ["malaria", "typhoide", "bp_level"],
    "result": {"malaria": "positive", "typhoide": "negative", "bp_level": "120"},
    
}

patient1 = Patient(**patient_dict)

show(patient1)