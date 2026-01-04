from fastapi import APIRouter ,Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from ..schemas.patient import PatientIn

from ..services import dependency
from ..core import database
from ..crud.patient  import (
    create_patient,
    get_patient_by_id,
    deactivate_patient
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.post("/createPatient",status_code=status.HTTP_201_CREATED)

async def create_patient_route(patient_data:PatientIn,
                         db: AsyncSession = Depends(database.get_db),
                         current_user = Depends(dependency.allow_worker)
                         ):
     return await create_patient(db, patient_data)



@router.get("/getPatient/{patient_id}")
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




     
    


