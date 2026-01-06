from pydantic import BaseModel, Field , field_validator
from typing import Optional
from datetime import date
import re


class PatientIn(BaseModel):
    name:str
    gender:str
    dob:date=Field(...,description="Patient's date of birth")
    parent_contact:str=Field(...,description="Enter parent's phone number")
    state: str = Field(..., example="Punjab")
    district: str = Field(..., example="Amritsar")
    city_or_village: Optional[str] = Field(None, example="Majitha")
    pincode: Optional[str] = Field(None, example="143001")
    Address:str=Field(None)

    @field_validator("dob")
    @classmethod
    def dob_must_be_in_past(cls, value: date):
        if value >= date.today():
            raise ValueError("Date of birth must be in the past")
        return value
    
    @field_validator("parent_contact")
    @classmethod
    def validate_phone_number(cls, value:str):
        pattern = r"^\+[1-9]\d{1,14}$"  # E.164 format
        if not re.match(pattern, value):
            raise ValueError("Invalid phone number format. Use E.164 format like +919876543210")
        return value
    
class PatientResponse(BaseModel):
    name:str
    gender:str
    dob:date=Field(...,description="Patient's date of birth")
    Address:str=Field(None)
    

         
       

  