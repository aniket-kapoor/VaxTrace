from fastapi import APIRouter ,Depends,HTTPException,status,UploadFile , File
from ..schemas.patient import PatientIn
from sqlalchemy.ext.asyncio import AsyncSession
from ..core import database
from ..services import dependency

from ..crud.patient import self_registration_application_service



router = APIRouter(
    tags=["Parents"]
)

@router.post("/parent/patient/selfRegistration" )

async def self_registration_application(patient_data:PatientIn = Depends(PatientIn.as_form),
                                        dob_document: UploadFile = File(...),
                                        db: AsyncSession = Depends(database.get_db),
                                        current_user = Depends(dependency.allow_parent)
                                        ):
    
    return await self_registration_application_service(db, patient_data , dob_document)