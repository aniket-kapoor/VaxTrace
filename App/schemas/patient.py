from pydantic import BaseModel, Field , field_validator
from fastapi import Form
from typing import Optional, List
from datetime import date
import re
import uuid
from enum import Enum


class PatientIn(BaseModel):
    name:str
    gender:str
    dob:date=Field(...,description="Patient's date of birth")
    father_name:str=Field(...,description="Father's name")
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
    
    
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        gender: str = Form(...),
        dob: date = Form(..., description="Patient's date of birth"),
        father_name: str = Form(..., description="Father's name"),
        parent_contact: str = Form(..., description="Enter parent's phone number"),
        state: str = Form(...),
        district: str = Form(...),
        city_or_village: Optional[str] = Form(None),
        pincode: Optional[str] = Form(None),
        Address: Optional[str] = Form(None),
    ) -> "PatientIn":
        return cls(
            name=name,
            gender=gender,
            dob=dob,
            father_name=father_name,
            parent_contact=parent_contact,
            state=state,
            district=district,
            city_or_village=city_or_village,
            pincode=pincode,
            Address=Address,
        )
    



    
class PatientResponse(BaseModel):
    name:str
    gender:str
    dob:date=Field(...,description="Patient's date of birth")
    Address:str=Field(None)

class DocumentUploadResponse(BaseModel):
    id:uuid.UUID
    document_type:str
    

class PatientOnboardResponse(BaseModel):
    patient: PatientResponse
    dob_document: DocumentUploadResponse






class VaccineStatusOut(BaseModel):
    vaccine_name: str
    dose_number: int
    due_date: date
    administered_date:Optional[date] = None
    status: str
    plan_id:uuid.UUID

class PatientVaccinePlanOut(BaseModel):
    patient_id: uuid.UUID
    name: str
    gender: str
    address: str
    vaccines:List[VaccineStatusOut]

class VaccineStatus(str, Enum):
    COMPLETED = "COMPLETED"
    MISSED = "MISSED"

class VaccineStatusUpdateIn(BaseModel):
    update_date: Optional[date] = None
    new_status:str
    confirm:bool










    

         
       

  