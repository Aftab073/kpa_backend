from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ... import schemas
from app import crud
from ...database import get_db

router = APIRouter()

@router.post("/wheel-specifications", response_model=schemas.form_schemas.WheelSpecificationPostResponse, status_code=status.HTTP_201_CREATED)
def add_wheel_specification(
    form: schemas.form_schemas.WheelSpecificationCreate, 
    db: Session = Depends(get_db)
):
    # Check if formNumber already exists
    existing_form = crud.crud_forms.get_wheel_specifications(db, formNumber=form.formNumber, submittedBy=None, submittedDate=None)
    if existing_form:
        raise HTTPException(status_code=400, detail="formNumber already exists")
    
    crud.crud_forms.create_wheel_specification(db=db, form=form)
    
    return {
        "success": True,
        "message": "Wheel specification submitted successfully.",
        "data": {
            "formNumber": form.formNumber,
            "submittedBy": form.sumittedBy,
            "submittedDate": form.submittedDate.isoformat(),
            "status": "Saved"
        }
    }


@router.post(
    "/bogie-checksheet",
    response_model=schemas.form_schemas.BogieChecksheetPostResponse,
    status_code=status.HTTP_201_CREATED
)
def add_bogie_checksheet(
    form: schemas.form_schemas.BogieChecksheetCreateForm,
    db: Session = Depends(get_db)
):
    existing_bogie_form = crud.crud_forms.get_bogie_checksheet_by_form_number(db, formNumber=form.formNumber)
    if existing_bogie_form:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Bogie checksheet with formNumber '{form.formNumber}' already exists."
        )    
    crud.crud_forms.create_bogie_checksheet(db=db, form=form)
    return {
        "success": True,
        "message": "Bogie checksheet submitted successfully.",
        "data": {
            "formNumber": form.formNumber,
            "inspectionBy": form.inspectionBy,
            "inspectionDate": form.inspectionDate.isoformat(),
            "status": "Saved"
        }
    }




@router.get("/wheel-specifications", response_model=schemas.form_schemas.WheelSpecificationGetResponse)
def read_wheel_specifications(
    formNumber: str | None = None,
    submittedBy: str | None = None,
    submittedDate: date | None = None,
    db: Session = Depends(get_db)
):
    forms = crud.crud_forms.get_wheel_specifications(db, formNumber, submittedBy, submittedDate)
    
    # Format the response to match the Postman collection
    response_data = []
    for form in forms:
        response_data.append({
            "formNumber": form.formNumber,
            "submittedBy": form.submittedBy,
            "submittedDate": form.submittedDate,
            "fields": {
                "treadDiameterNew": form.fields.treadDiameterNew,
                "lastShopIssueSize": form.fields.lastShopIssueSize,
                "condemningDia": form.fields.condemningDia,
                "wheelGauge": form.fields.wheelGauge
            }
        })

    return {
        "success": True,
        "message": "Filtered wheel specification forms fetched successfully.",
        "data": response_data
    }



@router.put("/wheel-specifications/{form_id}", response_model=schemas.form_schemas.WheelSpecificationPostResponse)
def update_wheel_specification_data(
    form_id: int,
    form_in: schemas.form_schemas.WheelSpecificationUpdate,
    db: Session = Depends(get_db)
):
    db_form = crud.crud_forms.get_wheel_specification_by_id(db=db, form_id=form_id)
    if not db_form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Form with ID {form_id} not found",
        )
    
    updated_form = crud.crud_forms.update_wheel_specification(db=db, db_obj=db_form, obj_in=form_in)

    return {
        "success": True,
        "message": f"Form ID {form_id} updated successfully.",
        "data": {
            "formNumber": updated_form.formNumber,
            "submittedBy": updated_form.submittedBy,
            "submittedDate": updated_form.submittedDate.isoformat(),
            "status": "Updated"
        }
    }


@router.delete("/wheel-specifications/{form_id}", response_model=schemas.form_schemas.WheelSpecificationPostResponse)
def delete_wheel_specification_data(
    form_id: int,
    db: Session = Depends(get_db)
):
    db_form = crud.crud_forms.delete_wheel_specification(db=db, form_id=form_id)
    if not db_form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Form with ID {form_id} not found or already deleted",
        )
    
    return {
        "success": True,
        "message": f"Form ID {form_id} has been deleted successfully.",
        "data": {} # No data to return on successful deletion
    }

