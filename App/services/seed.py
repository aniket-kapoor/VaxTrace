from sqlalchemy.orm import Session
from sqlalchemy import select
from ..model.vax_master import Vaccine
from ..model.vax_schedule  import VaccineScheduleMaster
 # Adjust imports to your file structure


def seed_vaccine_data(session: Session):
    """Sync function to be run inside a run_sync block"""
    
    # Check if data already exists to avoid duplicates
    existing_vax = session.execute(select(Vaccine).limit(1)).scalar()
    if existing_vax:
        print("Data already exists, skipping seed.")
        return

    # Define Dummy Data
    bcg = Vaccine(
        vaccine_code="BCG",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=0, max_age_days=15, is_booster=False)
        ]
    )

    hep_b = Vaccine(
        vaccine_code="HEP-B",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=0, max_age_days=1, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=30, max_age_days=60, is_booster=False)
        ]
    )

    session.add_all([bcg, hep_b])
    print("Dummy data seeded!")