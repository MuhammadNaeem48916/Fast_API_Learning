from pydantic import BaseModel
from typing import List, Dict, Optional

class Address(BaseModel):
    village :str
    house_no : int

class Patient(BaseModel):
    name : str
    age : int
    history : Dict[str,str]
    address : Address

def show(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.history)
    print(patient.address)

address_dict ={
    "village":"xyz",
    "house_no":100
}
address1 = Address(**address_dict)

patient_dict = {
    "name":"Arsalan", 
    "age":22,
    "history":{"Malaria":"positive","BP":"Low"},
    "address":address1
    }

patient1 = Patient(**patient_dict)

show(patient1)

temp_dict = patient1.model_dump()
print(type(temp_dict),temp_dict)

temp_json =patient1.model_dump_json()
print(type(temp_json),temp_json)
