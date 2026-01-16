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
    # bcg = Vaccine(
    #     vaccine_code="BCG",
    #     schedules=[
    #         VaccineScheduleMaster(dose_number=1, min_age_days=0, max_age_days=15, is_booster=False)
    #     ]
    # )

    vaccines = [

    # BCG
    Vaccine(
        vaccine_code="BCG",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=0, max_age_days=15, is_booster=False)
        ]
    ),

    # OPV
    Vaccine(
        vaccine_code="OPV",
        schedules=[
            VaccineScheduleMaster(dose_number=0, min_age_days=0, max_age_days=15, is_booster=False),
            VaccineScheduleMaster(dose_number=1, min_age_days=42, max_age_days=56, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=70, max_age_days=84, is_booster=False),
            VaccineScheduleMaster(dose_number=3, min_age_days=98, max_age_days=112, is_booster=False),
            VaccineScheduleMaster(dose_number=4, min_age_days=270, max_age_days=300, is_booster=True),
            VaccineScheduleMaster(dose_number=5, min_age_days=1825, max_age_days=2190, is_booster=True)
        ]
    ),

    # Hepatitis B
    Vaccine(
        vaccine_code="HEPATITIS_B",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=0, max_age_days=15, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=42, max_age_days=56, is_booster=False),
            VaccineScheduleMaster(dose_number=3, min_age_days=98, max_age_days=180, is_booster=False)
        ]
    ),

    # DTP / DTwP / DTaP
    Vaccine(
        vaccine_code="DTP",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=42, max_age_days=56, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=70, max_age_days=84, is_booster=False),
            VaccineScheduleMaster(dose_number=3, min_age_days=98, max_age_days=112, is_booster=False),
            VaccineScheduleMaster(dose_number=4, min_age_days=450, max_age_days=540, is_booster=True),
            VaccineScheduleMaster(dose_number=5, min_age_days=1825, max_age_days=2190, is_booster=True)
        ]
    ),

    # Hib
    Vaccine(
        vaccine_code="HIB",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=42, max_age_days=56, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=70, max_age_days=84, is_booster=False),
            VaccineScheduleMaster(dose_number=3, min_age_days=98, max_age_days=112, is_booster=False),
            VaccineScheduleMaster(dose_number=4, min_age_days=450, max_age_days=540, is_booster=True)
        ]
    ),

    # IPV
    Vaccine(
        vaccine_code="IPV",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=42, max_age_days=56, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=98, max_age_days=112, is_booster=False),
            VaccineScheduleMaster(dose_number=3, min_age_days=450, max_age_days=540, is_booster=True)
        ]
    ),

    # Pneumococcal (PCV)
    Vaccine(
        vaccine_code="PCV",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=42, max_age_days=56, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=70, max_age_days=84, is_booster=False),
            VaccineScheduleMaster(dose_number=3, min_age_days=98, max_age_days=112, is_booster=False),
            VaccineScheduleMaster(dose_number=4, min_age_days=270, max_age_days=300, is_booster=True)
        ]
    ),

    # Rotavirus
    Vaccine(
        vaccine_code="ROTAVIRUS",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=42, max_age_days=56, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=70, max_age_days=84, is_booster=False),
            VaccineScheduleMaster(dose_number=3, min_age_days=98, max_age_days=112, is_booster=False)
        ]
    ),

    # Measles
    Vaccine(
        vaccine_code="MEASLES",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=270, max_age_days=300, is_booster=False)
        ]
    ),

    # MMR
    Vaccine(
        vaccine_code="MMR",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=450, max_age_days=540, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=1825, max_age_days=2190, is_booster=True)
        ]
    ),

    # Varicella
    Vaccine(
        vaccine_code="VARICELLA",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=450, max_age_days=540, is_booster=False)
        ]
    ),

    # Hepatitis A
    Vaccine(
        vaccine_code="HEPATITIS_A",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=540, max_age_days=720, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=720, max_age_days=900, is_booster=True)
        ]
    ),

    # Typhoid
    Vaccine(
        vaccine_code="TYPHOID",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=730, max_age_days=900, is_booster=False)
        ]
    ),

    # Tdap / Td (10 years)
    Vaccine(
        vaccine_code="TDAP",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=3650, max_age_days=4015, is_booster=True)
        ]
    ),

    # HPV (girls)
    Vaccine(
        vaccine_code="HPV",
        schedules=[
            VaccineScheduleMaster(dose_number=1, min_age_days=3650, max_age_days=4015, is_booster=False),
            VaccineScheduleMaster(dose_number=2, min_age_days=3710, max_age_days=4080, is_booster=False),
            VaccineScheduleMaster(dose_number=3, min_age_days=3830, max_age_days=4260, is_booster=False)
        ]
    )
]

    session.add_all(vaccines)
    session.commit()
    print("Dummy data seeded!")