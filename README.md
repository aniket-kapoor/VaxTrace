# 🏥🛡️ VaxTrace Backend

The core engine behind **VaxTrace**, a high-performance, asynchronous REST API built with **FastAPI**.  
This backend serves as the **single source of truth** for lifetime vaccination records, managing complex scheduling logic, role-based security, and secure document handling.

---

## 🚀 Key Features

- **Asynchronous API**  
  Built with FastAPI for high-concurrency and low-latency performance.

- **Role-Based Access Control (RBAC)**  
  Secure endpoints with JWT-based authentication, differentiating between Parents/Guardians and Verified Healthcare Workers.

- **Automated Vaccine Scheduling**  
  Automatically generates vaccination timelines based on a patient's Date of Birth (DOB).

- **Relational Data Integrity**  
  Powered by PostgreSQL with normalized schemas to ensure consistency across lifetime records.

- **Cloud Document Management**  
  Integrated with Cloudinary for secure storage of medical verification documents.

- **Audit Logging**  
  Comprehensive tracking of status updates—knowing exactly who updated a record and when.

---

## 🛠️ Tech Stack

| Component   | Technology |
|------------|-----------|
| Language   | Python 3.10+ |
| Framework  | FastAPI |
| Database   | PostgreSQL |
| ORM        | SQLAlchemy  |
| Auth       | JWT (JSON Web Tokens) & Passlib |
| Storage    | Cloudinary API |
| Deployment | Render  |

---

## 🏗️ Architecture Overview

The backend follows a **modular service-oriented architecture**:

- **Models**  
  Define the database schema (Patients, Vaccines, Records, Users).

- **Schemas (Pydantic)**  
  Data validation and serialization.

- **Routes**  
  Endpoints for Authentication, Patient Management, and Vaccination Tracking.

- **Middleware**  
  Handling CORS, Authentication, and Logging.

---

## 🔧 Installation & Setup

### 1️⃣ Clone the Repository


```bash
git clone https://github.com/aniket-kapoor/VaxTrace
cd vaxtrace-backend
2️⃣ Set Up a Virtual Environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Environment Variables

Create a .env file in the root directory and add your credentials:

DATABASE_URL=postgresql://user:password@localhost/vaxtrace
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256

CLOUDINARY_CLOUD_NAME=your_name
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret

5️⃣ Run the Server
uvicorn main:app --reload








