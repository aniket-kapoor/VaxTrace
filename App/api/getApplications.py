from fastapi import APIRouter ,Depends,HTTPException,status,UploadFile , File
from ..schemas.patient import PatientIn
from sqlalchemy.ext.asyncio import AsyncSession
from ..core import database
from ..services import dependency
from ..schemas.application import PatientApplicationResponse
import uuid

from ..services.getApplications import get_patient_applications_service , verify_patient_application , check_my_application_services
from ..model.patient_mod import Patient , ApplicationStatus



router = APIRouter(
    tags=["Workers"]
)

@router.get("/patients/selfRegistration/applications"  , response_model=list[PatientApplicationResponse])

async def get_patient_applications(db: AsyncSession = Depends(database.get_db),
                                   current_user = Depends(dependency.allow_worker)):
    
  return await get_patient_applications_service(db )



@router.patch("/verify/application" )

async def verify_application(db: AsyncSession = Depends(database.get_db),
                              status=ApplicationStatus,
                              patient_id=uuid.UUID,
                              current_user = Depends(dependency.allow_worker)
                             ):
  return await verify_patient_application(db , status , patient_id)




@router.get("/check/application/status")

async def check_my_applications(db: AsyncSession = Depends(database.get_db),
                                parent_contact=str,
                                current_user = Depends(dependency.allow_parent)):
  
 return await check_my_application_services(db, parent_contact)