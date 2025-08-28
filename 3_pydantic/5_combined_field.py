from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict,Optional

class Patient(BaseModel):
    name : str 
    age :int
    email : EmailStr
    history_link : AnyUrl
    tests : List[str] 
    result : Dict[str,str]
    history :Optional[str]=None

    @computed_field
    @property
    def name_age(self)->str:
        name_age =self.name + str(self.age)
        return name_age

 
def show(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.history_link)
    print(patient.tests)
    print(patient.result)
    print(patient.history)
    print(patient.name_age)

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

temp = patient1.model_dump()
print(temp)