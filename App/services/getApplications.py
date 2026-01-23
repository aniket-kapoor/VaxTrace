from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..model.patient_mod import Patient , ApplicationStatus
from fastapi import HTTPException , status
from sqlalchemy.orm import selectinload
from .pat_plan_service import generate_patient_vaccine_plan



async def get_patient_applications_service( db: AsyncSession):

    result = await db.execute(
    select(Patient)
    .options(selectinload(Patient.documents)) 
    .where(Patient.application_status == ApplicationStatus.PROCESSING)
    .order_by(Patient.created_at.asc())   #Patient.application_status => to select the specific column in query
    )

    applications = result.scalars().all()

    if not applications:
        raise HTTPException(status_code=404 , detail="No pending applications!!")

    return applications


async def verify_patient_application( db: AsyncSession, 
                                     status:ApplicationStatus,
                                     patient_id):
    
    query= await db.execute(select(Patient)
                            .where(Patient.id==patient_id))
    
    patient=query.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=404 , detail="Error occured while updating")

    #update the status
    patient.application_status=status

    await db.commit()   #Keep in mind to commit the changes
    await db.refresh(patient)

    await generate_patient_vaccine_plan(db=db,
                                        patient_id=patient.id,
                                        birth_date=patient.dob
                                    )





    return {"application_status":patient.application_status,
            }



async def check_my_application_services(db: AsyncSession , parent_contact):

    query= await db.execute(select(Patient)
                            .where(Patient.parent_contact==parent_contact)
                            .order_by(Patient.created_at.desc())
                            )
    
    applications = query.scalars().all()

    if not applications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have not reistered any child yet!!")
    
    return applications



