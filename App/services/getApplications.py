from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..model.patient_mod import Patient , ApplicationStatus
from fastapi import HTTPException , status
from sqlalchemy.orm import selectinload



async def get_patient_applications_service( db: AsyncSession, status:ApplicationStatus.PROCESSING):

    result = await db.execute(
    select(Patient)
    .options(selectinload(Patient.documents)) 
    .where(Patient.application_status == status)
    .order_by(Patient.created_at.asc())   #Patient.application_status => to select the specific column in query
    )

    applications = result.scalars().all()

    if not applications:
        raise HTTPException(status_code=404 , detail="No pending applications!!")

    return applications