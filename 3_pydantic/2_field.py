from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict,Optional, Annotated

class Patient(BaseModel):
    name : str = Field(max_length=7,default="AAAAA")
    age : Annotated[int, Field(ge=0,le=100,default=18,description="The age should be between 0 and 100",examples=24)]
    email : EmailStr
    history_link : AnyUrl
    tests : List[str] = Field(max_length=3, description=" You cannot include more then 3 elements")
    result : Annotated[Dict[str,str],Field(description="This is the list of the test performed :")]
    history :Optional[str]=None


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
    "email": "aa@gmail.com",
    "history_link" : "http://history.com",
    "tests": ["malaria", "typhoide", "bp_level"],
    "result": {"malaria": "positive", "typhoide": "negative", "bp_level": "120"},
    
}

patient1 = Patient(**patient_dict)

show(patient1)