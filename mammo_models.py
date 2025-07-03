from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Measurement(BaseModel):
    """
    A class to represent measurements of a finding in millimeters.
    """
    length_mm: Optional[int] = Field(None, description="Length of the finding in millimeters.")
    width_mm: Optional[int] = Field(None, description="Width of the finding in millimeters.")

class Finding(BaseModel):
    """
    A class to represent a single finding within a breast.
    """
    category: Optional[str] = Field(None, description="Category of the finding, e.g., 'Category 5'")
    location: str = Field(..., description="Location of the finding, e.g., 'Central, Retro'")
    measurements: Optional[Measurement] = Field(None, description="Measurements of the finding.")
    shape: Optional[str] = Field(None, description="Shape of the finding, e.g., 'round'")
    density: Optional[str] = Field(None, description="Density of the finding, e.g., 'Microlobulated'")
    associated_calcifications: Optional[bool] = Field(None, description="Indicates if associated calcifications are present.")
    associated_features: List[str] = Field(..., description="List of descriptions for associated features.")
    calcifications: Optional[str] = Field(None, description="Details about calcifications.")
    architectural_distortion: Optional[str] = Field(None, description="Details about architectural distortion.")
    skin_lesion: Optional[str] = Field(None, description="Details about any skin lesions.")

class BreastComposition(BaseModel):
    """
    A class to represent the composition and findings of a single breast.
    """
    name: str = Field(..., description="Name of the breast, e.g., 'Left Composition'")
    findings: List[Finding] = Field(..., description="List of findings for this breast.")


class MammogramReport(BaseModel):
    """
    A Pydantic model to represent a patient's mammogram report.
    """
    patient_name: str = Field(..., description="Name of the patient.")
    test_type: str = Field(..., description="Type of test performed, e.g., 'Mammogram'")
    date_of_test: date = Field(..., description="Date the mammogram was performed.")
    reason_for_test: str = Field(..., description="Reason for the mammogram, e.g., 'Asymptomatic path'")
    breast_composition: List[BreastComposition] = Field(..., description="Composition and findings for each breast.")
    birads_score: int = Field(..., description="BI-RADS score.")
    birads_composition_comments: str = Field(..., description="Comments on BI-RADS composition.")
    impression: Optional[str] = Field(None, description="The overall impression from the report.")
    hospital_name: str = Field(..., description="Name of the hospital or lab.")
    lab_technician: Optional[str] = Field(None, description="Name of the lab technician.")

