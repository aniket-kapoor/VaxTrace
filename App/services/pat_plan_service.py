from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from fastapi import HTTPException
import datetime

from datetime import datetime, timezone

from ..model.vax_auditlog import VaccineAuditLog
from ..model.vax_schedule import VaccineScheduleMaster
from ..model.pat_vax_plan import PatientVaccinePlan

from ..model.patient_mod import Patient
from ..model.vax_master import Vaccine


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



async def get_patient_vaccine_plan(db:AsyncSession,
                                   patient_id):
    
    query= (
        select(
            Patient.id,
            Patient.name,
            Patient.gender,
            Patient.Address,

            PatientVaccinePlan.id.label("plan_id"),
            Vaccine.vaccine_code.label("vaccine_name"),
            PatientVaccinePlan.dose_number,
            PatientVaccinePlan.due_date,
            PatientVaccinePlan.status,
        )
        .join(PatientVaccinePlan, Patient.id==PatientVaccinePlan.patient_id)
        .join(Vaccine, Vaccine.id==PatientVaccinePlan.vaccine_id)
        .where(Patient.id == patient_id)
        .order_by(PatientVaccinePlan.due_date)
    )
    
    result = await db.execute(query)

    rows=result.all()

    if not rows:
        return None
    
    # We need a nested response so
    patient_info = rows[0]
    vaccines=[]

    for row in rows:
        vaccines.append(
            {
            "vaccine_name": row.vaccine_name,
            "dose_number": row.dose_number,
            "due_date": row.due_date,
            "status": row.status,
            "plan_id": row.plan_id, 
        }
        )

        return {
        "patient_id": patient_info.id,
        "name": patient_info.name,
        "gender": patient_info.gender,
        "address": patient_info.Address,
        "vaccines": vaccines
    }



async def update_vaccine_status_with_audit(
    db:AsyncSession,
    new_date,
    plan_id,
    new_status,
    worker_id,
    confirm: bool
):
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail="Final confirmation required"
        )

    result = await db.execute(
        select(PatientVaccinePlan).where(
            PatientVaccinePlan.id == plan_id
        )
    )
    plan = result.scalar_one_or_none()

    if not plan:
        raise HTTPException(404, "Vaccine plan not found")

    if plan.status == "COMPLETED":
        raise HTTPException(
            status_code=409,
            detail="Vaccine already marked as completed"
        )

    old_status = plan.status

    #Update main table
    plan.status = new_status
    plan.verified_by_worker = worker_id
    plan.verified_at = datetime.now(timezone.utc)
    plan.administered_date=new_date

    # Create audit log
    audit_log = VaccineAuditLog(
        plan_id=plan.id,
        old_status=old_status,
        new_status=new_status,
        changed_by=worker_id
    )

    db.add(audit_log)

    await db.commit()
    await db.refresh(plan)

    return plan

    



    

    
    

    