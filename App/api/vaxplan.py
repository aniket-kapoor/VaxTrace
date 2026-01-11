from fastapi import APIRouter ,Depends,HTTPException,status
from ..schemas import user
from ..security import hashing
import uuid

from ..services import dependency
from ..core import database
from ..services.pat_plan_service import get_patient_vaccine_plan
from ..schemas.patient import PatientVaccinePlanOut

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.concurrency import run_in_threadpool
# Import your models and schemas...

router = APIRouter(tags=['Workers'])

@router.get('/get/patients/{patient_id}/plan' , response_model=PatientVaccinePlanOut)

async def get_plan(patient_id: uuid.UUID,
                   db: AsyncSession = Depends(database.get_db),
                   current_user = Depends(dependency.allow_worker)
                   ):
    
    data= await get_patient_vaccine_plan(db, patient_id )

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    return data



