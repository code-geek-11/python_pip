@tool
def analyze_claims_document_tool(claims_text: str) -> str:
    """Analyzes a claims document to find missing details."""
    prompt = f"""
    You are an expert in insurance claims processing.  
    Analyze the following claims document and identify missing key details:

    {claims_text}

    The claim document should include:  
    - Claimant’s Name  
    - Policy Number  
    - Date of Incident  
    - Type of Claim (Property, Medical, Liability, etc.)  
    - Description of Incident  
    - Supporting Documents (Police Report, Medical Bills, etc.)  
    - Claim Amount Requested  

    If any of these are missing, list them. Otherwise, confirm that all details are present.
    """

    llm = AzureChatOpenAI(
        openai_api_base=AZURE_OPENAI_ENDPOINT,
        openai_api_version=AZURE_OPENAI_API_VERSION,
        deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_key=AZURE_OPENAI_API_KEY,
        temperature=0
    )

    return llm.predict(prompt)
