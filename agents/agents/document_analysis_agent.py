"""
Agent responsible for analyzing PDF content and extracting structured information.
"""
from crewai import Agent, Task
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tools import PDFContentProcessor, InformationExtractor
import config

class DocumentAnalysisAgent:
    def __init__(self, pdf_content=None):
        self.pdf_content = pdf_content
        self.tools = [
            PDFContentProcessor(),
            InformationExtractor(),
        ]
    
    def get_agent(self):
        """Create and return the document analysis agent."""
        return Agent(
            role="Document Analysis Expert",
            goal="Extract key information and insights from document content",
            backstory=(
                "You are an expert in document analysis with years of experience "
                "extracting structured information from unstructured text. You excel "
                "at identifying key data points, relationships, and patterns in documents."
            ),
            verbose=True,
            allow_delegation=True,
            llm='gemini/gemini-1.5-flash',
        )
    
    def get_task(self):
        """Create and return the document analysis task."""
        return Task(
            description=(
                f"Analyze the provided document content and extract structured information. "
                f"Include key entities, relationships, main topics, and any relevant data points. "
                f"The content is as follows: {self.pdf_content[:500]}... [content truncated]"
            ),
            expected_output=(
                "A JSON structure containing extracted information including: "
                "1. Key entities (people, organizations, locations, etc.) "
                "2. Main topics and themes "
                "3. Important facts and data points "
                "4. Relationships between entities "
                "5. Any time-sensitive information or dates"
            ),
            agent=self.get_agent()
        )
    
    def _get_gemini_llm(self):
        """Initialize the Gemini LLM."""
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        return ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=config.TEMPERATURE,
            verbose=config.VERBOSE
        )