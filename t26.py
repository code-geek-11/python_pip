# Run the agent based on the type of document
def analyze_document(document_text: str, document_type: str):
    """
    Analyzes a document based on its type (Policy or Claims).
    Calls the appropriate tool explicitly.
    """
    if document_type.lower() == "policy":
        return analyze_insurance_policy_tool.run(document_text)
    elif document_type.lower() == "claims":
        return analyze_claims_document_tool.run(document_text)
    else:
        return "Invalid document type. Please specify 'policy' or 'claims'."

# Example usage
policy_text = """Your extracted insurance policy text goes here."""
claims_text = """Your extracted claims document text goes here."""

# Explicitly calling the correct tool
policy_analysis = analyze_document(policy_text, "policy")
claims_analysis = analyze_document(claims_text, "claims")

print("Policy Analysis:\n", policy_analysis)
print("\nClaims Analysis:\n", claims_analysis)
