from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class WheelSpecification(Base):
    __tablename__ = "wheel_specifications"

    id = Column(Integer, primary_key=True, index=True)
    formNumber = Column(String, unique=True, index=True, nullable=False)
    submittedBy = Column(String, nullable=False)
    submittedDate = Column(Date, nullable=False)

    # Relationship to link to the fields
    fields = relationship("WheelSpecificationFields", back_populates="form", uselist=False, cascade="all, delete-orphan")

class WheelSpecificationFields(Base):
    __tablename__ = "wheel_specification_fields"

    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("wheel_specifications.id"))

    treadDiameterNew = Column(String)
    lastShopIssueSize = Column(String)
    condemningDia = Column(String)
    wheelGauge = Column(String)
    variationSameAxle = Column(String)
    variationSameBogie = Column(String)
    variationSameCoach = Column(String)
    wheelProfile = Column(String)
    intermediateWWP = Column(String)
    bearingSeatDiameter = Column(String)
    rollerBearingOuterDia = Column(String)
    rollerBearingBoreDia = Column(String)
    rollerBearingWidth = Column(String)
    axleBoxHousingBoreDia = Column(String)
    wheelDiscWidth = Column(String)

    # Relationship back to the main form
    form = relationship("WheelSpecification", back_populates="fields")



class BogieChecksheetForm(Base):
    __tablename__ = "bogie_checksheet_forms"
    id = Column(Integer, primary_key=True, index=True)
    formNumber = Column(String, unique=True, index=True, nullable=False)
    inspectionBy = Column(String, nullable=False)
    inspectionDate = Column(Date, nullable=False)

    # Relationships to nested data
    bogieDetails = relationship("BogieDetails", back_populates="form", uselist=False, cascade="all, delete-orphan")
    bogieChecksheet = relationship("BogieChecksheet", back_populates="form", uselist=False, cascade="all, delete-orphan")
    bmbcChecksheet = relationship("BmbcChecksheet", back_populates="form", uselist=False, cascade="all, delete-orphan")

class BogieDetails(Base):
    __tablename__ = "bogie_details"
    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("bogie_checksheet_forms.id"))
    bogieNo = Column(String)
    makerYearBuilt = Column(String)
    incomingDivAndDate = Column(String)
    deficitComponents = Column(String)
    dateOfIOH = Column(String) # Storing as string as per payload
    form = relationship("BogieChecksheetForm", back_populates="bogieDetails")

class BogieChecksheet(Base):
    __tablename__ = "bogie_checksheets"
    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("bogie_checksheet_forms.id"))
    bogieFrameCondition = Column(String)
    bolster = Column(String)
    bolsterSuspensionBracket = Column(String)
    lowerSpringSeat = Column(String)
    axleGuide = Column(String)
    form = relationship("BogieChecksheetForm", back_populates="bogieChecksheet")

class BmbcChecksheet(Base):
    __tablename__ = "bmbc_checksheets"
    id = Column(Integer, primary_key=True, index=True)
    form_id = Column(Integer, ForeignKey("bogie_checksheet_forms.id"))
    cylinderBody = Column(String)
    pistonTrunnion = Column(String)
    adjustingTube = Column(String)
    plungerSpring = Column(String)
    form = relationship("BogieChecksheetForm", back_populates="bmbcChecksheet")
