from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, UploadFile, HTTPException
from sqlalchemy import select
import uuid , os 

from ..model.patient_mod import Patient 
from ..model.patientDocs import PatientDocuments

# from ..services.pat_plan_service import generate_patient_vaccine_plan
from ..services.pat_plan_service import generate_patient_vaccine_plan 
from ..services.uploadFiles import save_upload_file


from ..schemas.patient import PatientIn
from ..core import database


async def create_patient_with_dob_document(
                db: AsyncSession,
                patient_data ,
                dob_document
                ) -> Patient:
        
        file_path: str | None = None
    
        try:
            file_path = await save_upload_file(dob_document)
            
            patient=Patient(**patient_data.model_dump())
            db.add(patient)
            await db.flush()

            document=PatientDocuments(patient_id=patient.id,
                                    document_type="DOB_PROOF",
                                    file_path=file_path)
            db.add(document)

            await generate_patient_vaccine_plan(db=db,
                                        patient_id=patient.id,
                                        birth_date=patient.dob
                                    )
            
            await db.commit()
            await db.refresh(patient)
            await db.refresh(document)


            return {
            "patient": patient,
            "dob_document": document
             }



        except Exception as e:
                await db.rollback()

                # cleanup file if DB fails
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)

         

                raise HTTPException(
                    status_code=500,
                    detail=str(e)
                        )

            



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
    

