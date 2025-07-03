# 🏥 Medical Report Processing API

A FastAPI-based pipeline that converts medical PDF reports (therapy and radiation therapy) into structured JSON data using Mistral AI's OCR and language models.

## 🚀 Features

- **Complete PDF → JSON Pipeline**: Upload medical PDFs and get structured JSON data
- **Multiple Report Types**: Supports therapy reports (chemotherapy, biological, etc.) and radiation therapy reports
- **Mistral AI Integration**: Uses Mistral OCR for PDF text extraction and AI models for data structuring
- **Pydantic Models**: Structured data validation using medical report-specific models
- **RESTful API**: Clean endpoints for programmatic access
- **Async & Error Handling**: Comprehensive error handling and async processing

## 📁 Project Structure

```
therapies_api/
├── app.py                  # FastAPI application (main pipeline)
├── pdf_to_markdown.py      # PDF to markdown conversion using Mistral OCR
├── md_to_json.py          # Markdown to structured JSON using AI
├── therapy_models.py      # Pydantic models for therapy reports
├── rad_models.py          # Pydantic models for radiation therapy reports
├── requirements.txt       # Python dependencies
├── test_api.py           # API testing script
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🛠️ Setup

### Option 1: Docker Deployment (Recommended)

#### Prerequisites
- Docker installed
- Mistral AI API key

#### Quick Start with .env file
```bash
# 1. Clone and navigate
git clone <repository>
cd therapies_api

# 2. Set up environment file
cp .env.example .env
# Edit .env and add your Mistral API key

# 3. Build Docker image
docker build -t therapy-api .

# 4. Run container with .env file
docker run -d \
  --name therapy-api \
  -p 8000:8000 \
  --env-file .env \
  therapy-api
```

#### Alternative: Manual Environment Variables
```bash
# If you prefer to set variables manually
docker run -d \
  --name therapy-api \
  -p 8000:8000 \
  -e MISTRAL_API_KEY=your_actual_api_key_here \
  -e LOG_LEVEL=INFO \
  therapy-api
```

#### Docker Management Commands
```bash
# View logs
docker logs -f therapy-api

# Stop container
docker stop therapy-api

# Remove container
docker rm therapy-api

# Restart container
docker restart therapy-api
```

### Option 2: Local Development

#### Prerequisites
- Python 3.8+
- Mistral AI API key

#### Setup Steps
```bash
# 1. Clone and navigate
git clone <repository>
cd therapies_api

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment configuration
cp .env.example .env
# Edit .env and add your Mistral API key

# 5. Run the application
python app.py
```

**Get your Mistral API key from**: https://console.mistral.ai/

The API will be available at: http://localhost:8000

## 🌐 API Endpoints

### 1. Health Check
```bash
GET /health

curl http://localhost:8000/health
```

### 2. Process Therapy Reports
```bash
POST /therapies
Content-Type: multipart/form-data

curl -X POST "http://localhost:8000/therapies" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@therapy_report.pdf"
```

**Therapy Response Example:**
```json
{
  "success": true,
  "message": "Successfully processed therapy report: therapy_report.pdf",
  "processing_time": 15.42,
  "data": {
    "patient_id": "PAT123",
    "therapy_type": "Chemotherapy",
    "administration_route": "Intravenous",
    "drugs_administered": [
      {
        "drug_name": "Docetaxel",
        "dosage": 75.0,
        "unit": "mg/m²"
      }
    ],
    "first_date_of_therapy": "2024-01-15",
    "number_of_cycles": 6,
    "cycle_interval_days": 21,
    "adverse_event_observed": true,
    "adverse_event_medication": "Ondansetron",
    "hospital_name": "City Medical Center",
    "hospital_location": "New York, NY"
  }
}
```

### 3. Process Radiation Therapy Reports
```bash
POST /radiation
Content-Type: multipart/form-data

