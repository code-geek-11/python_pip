import os
import fitz  # PyMuPDF for PDF processing
import pytesseract  # OCR for scanned PDFs
from PIL import Image
from flask import Flask, request, jsonify
from langchain.chat_models import AzureChatOpenAI
from werkzeug.utils import secure_filename

# ---------------------- Flask App Initialization ----------------------
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------------------- Azure OpenAI Configuration ----------------------
AZURE_OPENAI_API_KEY = "your-azure-openai-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-deployment-name"
AZURE_OPENAI_API_VERSION = "2023-12-01-preview"

llm = AzureChatOpenAI(
    openai_api_base=AZURE_OPENAI_ENDPOINT,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
    openai_api_key=AZURE_OPENAI_API_KEY,
    temperature=0
)

# ---------------------- Helper Functions ----------------------

def extract_text_from_pdf(pdf_path):
    """Extracts text from a text-based PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text if text.strip() else None  # Return None if no text found

def extract_text_with_ocr(pdf_path):
    """Extracts text using OCR for scanned PDFs."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            pix = doc[page_num].get_pixmap()  # Convert to image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            page_text = pytesseract.image_to_string(img)  # Perform OCR
            text += page_text + "\n"
    return text

def classify_document(email_subject, email_body):
    """Classifies if the email is related to Policy or Claim."""
    prompt = f"""
    You are an expert in insurance document classification.
    Given the following email subject and body:

    Subject: {email_subject}
    Body: {email_body}

    Determine if it is related to:
    - "policy" if it discusses insurance coverage, premiums, exclusions, or terms.
    - "claim" if it discusses an incident, damages, reimbursement, claim amount, or supporting documents.
    - "unknown" if it does not fit either category.

    Only return "policy", "claim", or "unknown". No explanations.
    """
    return llm.predict(prompt).strip().lower()

def analyze_missing_details(doc_type, text):
    """Analyzes missing details based on document type."""
    if doc_type == "policy":
        return analyze_insurance_policy_tool.run(text)
    elif doc_type == "claim":
        return analyze_claims_document_tool.run(text)
    else:
        return "No relevant missing details found."

def generate_response_email(missing_details, doc_type):
    """Generates a professional email response mentioning missing details."""
    prompt = f"""
    You are an expert insurance agent. Draft a professional email response
    regarding a {doc_type} inquiry. Address the customer, mention the missing details, 
    and request the necessary information.

    Missing Details:
    {missing_details}

    Ensure the tone is professional and customer-friendly.
    """
    return llm.predict(prompt)

# ---------------------- Flask API Route ----------------------
@app.route("/analyze-email", methods=["POST"])
def analyze_email():
    """API Endpoint to process the email and return the generated response."""
    try:
        # Get email details from request
        email_subject = request.form.get("email_subject")
        email_body = request.form.get("email_body")
        pdf_file = request.files.get("pdf_attachment")

        if not email_subject or not email_body:
            return jsonify({"error": "Email subject and body are required."}), 400

        # Save uploaded PDF file
        pdf_text = ""
        if pdf_file:
            filename = secure_filename(pdf_file.filename)
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            pdf_file.save(pdf_path)

            # Extract text (Use OCR if needed)
            pdf_text = extract_text_from_pdf(pdf_path) or extract_text_with_ocr(pdf_path)

        # Classify document type (Policy / Claim)
        doc_type = classify_document(email_subject, email_body)

        if doc_type == "unknown":
            return jsonify({"message": "This email is not related to a policy or claim."})

        # Combine email body & PDF text for analysis
        combined_text = f"Email Body:\n{email_body}\n\nExtracted PDF Content:\n{pdf_text}"

        # Identify missing details
        missing_details = analyze_missing_details(doc_type, combined_text)

        # Generate professional response email
        response_email_body = generate_response_email(missing_details, doc_type)

        return jsonify({
            "document_type": doc_type,
            "missing_details": missing_details,
            "generated_email": response_email_body
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------- Run Flask App ----------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
