# KPA Backend Developer Assignment

This project contains the backend API implementation for the KPA assignment. It is built using FastAPI and connects to a PostgreSQL database, with full support for the two specified form types.

---

## 🚀 Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy with Alembic for migrations
- **Validation**: Pydantic for strict data validation
- **Server**: Uvicorn
- **Containerization**: Docker & Docker Compose

---

## ✨ Bonus Features Implemented

- **Full Dockerization**: The entire application stack (API, Database) can be launched with a single `docker-compose up` command.
- **Strict Input Validation**: Pydantic schemas enforce required fields, data types, and custom rules (e.g., dates cannot be in the future).
- **Environment Configuration**: Securely manages database credentials and other settings using a `.env` file.
- **Interactive API Docs**: Automatic Swagger UI and ReDoc documentation is available at `/docs` and `/redoc`.

---

## Implemented APIs

The following endpoints from the Postman collection have been implemented and are fully functional:

1.  **`POST /api/forms/wheel-specifications`**
    -   **Description**: Adds a new wheel specification form to the database.
    -   **Status Code**: `201 Created`
    -   **Response**: Returns a success message and submission status, matching the contract.

2.  **`POST /api/forms/bogie-checksheet`**
    -   **Description**: Adds a new bogie checksheet form, handling multiple nested JSON objects.
    -   **Status Code**: `201 Created`
    -   **Response**: Returns a success message and submission status, matching the contract.

3.  **`GET /api/forms/wheel-specifications`**
    -   **Description**: Retrieves a list of wheel specification forms.
    -   **Filtering**: Supports query parameters `formNumber`, `submittedBy`, and `submittedDate`.
    -   **Response**: Returns a list of matching forms with an abbreviated `fields` object, per the contract.

---

## ⚙️ Project Setup and Usage

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1.  **Clone the repository:**
    ```
    git clone https://github.com/Aftab073/kpa_backend
    cd kpa_backend
    ```

2.  **Set up environment variables:**
    -   Rename the `.env.example` file to `.env`.
    -   (Optional) Modify the PostgreSQL credentials if needed. The defaults are configured to work with Docker Compose.

3.  **Launch the application using Docker Compose:**
    ```
    docker-compose up --build -d
    ```

4.  **The API is now running!**
    -   **API URL**: `http://127.0.0.1:8000`
    -   **Interactive Docs (Swagger)**: `http://127.0.0.1:8000/docs`
    -   **Database Admin (pgAdmin)**: `http://localhost:5050` (Login with credentials from `.env` file)

### Running Database Migrations

The initial Docker Compose setup runs the migrations automatically. To run them manually:
Get the container ID for the api service
docker-compose ps

Execute the alembic command inside the container
docker exec -it <container_id> alembic upgrade head

### Running Without Docker (Optional)

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows


2. Install dependencies:

pip install -r requirements.txt

3. Set environment variables via .env

4. Run the API:
uvicorn app.main:app --reload
