from fastapi import FastAPI
from pydantic import BaseModel,Field, computed_field
from fastapi.responses import JSONResponse
from typing import Annotated
import pickle
import pandas as pd

with open("model.pkl1",'rb') as f:
   model =  pickle.load(f)

app=FastAPI()

# Tier 1 Cities (Major Metros)
tier1_cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi"]

# Tier 2 Cities (Secondary Urban Centers)
tier2_cities = [
    "Faisalabad",
    "Multan",
    "Peshawar",
    "Quetta",
    "Gujranwala",
    "Sialkot",
    "Hyderabad"
]

class pyd_model(BaseModel):
    age  : Annotated[int, Field(..., gt=0,examples=['22'])]
    weight : Annotated[float, Field(..., gt=10,le=120, description="The weight should be in kg",examples=['50'])]
    height : Annotated[float, Field(..., gt=1, le=8,description="The height shoud be in feets and inches",examples=['5.8'])]
    income_lpa:Annotated[float,Field(...,ge=0,description="The income should be in dollars",examples=["500"])]
    smoker:Annotated[bool,Field(...,description="The smoker shoub be yas or no",examples=[False])]
    city:Annotated[str,Field(..., description='The city shoud be from Pakistan', examples=['Peshawar'])]
    occupation:Annotated[str,Field(...,description=" the occupation is you profesional",examples=['Teacher'])]

    #bmi,lifestyle_risk,age_group,city_tier
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight/self.height**2
        return bmi
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return  "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
         if self.city in tier1_cities:
            return 1
         elif self.city in tier2_cities:
            return 2
         else:
            return 3
       
@app.post("/predict")
def prediction(data : pyd_model):

    input = pd.DataFrame([{
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }])
    ohe = model.named_steps["preprocessor"].named_transformers_["cat"]
    print("Expected categories:", ohe.categories_)

    output = model.predict(input)[0]
    return JSONResponse(status_code=201,content={"predicted_category":output})