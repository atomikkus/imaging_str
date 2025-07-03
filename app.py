import os
import tempfile
import logging
import time
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import our existing modules
from pdf_to_markdown import MarkdownConverter, pdf_to_markdown_text
from md_to_json import get_ctscan_json, get_petct_json, get_mammogram_json, get_mistral_client
from ct_models import CTScanReport, PETCTReport
from mammo_models import MammogramReport

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Medical Imaging PDF reports Processing API (Imaging Reports)",
    description="Convert imaging PDF reports (PETCT, CT Scan, Mammogram) into structured JSON data",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class CTScanResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    processing_time: Optional[float] = None

class PETCTResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    processing_time: Optional[float] = None

class MammogramResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    processing_time: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    mistral_api_configured: bool

# Global converter instance
_converter = None

def get_converter():
    """Get or create a global MarkdownConverter instance."""
    global _converter
    if _converter is None:
        api_key = os.environ.get('MISTRAL_API_KEY')
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set.")
        _converter = MarkdownConverter(api_key=api_key)
    return _converter

async def cleanup_temp_file(file_path: str):
    """Background task to cleanup temporary files."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up temporary file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to cleanup temporary file {file_path}: {e}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Check if Mistral API is configured
        mistral_configured = bool(os.environ.get('MISTRAL_API_KEY'))
        
        # Try to initialize clients to verify configuration
        if mistral_configured:
            get_mistral_client()  # This will raise an error if API key is invalid
            get_converter()
        
        return HealthResponse(
            status="healthy",
            mistral_api_configured=mistral_configured
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")

@app.post("/ctscan_structured", response_model=CTScanResponse)
async def process_ctscan_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF CT/MRI/USG/Doppler Scan report to process")
):
    """
    Process a CT/MRI/USG/Doppler Scan PDF report and extract structured data.
    """
    start_time = time.time()
    temp_file_path = None
    
    try:
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)
        
        logger.info(f"Processing CT Scan report: {file.filename} ({len(content)} bytes)")
        
        converter = get_converter()
        markdown_text = pdf_to_markdown_text(temp_file_path, converter, with_images=False)
        
        if not markdown_text.strip():
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")
        
        structured_data = get_ctscan_json(markdown_text)
        
        if not structured_data:
            raise HTTPException(status_code=400, detail="Failed to extract structured data from document")
        
        try:
            ctscan_report = CTScanReport(**structured_data)
            validated_data = ctscan_report.model_dump()
        except Exception as validation_error:
            logger.warning(f"Data validation warning for CT Scan: {validation_error}")
            validated_data = structured_data
        
        processing_time = time.time() - start_time
        logger.info(f"Successfully processed {file.filename} in {processing_time:.2f} seconds")
        
        background_tasks.add_task(cleanup_temp_file, temp_file_path)
        
        return CTScanResponse(
            success=True,
            message=f"Successfully processed CT Scan report: {file.filename}",
            data=validated_data,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing CT Scan report {file.filename}: {e}")
        if temp_file_path:
            background_tasks.add_task(cleanup_temp_file, temp_file_path)
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/petct_structured", response_model=PETCTResponse)
async def process_petct_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF PETCT report to process")
):
    """
    Process a PETCT PDF report and extract structured data.
    """
    start_time = time.time()
    temp_file_path = None
    
    try:
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)
        
        logger.info(f"Processing PETCT report: {file.filename} ({len(content)} bytes)")
        
        converter = get_converter()
        markdown_text = pdf_to_markdown_text(temp_file_path, converter, with_images=False)
        
        if not markdown_text.strip():
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")
        
        structured_data = get_petct_json(markdown_text)
        
        if not structured_data:
            raise HTTPException(status_code=400, detail="Failed to extract structured data from document")
        
        try:
            petct_report = PETCTReport(**structured_data)
            validated_data = petct_report.model_dump()
        except Exception as validation_error:
            logger.warning(f"Data validation warning for PETCT: {validation_error}")
            validated_data = structured_data
        
        processing_time = time.time() - start_time
        logger.info(f"Successfully processed {file.filename} in {processing_time:.2f} seconds")
        
        background_tasks.add_task(cleanup_temp_file, temp_file_path)
        
        return PETCTResponse(
            success=True,
            message=f"Successfully processed PETCT report: {file.filename}",
            data=validated_data,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing PETCT report {file.filename}: {e}")
        if temp_file_path:
            background_tasks.add_task(cleanup_temp_file, temp_file_path)
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/mammogram_structured", response_model=MammogramResponse)
async def process_mammogram_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="PDF Mammogram report to process")
):
    """
    Process a Mammogram PDF report and extract structured data.
    """
    start_time = time.time()
    temp_file_path = None
    
    try:
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file_path = temp_file.name
            content = await file.read()
            temp_file.write(content)
        
        logger.info(f"Processing Mammogram report: {file.filename} ({len(content)} bytes)")
        
        converter = get_converter()
        markdown_text = pdf_to_markdown_text(temp_file_path, converter, with_images=False)
        
        if not markdown_text.strip():
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")
        
        structured_data = get_mammogram_json(markdown_text)
        
        if not structured_data:
            raise HTTPException(status_code=400, detail="Failed to extract structured data from document")
        
        try:
            mammogram_report = MammogramReport(**structured_data)
            validated_data = mammogram_report.model_dump()
        except Exception as validation_error:
            logger.warning(f"Data validation warning for Mammogram: {validation_error}")
            validated_data = structured_data
        
        processing_time = time.time() - start_time
        logger.info(f"Successfully processed {file.filename} in {processing_time:.2f} seconds")
        
        background_tasks.add_task(cleanup_temp_file, temp_file_path)
        
        return MammogramResponse(
            success=True,
            message=f"Successfully processed Mammogram report: {file.filename}",
            data=validated_data,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing Mammogram report {file.filename}: {e}")
        if temp_file_path:
            background_tasks.add_task(cleanup_temp_file, temp_file_path)
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/")
async def root():
    return {"message": "Welcome to the Medical Report Processing API. Visit /docs for API documentation."
}

if __name__ == "__main__":
    import uvicorn
    
    # Check if API key is configured
    if not os.environ.get('MISTRAL_API_KEY'):
        logger.error("MISTRAL_API_KEY environment variable not set!")
        exit(1)
    
    logger.info("Starting Medical Report Processing API...")
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True) 