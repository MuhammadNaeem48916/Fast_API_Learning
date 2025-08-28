from pydantic import BaseModel
from typing import List, Dict, Optional

class Patient(BaseModel):
    name : str
    age : int
    tests : List[str]
    result : Dict[str,str]
    history : Optional[str] = 23



def show(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.tests)
    print(patient.result)
    print(patient.history)

patient_dict = {
    "name": "Arsalan",
    "age": 15,
    "tests": ["malaria", "typhoide", "bp_level"],
    "result": {"malaria": "positive", "typhoide": "negative", "bp_level": "120"},
    
}

patient1 = Patient(**patient_dict)

show(patient1)