curl -X POST "http://localhost:8000/radiation" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@radiation_report.pdf"
```

**Radiation Response Example:**
```json
{
  "success": true,
  "message": "Successfully processed radiation therapy report: radiation_report.pdf",
  "processing_time": 12.35,
  "data": {
    "patient_name": "John Doe",
    "test_therapy": "therapy",
    "radiation_type": "EBRT",
    "start_date": "2024-01-10",
    "end_date": "2024-02-15",
    "fractions": 25,
    "dosage": 50.0,
    "unit": "Gy",
    "area_treated": "Spine",
    "events": "Mild skin irritation",
    "medication": "Topical cream",
    "lab_name": "Regional Cancer Center",
    "lab_location": "Boston, MA"
  }
}
```

## 📊 Data Models

### Therapy Reports Extract:
- Patient ID and therapy type
- Drug names, dosages, and units
- Treatment schedule and cycles
- Adverse events and medications
- Hospital information

### Radiation Therapy Reports Extract:
- Patient name and radiation type
- Treatment dates and fractions
- Total dosage and units
- Area treated
- Adverse events and medications
- Laboratory information

## 🔧 Command Line Usage

### Process Therapy Reports:
```bash
python md_to_json.py therapy_report.md --report_type therapy --output_file result.json
```

### Process Radiation Reports:
```bash
python md_to_json.py radiation_report.md --report_type radiation --output_file result.json
```

### Convert PDF to Markdown:
```bash
python pdf_to_markdown.py --input_pdf report.pdf
# Creates: report_no_images.md, report_with_images.md, report.txt
```

## 🐳 Docker Deployment

### Simple Docker Setup

The project includes a `Dockerfile` for easy containerization:

```bash
# Build the image
docker build -t therapy-api .

# Run the container
docker run -d \
  --name therapy-api \
  -p 8000:8000 \
  --env-file .env \
  therapy-api
```

### Environment Variables

The containerized application uses the following environment variables:

```bash
MISTRAL_API_KEY=your_api_key_here  # Required
LOG_LEVEL=INFO                     # Optional (DEBUG, INFO, WARNING, ERROR)
```

### Container Features

- **🔒 Security**: Runs as non-root user
- **🏥 Health Checks**: Built-in health monitoring
- **🔄 File Cleanup**: Automatic temporary file cleanup
- **📦 Optimized**: Multi-layer caching for faster builds

## 🧪 Testing

### Manual Testing:
1. **Health Check**: Visit http://localhost:8000/health
2. **API Documentation**: Visit http://localhost:8000/docs (Swagger UI)
3. **Test with cURL**: Use the example commands above

### Docker Testing:
```bash
# Test API health
curl http://localhost:8000/health

# Test therapy endpoint
curl -X POST "http://localhost:8000/therapies" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_therapy.pdf"

# Test radiation endpoint
curl -X POST "http://localhost:8000/radiation" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_radiation.pdf"
```

## 📝 Supported Report Types

### Therapy Reports:
- **Chemotherapy**: Traditional cancer drug treatments
- **Biological Therapy**: Targeted biological treatments
- **Hormonal Therapy**: Hormone-based treatments
- **Targeted Therapy**: Precision medicine approaches
- **Immunotherapy**: Immune system-based treatments

### Radiation Therapy Reports:
- **EBRT**: External Beam Radiation Therapy
- **IMRT**: Intensity-Modulated Radiation Therapy
- **IGRT**: Image-Guided Radiation Therapy
- **Stereotactic**: Stereotactic radiosurgery/radiotherapy
- **Brachytherapy**: Internal radiation therapy

## ⚠️ Requirements

- **Python 3.8+**
- **Mistral AI API Key** (required for OCR and AI processing)
- **PDF files** containing medical reports in standard format

## 🛡️ Error Handling

The API provides comprehensive error handling:
- **400**: Invalid file format or empty content
- **500**: Processing errors or API issues
- **Detailed logging** for debugging
- **Async processing** with background task cleanup

## 🔒 Security Notes

- API keys are loaded from environment variables
- Temporary files are automatically cleaned up
- CORS is configured (adjust for production)

## 📞 Support

For issues or questions:
1. Check the API health endpoint: `/health`
2. Review logs for detailed error information
3. Ensure your Mistral API key is valid and has sufficient credits

---

**Built with**: FastAPI, Mistral AI, Pydantic, and modern Python tools 