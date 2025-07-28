from fastapi import FastAPI
from .api.endpoints import forms
from .database import Base, engine

# This line creates the tables if they don't exist. 
# In a production app, you'd use Alembic.
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPA Form Data API",
    description="API for managing KPA form data, built for a backend assignment.",
    version="1.0.0"
)

app.include_router(forms.router, prefix="/api/forms", tags=["Forms"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the KPA Form Data API"}
