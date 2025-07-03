from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date

class Measurement(BaseModel):
    """
    A class to represent a single measurement of a finding.
    """
    length: Optional[str] = Field(None, description="Length of the finding, e.g., '18 mm'")
    width: Optional[str] = Field(None, description="Width of the finding, e.g., '16 mm'")
    depth: Optional[str] = Field(None, description="Depth of the finding, e.g., '15 mm'")

class Finding(BaseModel):
    """
    A class to represent a single finding within an organ or region.
    """
    location: str = Field(..., description="Specific location of the finding, e.g., 'Cervical Level II'")
    lobe: Optional[str] = Field(None, description="Specific lobe if applicable, e.g., 'Lower lobe'")
    measurements: Measurement = Field(..., description="Measurements of the finding.")
    suv_max_value: Optional[float] = Field(None, description="Maximum Standardized Uptake Value.")
    description: str = Field(..., description="Textual description of the finding.")
    comparison: Optional[str] = Field(None, description="Comparison to previous scans.")

class OrganSystem(BaseModel):
    """
    A class to represent findings within a specific organ or system.
    """
    organ: str = Field(..., description="The organ or system being reported, e.g., 'Lymph nodes', 'Right Lung'")
    hypermetabolic_region: str = Field(..., description="The broader anatomical region, e.g., 'Head and Neck', 'Thorax'")
    findings: List[Finding] = Field(..., description="A list of specific findings for this organ.")

class PETCTReport(BaseModel):
    """
    A Pydantic model to represent a patient's PET/CT report.
    """
    patient_name: str = Field(..., description="Name of the patient.")
    date_of_test: date = Field(..., description="Date the PET/CT scan was performed.")
    test_type: str = Field(..., description="Type of test performed, e.g., 'PET-CT'")
    organ_systems: List[OrganSystem] = Field(..., description="List of organ systems with findings.")
    other_abnormalities: Optional[str] = Field(None, description="Description of other noted abnormalities.")
    impression: str = Field(..., description="The overall impression from the report.")
    hospital_lab_name: str = Field(..., description="Name of the hospital or lab.")
    hospital_lab_id: str = Field(..., description="Identifier for the hospital or lab.")

class Lesion(BaseModel):
    """
    A class to represent a single lesion found in a CT scan.
    """
    site: str = Field(..., description="The anatomical site of the lesion, e.g., 'Uterus'")
    max_length_cm: Optional[float] = Field(None, description="Maximum length of the lesion in centimeters.")
    width_cm: Optional[float] = Field(None, description="Width of the lesion in centimeters.")
    depth_cm: Optional[float] = Field(None, description="Depth of the lesion in centimeters.")
    description: str = Field(..., description="Textual description of the lesion.")

class CTScanReport(BaseModel):
    """
    A Pydantic model to represent a patient's CT scan report.
    """
    patient_name: str = Field(..., description="Name of the patient.")
    test_type: str = Field(..., description="Type of test performed, e.g., 'CT Scan'")
    date_of_test: date = Field(..., description="Date the CT scan was performed.")
    imaging_site: str = Field(..., description="Anatomical area scanned, e.g., 'Abdomen and Pelvis'")
    contrast_enhanced: bool = Field(..., description="Whether contrast was used for the imaging.")
    new_lesion_evidence: bool = Field(..., description="Indicates if there is evidence of a new lesion.")
    lesions: List[Lesion] = Field(..., description="A list of lesions identified in the scan.")
    lymph_nodes_detected: Optional[int] = Field(None, description="The number of lymph nodes detected.")
    impression: str = Field(..., description="The overall impression from the report.")
    imaging_comments: Optional[str] = Field(None, description="Any additional comments on the imaging.")
    hospital_name: Optional[str] = Field(None, description="Name of the hospital or lab.")
    hospital_location: Optional[str] = Field(None, description="Location of the hospital or lab.") 