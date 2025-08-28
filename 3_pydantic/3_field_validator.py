from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict,Optional, Annotated

class Patient(BaseModel):
    name : str 
    age :int
    email : EmailStr
    history_link : AnyUrl
    tests : List[str] 
    result : Dict[str,str]
    history :Optional[str]=None

    @field_validator("email")
    @classmethod
    def field_validation(cls, value):
        valid = ['icc.com',"gik.com"]
        domain = value.split('@')[-1]
        if domain not in valid:
            raise ValueError("Wrong entry")
        
        return domain
    
    @field_validator('name')
    @classmethod
    def transform(cls, value):
        name = value.upper()
        return name


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
    "age": 15,
    "email": "aa@gik.com",
    "history_link" : "http://history.com",
    "tests": ["malaria", "typhoide", "bp_level"],
    "result": {"malaria": "positive", "typhoide": "negative", "bp_level": "120"},
    
}

patient1 = Patient(**patient_dict)

show(patient1)