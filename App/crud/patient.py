from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select
import uuid
from ..model.patient_mod import Patient

# from ..services.pat_plan_service import generate_patient_vaccine_plan
from ..services.pat_plan_service import generate_patient_vaccine_plan


from ..schemas.patient import PatientIn
from ..core import database


async def create_patient(
                db: AsyncSession,
                patient_data:PatientIn 
                ) -> Patient:
    
    patient=Patient(**patient_data.model_dump())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)

    await generate_patient_vaccine_plan(db=db,
                                patient_id=patient.id,
                                birth_date=patient.dob
                             )


    return patient



async def get_patient_by_id(
    db: AsyncSession,
    patient_id: uuid.UUID
     ) -> Patient | None:

    stmt = select(Patient).where(Patient.id == patient_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()



async def deactivate_patient(
    db: AsyncSession,
    patient_id: uuid.UUID
   ) -> Patient:
    
    stmt = select(Patient).where(Patient.id == patient_id)
    result = await db.execute(stmt)
    patient=result.scalar_one_or_none()

    patient.is_active = False
    await db.commit()
    await db.refresh(patient)
    return patient
    

