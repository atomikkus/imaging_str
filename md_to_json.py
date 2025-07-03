import os
import json
import argparse
import logging
import time
from typing import Dict, Any, List
from dotenv import load_dotenv
from mistralai import Mistral
from ct_models import CTScanReport, PETCTReport
from mammo_models import MammogramReport
from langsmith import traceable

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global client instance to reuse across calls
_mistral_client = None

def get_mistral_client():
    """Get or create a global Mistral client instance."""
    global _mistral_client
    if _mistral_client is None:
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable not set.")
        _mistral_client = Mistral(api_key=api_key)
    return _mistral_client

@traceable(
    run_type="llm",
    name="ctscan_extraction",
    tags=["ctscan", "medical_report", "mistral"],
    metadata={"model": "mistral-medium-latest", "report_type": "ctscan"}
)
def get_ctscan_json(markdown_text: str) -> dict:
    """
    Converts markdown text from a CT Scan report to a structured JSON object.
    
    Args:
        markdown_text: The markdown content of the CT Scan report.
    
    Returns:
        A dictionary with the structured CT Scan data.
    """
    client = get_mistral_client()
    model = "mistral-medium-latest"
    
    schema = CTScanReport.model_json_schema()
    
    prompt = f"""Extract structured CT/MRI/USG/Doppler/XRAY/Ultrasound/Thermography/ Scan report data from this markdown text. Return only a JSON object conforming to this schema:

{json.dumps(schema, indent=2)}

Important notes:
- Convert dates to YYYY-MM-DD format.
- Extract all findings, impressions, and recommendations.
- Identify the type of scan (e.g., 'CT', 'MRI', 'USG', 'Doppler', 'XRAY', 'Ultrasound', 'Thermography').
- Identify the type of CT scan if CT is the type of scan (e.g., 'Abdominal', 'Chest', 'Head').
- Include details about contrast media if used.

Report:
{markdown_text}"""

    messages: List[Dict[str, str]] = [
        {"role": "user", "content": prompt}
    ]

    start_time = time.time()
    try:
        print(f"[🔄] Starting CT Scan JSON extraction with {model}...")
        
        chat_response = client.chat.complete(
            model=model,
            messages=messages,  # type: ignore
            response_format={"type": "json_object"},
            max_tokens=4000,
            temperature=0.1
        )
        
        response_content = chat_response.choices[0].message.content  # type: ignore
        if response_content:
            result = json.loads(response_content)  # type: ignore
            elapsed_time = time.time() - start_time
            print(f"[✅] CT Scan JSON extraction completed in {elapsed_time:.2f} seconds")
            return result
        else:
            logging.error("Empty response from Mistral API")
            return {}
    except Exception as e:
        elapsed_time = time.time() - start_time
        logging.error(f"Failed to get CT Scan data from Mistral API after {elapsed_time:.2f}s: {e}")
        return {}

@traceable(
    run_type="llm",
    name="petct_extraction",
    tags=["petct", "medical_report", "mistral"],
    metadata={"model": "mistral-medium-latest", "report_type": "petct"}
)
def get_petct_json(markdown_text: str) -> dict:
    """
    Converts markdown text from a PETCT report to a structured JSON object.
    
    Args:
        markdown_text: The markdown content of the PETCT report.
    
    Returns:
        A dictionary with the structured PETCT data.
    """
    client = get_mistral_client()
    model = "mistral-medium-latest"
    
    schema = PETCTReport.model_json_schema()
    
    prompt = f"""Extract structured PETCT report data from this markdown text. Return only a JSON object conforming to this schema:

{json.dumps(schema, indent=2)}

Important notes:
- Convert dates to YYYY-MM-DD format.
- Extract all findings, impressions, and recommendations.
- Identify SUV max values for lesions.
- Include details about radiopharmaceutical used.

Report:
{markdown_text}"""

    messages: List[Dict[str, str]] = [
        {"role": "user", "content": prompt}
    ]

    start_time = time.time()
    try:
        print(f"[🔄] Starting PETCT JSON extraction with {model}...")
        
        chat_response = client.chat.complete(
            model=model,
            messages=messages,  # type: ignore
            response_format={"type": "json_object"},
            max_tokens=4000,
            temperature=0.1
        )
        
        response_content = chat_response.choices[0].message.content  # type: ignore
        if response_content:
            result = json.loads(response_content)  # type: ignore
            elapsed_time = time.time() - start_time
            print(f"[✅] PETCT JSON extraction completed in {elapsed_time:.2f} seconds")
            return result
        else:
            logging.error("Empty response from Mistral API")
            return {}
    except Exception as e:
        elapsed_time = time.time() - start_time
        logging.error(f"Failed to get PETCT data from Mistral API after {elapsed_time:.2f}s: {e}")
        return {}

