from sqlalchemy.orm import Session
from ..models import form_models
from ..schemas import form_schemas
from datetime import date
from fastapi.encoders import jsonable_encoder



def get_wheel_specification_by_id(db: Session, form_id: int):
    return db.query(form_models.WheelSpecification).filter(form_models.WheelSpecification.id == form_id).first()

def update_wheel_specification(db: Session, db_obj: form_models.WheelSpecification, obj_in: form_schemas.WheelSpecificationUpdate):
    obj_data = jsonable_encoder(db_obj)
    update_data = obj_in.dict(exclude_unset=True) # Get only the fields that were sent

    for field in obj_data:
        if field in update_data:
            setattr(db_obj, field, update_data[field])
    
    # Handle nested fields object separately
    if 'fields' in update_data and update_data['fields'] is not None:
        for key, value in update_data['fields'].items():
            setattr(db_obj.fields, key, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_wheel_specification(db: Session, form_id: int):
    db_obj = get_wheel_specification_by_id(db, form_id)
    if db_obj:
        db.delete(db_obj)
        db.commit()
    return db_obj


def create_wheel_specification(db: Session, form: form_schemas.WheelSpecificationCreate):
    # Create the nested fields object first
    db_fields = form_models.WheelSpecificationFields(**form.fields.dict())
    
    # Create the main form object, excluding the 'fields' part
    form_data = form.dict(exclude={"fields"})
    db_form = form_models.WheelSpecification(**form_data)
    
    # Associate the fields with the form
    db_form.fields = db_fields

    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form

def get_wheel_specifications(db: Session, formNumber: str | None, submittedBy: str | None, submittedDate: date | None, skip: int = 0, limit: int = 100):
    query = db.query(form_models.WheelSpecification)

    if formNumber:
        query = query.filter(form_models.WheelSpecification.formNumber == formNumber)
    if submittedBy:
        query = query.filter(form_models.WheelSpecification.submittedBy == submittedBy)
    if submittedDate:
        query = query.filter(form_models.WheelSpecification.submittedDate == submittedDate)
    
    return query.offset(skip).limit(limit).all()

def get_bogie_checksheet_by_form_number(db: Session, formNumber: str):
    return db.query(form_models.BogieChecksheetForm).filter(form_models.BogieChecksheetForm.formNumber == formNumber).first()

def create_bogie_checksheet(db: Session, form: form_schemas.BogieChecksheetCreateForm):
    # Create the main form object first, excluding nested objects
    form_data = form.dict(exclude={"bogieDetails", "bogieChecksheet", "bmbcChecksheet"})
    db_form = form_models.BogieChecksheetForm(**form_data)
    
    # Create and associate the nested objects
    db_form.bogieDetails = form_models.BogieDetails(**form.bogieDetails.dict())
    db_form.bogieChecksheet = form_models.BogieChecksheet(**form.bogieChecksheet.dict())
    db_form.bmbcChecksheet = form_models.BmbcChecksheet(**form.bmbcChecksheet.dict())

    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form
