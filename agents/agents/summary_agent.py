"""
Agent responsible for summarizing the extracted information from documents.
"""
from crewai import Agent, Task
import config

class SummaryAgent:
    def __init__(self):
        self.tools = []  # No specific tools needed for summarization
    
    def get_agent(self):
        """Create and return the summary agent."""
        return Agent(
            role="Content Summarization Expert",
            goal="Create concise and informative summaries from structured document data",
            backstory=(
                "You are a professional document summarizer with a talent for distilling "
                "complex information into clear, concise summaries. You can identify the "
                "most important points and present them in a structured, readable format."
            ),
            verbose=True,
            allow_delegation=False,
            tools=[],  # No tools needed for summary agent
            llm='gemini/gemini-1.5-flash',
        )
    
    def get_task(self):
        """Create and return the summary task."""
        return Task(
            description=(
                "Using the structured information extracted by the Document Analysis Agent, "
                "create a comprehensive yet concise summary of the document content. "
                "This summary should capture the main points, key findings, and important relationships."
            ),
            expected_output=(
                "A well-structured summary that includes: "
                "1. An executive summary paragraph (3-5 sentences) "
                "2. Key findings and insights (bullet points) "
                "3. Main topics covered with brief descriptions "
                "4. Recommendations or next steps (if applicable based on content)"
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