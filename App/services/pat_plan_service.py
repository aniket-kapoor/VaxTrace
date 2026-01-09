from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from ..model.vax_schedule import VaccineScheduleMaster
from ..model.pat_vax_plan import PatientVaccinePlan


async def generate_patient_vaccine_plan(db:AsyncSession,
                                        patient_id,
                                        birth_date
                                    ):
    
    result= await db.execute(select(VaccineScheduleMaster))
    schedules=result.scalars().all()
    
    for schedule in schedules:
        due_date = birth_date + timedelta(days=schedule.min_age_days)

    plans=[]

    plan=PatientVaccinePlan(patient_id=patient_id,
                      vaccine_id=schedule.vaccine_id ,
                      dose_number=schedule.dose_number,
                      due_date=due_date  ,
                      status="PENDING"  ,
                      )
    
    plans.append(plan)
   
    #Bulk insert
    db.add_all(plans)
    await db.commit()

    