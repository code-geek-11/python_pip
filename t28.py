import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from langchain.chat_models import AzureChatOpenAI

# ---------------------- Azure OpenAI Configuration ----------------------

AZURE_OPENAI_API_KEY = "your-azure-openai-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-deployment-name"
AZURE_OPENAI_API_VERSION = "2023-12-01-preview"

# ---------------------- Email Configuration (Outlook SMTP) ----------------------

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SENDER_EMAIL = "your-email@outlook.com"
SENDER_PASSWORD = "your-email-password"

# ---------------------- Initialize Azure OpenAI Model ----------------------

llm = AzureChatOpenAI(
    openai_api_base=AZURE_OPENAI_ENDPOINT,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
    openai_api_key=AZURE_OPENAI_API_KEY,
    temperature=0
)

# ---------------------- Document Classification Function ----------------------

def classify_document(email_subject: str, email_body: str) -> str:
    """
    Classifies whether the email is related to an insurance policy or a claim using both subject and body.
    """
    prompt = f"""
    You are an expert in insurance document classification.
    Given the following email subject and body:

    Subject: {email_subject}

    Body: {email_body}

    Determine whether it is related to:
    - "policy" if it discusses insurance coverage, premiums, exclusions, terms, or conditions.
    - "claim" if it discusses an incident, damages, reimbursement, claim amount, or supporting documents.
    - "unknown" if the content does not match either category.

    Only return "policy", "claim", or "unknown". No explanations.
    """
    
    return llm.predict(prompt).strip().lower()

# ---------------------- Missing Details Analysis ----------------------

def analyze_email(email_subject: str, email_body: str):
    """
    Classifies the email using subject & body and analyzes it using the appropriate tool.
    """
    doc_type = classify_document(email_subject, email_body)

    if doc_type == "policy":
        analysis_result = analyze_insurance_policy_tool.run(email_body)
    elif doc_type == "claim":
        analysis_result = analyze_claims_document_tool.run(email_body)
    else:
        return "This email does not appear to be related to an insurance policy or a claim."

    return doc_type, analysis_result

# ---------------------- Generate Well-Drafted Response Email ----------------------

def generate_response_email(original_subject: str, missing_details: str, doc_type: str):
    """
    Generates a professional email response highlighting the missing details.
    """
    prompt = f"""
    You are an expert insurance agent. Draft a polite and professional email response 
    regarding a {doc_type} inquiry. Address the customer, mention the missing details, 
    and request the necessary information.

    Missing Details:
    {missing_details}

    Ensure the tone is professional and customer-friendly.
    """
    
    return llm.predict(prompt)

# ---------------------- Send Email Using Outlook SMTP ----------------------

def send_email(recipient_email: str, subject: str, body: str):
    """
    Sends an email via Outlook SMTP.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return "Email sent successfully."
    except Exception as e:
        return f"Failed to send email: {str(e)}"

# ---------------------- Example Usage ----------------------

email_subject = "Car Insurance Claim Submission - Urgent"
email_body = """
Dear Claims Department,

I recently met with an accident and need to file a claim. My vehicle sustained damages, and I have attached the police report and photographs.
Please guide me on the claim process.

Best regards,
John Doe
"""

# Analyze the email for missing details
doc_type, missing_details = analyze_email(email_subject, email_body)

# Generate a well-drafted response email
response_email_body = generate_response_email(email_subject, missing_details, doc_type)

# Send the response email
send_status = send_email("abcd@outlook.com", f"Re: {email_subject}", response_email_body)

print("Email Sent Status:", send_status)
