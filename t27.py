from langchain.chat_models import AzureChatOpenAI

# ---------------------- Azure OpenAI Configuration ----------------------

AZURE_OPENAI_API_KEY = "your-azure-openai-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-deployment-name"
AZURE_OPENAI_API_VERSION = "2023-12-01-preview"

# ---------------------- Initialize LLM ----------------------

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

# ---------------------- Document Analysis Based on Classification ----------------------

def analyze_email(email_subject: str, email_body: str):
    """
    Classifies the email using subject & body and analyzes it using the appropriate tool.
    """
    doc_type = classify_document(email_subject, email_body)

    if doc_type == "policy":
        return analyze_insurance_policy_tool.run(email_body)
    elif doc_type == "claim":
        return analyze_claims_document_tool.run(email_body)
    else:
        return "This email does not appear to be related to an insurance policy or a claim."

# ---------------------- Example Usage ----------------------

email_subject_policy = "Inquiry About Policy Coverage and Exclusions"
email_body_policy = """
Dear Insurance Team,

I would like to inquire about the coverage details of my general insurance policy. 
Can you please confirm the exclusions and deductible amount? Also, I need clarity on the premium structure.

Best regards,  
John Doe
"""

email_subject_claim = "Car Accident Claim Submission - Urgent"
email_body_claim = """
Dear Claims Department,

I recently met with an accident and need to file a claim. The incident happened on March 15, 2024. 
My vehicle sustained damages, and I have attached the police report and photographs. 
Please guide me on the claim process and required documents.

Regards,  
John Doe
"""

# Run classification and analysis
print("Policy Email Analysis:\n", analyze_email(email_subject_policy, email_body_policy))
print("\nClaims Email Analysis:\n", analyze_email(email_subject_claim, email_body_claim))
