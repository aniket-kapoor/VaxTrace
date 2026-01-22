from pydantic import BaseModel, Field , field_validator
from fastapi import Form
from typing import Optional, List
from datetime import date
import re
import uuid
import enum

class ApplicationStatus(str, enum.Enum):
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"

class ApplicationDocument(BaseModel):
    document_type:str
    file_path:str

    class Config:
        from_attributes = True

class PatientApplicationResponse(BaseModel):
    id:uuid.UUID
    name:str
    gender:str
    dob:date=Field(...,description="Patient's date of birth")
    father_name:str
    district:str
    pincode:str
    Address:str=Field(None)
    application_status:ApplicationStatus

    documents:list[ApplicationDocument]

    class Config:
        from_attributes = True

