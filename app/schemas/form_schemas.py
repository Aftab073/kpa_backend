from pydantic import BaseModel, ConfigDict, Field, validator
from typing import Optional, List
from datetime import date

# ==============================================================================
# Schemas for Wheel Specifications
# ==============================================================================

# --- Schemas for the NESTED 'fields' object ---

class WheelSpecificationFieldsBase(BaseModel):
    """Base schema for the fields within a wheel specification form."""
    treadDiameterNew: str
    lastShopIssueSize: str
    condemningDia: str
    wheelGauge: str
    variationSameAxle: str
    variationSameBogie: str
    variationSameCoach: str
    wheelProfile: str
    intermediateWWP: str
    bearingSeatDiameter: str
    rollerBearingOuterDia: str
    rollerBearingBoreDia: str
    rollerBearingWidth: str
    axleBoxHousingBoreDia: str
    wheelDiscWidth: str

class WheelSpecificationFieldsCreate(WheelSpecificationFieldsBase):
    """Schema for creating the fields. Inherits all fields without change."""
    pass

class WheelSpecificationFields(WheelSpecificationFieldsBase):
    """Schema for reading fields from the DB, includes the 'id'."""
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Schemas for the TOP-LEVEL form ---

class WheelSpecificationBase(BaseModel):
    """Base schema for the main form metadata."""
    formNumber: str = Field(..., min_length=1)
    submittedBy: str = Field(..., min_length=1)
    submittedDate: date

    # CORRECT PLACEMENT: The validator is now in the same class as the field.
    @validator('submittedDate')
    def date_cannot_be_in_the_future(cls, v):
        if v > date.today():
            raise ValueError('submittedDate cannot be in the future')
        return v

class WheelSpecificationCreate(WheelSpecificationBase):
    """Schema for the full request body when creating a new wheel spec."""
    fields: WheelSpecificationFieldsCreate

class WheelSpecification(WheelSpecificationBase):
    """Schema for reading a full wheel spec from the DB, includes 'id'."""
    id: int
    fields: WheelSpecificationFields
    model_config = ConfigDict(from_attributes=True)
    
class WheelSpecificationUpdate(BaseModel):
    """Schema for updates. All fields are optional."""
    formNumber: Optional[str] = Field(None, min_length=1)
    submittedBy: Optional[str] = Field(None, min_length=1)
    submittedDate: Optional[date] = None
    fields: Optional[WheelSpecificationFieldsCreate] = None

# --- Schemas for API Responses (Wheel Spec) ---

class WheelSpecificationGetResponseFields(BaseModel):
    """
    (IMPROVEMENT) A strongly-typed schema for the GET response's fields,
    instead of a generic 'dict'. Matches Postman collection.
    """
    treadDiameterNew: str
    lastShopIssueSize: str
    condemningDia: str
    wheelGauge: str
    
class WheelSpecificationGetResponseData(BaseModel):
    """Schema for a single data item in the GET response list."""
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: WheelSpecificationGetResponseFields
    model_config = ConfigDict(from_attributes=True)

class WheelSpecificationPostResponse(BaseModel):
    success: bool
    message: str
    data: dict

class WheelSpecificationGetResponse(BaseModel):
    success: bool
    message: str
    data: List[WheelSpecificationGetResponseData]


# ==============================================================================
# Schemas for Bogie Checksheets
# ==============================================================================

# --- Schemas for CREATING Bogie Checksheets ---

class BogieDetailsCreate(BaseModel):
    bogieNo: str
    makerYearBuilt: str
    incomingDivAndDate: str
    deficitComponents: str
    dateOfIOH: str

class BogieChecksheetCreate(BaseModel):
    bogieFrameCondition: str
    bolster: str
    bolsterSuspensionBracket: str
    lowerSpringSeat: str
    axleGuide: str

class BmbcChecksheetCreate(BaseModel):
    cylinderBody: str
    pistonTrunnion: str
    adjustingTube: str
    plungerSpring: str

class BogieChecksheetCreateForm(BaseModel):
    """Schema for the full request body when creating a new bogie checksheet."""
    formNumber: str = Field(..., min_length=1)
    inspectionBy: str = Field(..., min_length=1)
    inspectionDate: date
    bogieDetails: BogieDetailsCreate
    bogieChecksheet: BogieChecksheetCreate
    bmbcChecksheet: BmbcChecksheetCreate

# --- (MISSING PART - ADDED) Schemas for READING Bogie Checksheets ---

class BogieDetails(BogieDetailsCreate):
    """Schema for reading BogieDetails from the DB, includes 'id'."""
    id: int
    model_config = ConfigDict(from_attributes=True)

class BogieChecksheet(BogieChecksheetCreate):
    """Schema for reading BogieChecksheet from the DB, includes 'id'."""
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class BmbcChecksheet(BmbcChecksheetCreate):
    """Schema for reading BmbcChecksheet from the DB, includes 'id'."""
    id: int
    model_config = ConfigDict(from_attributes=True)
    
class BogieChecksheetResponse(BaseModel):
    """Schema for reading a full BogieChecksheetForm from the DB."""
    id: int
    formNumber: str
    inspectionBy: str
    inspectionDate: date
    bogieDetails: BogieDetails
    bogieChecksheet: BogieChecksheet
    bmbcChecksheet: BmbcChecksheet
    model_config = ConfigDict(from_attributes=True)

# --- Schemas for API Responses (Bogie Checksheet) ---

class BogieChecksheetPostResponse(BaseModel):
    success: bool
    message: str
    data: dict

