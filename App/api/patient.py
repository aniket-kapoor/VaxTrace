from fastapi import APIRouter ,Depends,HTTPException,status,UploadFile , File
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from ..schemas.patient import PatientIn, PatientOnboardResponse , PatientResponse

from ..services import dependency
from ..core import database
from ..crud.patient  import (
    create_patient_with_dob_document,
    get_patient_by_id,
    deactivate_patient
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.post("/createPatient",status_code=status.HTTP_201_CREATED, response_model=PatientOnboardResponse)

async def create_patient_route(patient_data:PatientIn = Depends(PatientIn.as_form),
                         dob_document: UploadFile = File(...),
                         db: AsyncSession = Depends(database.get_db),
                         current_user = Depends(dependency.allow_worker)
                         ):
     return await create_patient_with_dob_document(db, patient_data , dob_document)



@router.get("/getPatient/{patient_id}" , response_model=PatientResponse)
async def get_patient(patient_id: uuid.UUID ,
                db: AsyncSession = Depends(database.get_db),
                
                ):
     
     patient=await get_patient_by_id(db,patient_id)

     if not patient:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Patient Does not Exist"
                              )
     
     return patient



@router.delete("/{patient_id}")
async def deactivate_patient_route(
    patient_id: uuid.UUID,
    db: AsyncSession = Depends(database.get_db),
    current_user = Depends(dependency.allow_worker)
):
    patient=await deactivate_patient(db,patient_id)

    if not patient:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Patient Does not Exist"
                              )
    return patient




     
    