@traceable(
    run_type="llm",
    name="mammogram_extraction",
    tags=["mammogram", "medical_report", "mistral"],
    metadata={"model": "mistral-medium-latest", "report_type": "mammogram"}
)
def get_mammogram_json(markdown_text: str) -> dict:
    """
    Converts markdown text from a Mammogram report to a structured JSON object.
    
    Args:
        markdown_text: The markdown content of the Mammogram report.
    
    Returns:
        A dictionary with the structured Mammogram data.
    """
    client = get_mistral_client()
    model = "mistral-medium-latest"
    
    schema = MammogramReport.model_json_schema()
    
    prompt = f"""Extract structured mammogram report data from this markdown text. Return only a JSON object conforming to this schema:

{json.dumps(schema, indent=2)}

Important notes:
- Convert dates to YYYY-MM-DD format.
- Extract BIRADS category.
- Identify breast density.
- Include details about findings and recommendations.

Report:
{markdown_text}"""

    messages: List[Dict[str, str]] = [
        {"role": "user", "content": prompt}
    ]

    start_time = time.time()
    try:
        print(f"[🔄] Starting Mammogram JSON extraction with {model}...")
        
        chat_response = client.chat.complete(
            model=model,
            messages=messages,  # type: ignore
            response_format={"type": "json_object"},
            max_tokens=4000,
            temperature=0.1
        )
        
        response_content = chat_response.choices[0].message.content  # type: ignore
        if response_content:
            result = json.loads(response_content)  # type: ignore
            elapsed_time = time.time() - start_time
            print(f"[✅] Mammogram JSON extraction completed in {elapsed_time:.2f} seconds")
            return result
        else:
            logging.error("Empty response from Mistral API")
            return {}
    except Exception as e:
        elapsed_time = time.time() - start_time
        logging.error(f"Failed to get Mammogram data from Mistral API after {elapsed_time:.2f}s: {e}")
        return {}

def main():
    parser = argparse.ArgumentParser(description="Convert a medical report from markdown to JSON.")
    parser.add_argument("input_file", type=str, help="Path to the input markdown file.")
    parser.add_argument("--output_file", type=str, help="Optional path to the output JSON file.")
    parser.add_argument("--report_type", type=str,
                       choices=["ctscan", "petct", "mammogram"], 
                       help="Type of report to process.")
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        logging.error(f"Input file not found: {args.input_file}")
        return

    # Process based on report type
    if args.report_type == "ctscan":
        json_output = get_ctscan_json(markdown_content)
    elif args.report_type == "petct":
        json_output = get_petct_json(markdown_content)
    elif args.report_type == "mammogram":
        json_output = get_mammogram_json(markdown_content)
    else:
        logging.error(f"Unsupported report type: {args.report_type}")
        return

    if json_output:
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                json.dump(json_output, f, indent=4)
            logging.info(f"Successfully created JSON output at {args.output_file}")
        else:
            print(json.dumps(json_output, indent=4))

if __name__ == "__main__":
    main() 