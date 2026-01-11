from fastapi import APIRouter ,Depends,HTTPException,status
from ..schemas import user
from ..security import hashing
import uuid

from ..services import dependency
from ..core import database
from ..services.pat_plan_service import get_patient_vaccine_plan
from ..services.pat_plan_service import update_vaccine_status_with_audit
from ..schemas.patient import PatientVaccinePlanOut, VaccineStatusUpdateIn

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


@router.put(
    "/plan/{plan_id}/confirm",
    summary="Confirm vaccination and store audit log"
)
async def confirm_vaccine(
    plan_id: uuid.UUID,
    payload: VaccineStatusUpdateIn,
    db: AsyncSession = Depends(database.get_db),
    current_user = Depends(dependency.allow_worker)
):
    plan = await update_vaccine_status_with_audit(
        db=db,
        plan_id=plan_id,
        new_status=payload.status,
        worker_id=current_user.id,
        confirm=payload.confirm
    )

    return {
        "message": "Vaccination status updated successfully",
        "plan_id": plan.id,
        "status": plan.status,
        "verified_by": current_user.id,
        "verified_at": plan.verified_at
    }




