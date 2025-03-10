import fitz  # PyMuPDF for PDFs
import pytesseract  # OCR
from PIL import Image
from langchain.chat_models import AzureChatOpenAI  # Azure-specific LLM
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory

# ---------------------- Azure OpenAI Configuration ----------------------

# Replace with your Azure OpenAI details
AZURE_OPENAI_API_KEY = "your-azure-openai-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT_NAME = "your-deployment-name"  # Model deployment name
AZURE_OPENAI_API_VERSION = "2023-12-01-preview"  # API version

# ---------------------- PDF Text Extraction Functions ----------------------

# Function to extract text from a text-based PDF
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text if text.strip() else None  # Return None if no text found

# Function to extract text using OCR
def extract_text_with_ocr(pdf_path):
    """Extract text using OCR for scanned PDFs."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            pix = doc[page_num].get_pixmap()  # Convert to image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            page_text = pytesseract.image_to_string(img)  # Perform OCR
            text += page_text + "\n"
    return text

# Tool to handle PDF extraction (with OCR fallback)
@tool
def pdf_text_extraction_tool(pdf_path: str) -> str:
    """Extracts text from a PDF, using OCR if necessary."""
    extracted_text = extract_text_from_pdf(pdf_path)
    if extracted_text:
        return extracted_text
    return extract_text_with_ocr(pdf_path)  # Fallback to OCR

# ---------------------- Azure LLM for Insurance Analysis ----------------------

# Tool to analyze missing insurance details
@tool
def analyze_insurance_details_tool(text: str) -> str:
    """Analyzes insurance document for missing details."""
    prompt = f"""
    You are an expert in insurance policy analysis.
    Given this document:

    {text}

    Identify missing key details:
    - Policy Number
    - Coverage Amount
    - Exclusions
    - Premium Cost
    - Deductible
    - Claim Process

    Provide a structured report listing missing details.
    """

    llm = AzureChatOpenAI(
        openai_api_base=AZURE_OPENAI_ENDPOINT,
        openai_api_version=AZURE_OPENAI_API_VERSION,
        deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
        openai_api_key=AZURE_OPENAI_API_KEY,
        temperature=0
    )
    
    return llm.predict(prompt)

# ---------------------- Initialize LangChain Agent ----------------------

llm = AzureChatOpenAI(
    openai_api_base=AZURE_OPENAI_ENDPOINT,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    deployment_name=AZURE_OPENAI_DEPLOYMENT_NAME,
    openai_api_key=AZURE_OPENAI_API_KEY,
    temperature=0
)

tools = [pdf_text_extraction_tool, analyze_insurance_details_tool]
memory = ConversationBufferMemory(memory_key="history")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    memory=memory
)

# ---------------------- Run the Agent on a PDF ----------------------

pdf_path = "insurance_document.pdf"  # Replace with your file path
extracted_text = pdf_text_extraction_tool.run(pdf_path)
missing_details_report = agent.run(f"Analyze this document for missing details: {extracted_text}")

print("Missing Details Report:\n", missing_details_report)
