from fastapi import APIRouter ,Depends,HTTPException,status,UploadFile , File
from ..schemas.patient import PatientIn
from sqlalchemy.ext.asyncio import AsyncSession
from ..core import database
from ..services import dependency
from ..schemas.application import PatientApplicationResponse

from ..services.getApplications import get_patient_applications_service
from ..model.patient_mod import Patient , ApplicationStatus



router = APIRouter(
    tags=["Workers"]
)

@router.get("/patients/selfRegistration/applications"  , response_model=list[PatientApplicationResponse])

async def get_patient_applications(db: AsyncSession = Depends(database.get_db),
                                   status=ApplicationStatus.PROCESSING,
                                   current_user = Depends(dependency.allow_worker)):
    
  return await get_patient_applications_service(db , status)