"""
Main entry point for the CrewAI application.
"""
import sys
import os
from crewai import Crew
import json

# Import agents and tools
from agents import DocumentAnalysisAgent, SummaryAgent
from agents.matching_agent import MatchingAgent
from agents.web_scraper_agent import WebScraperAgent  
from tools import PDFContentProcessor, PDFParser

def main(pdf_path_or_content=None):
    """
    Main function to process PDF and run the CrewAI system.
    
    Args:
        pdf_path_or_content: Either a path to a PDF file or the extracted PDF content
    
    Returns:
        The result from the crew execution - top 3 internship matches
    """
    if pdf_path_or_content is None:
        pdf_path_or_content = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not pdf_path_or_content:
        print("Please provide a PDF file path or extracted PDF content as an argument.")
        return
    
    is_file_path = isinstance(pdf_path_or_content, str) and (
        pdf_path_or_content.lower().endswith('.pdf') and 
        os.path.exists(pdf_path_or_content)
    )
    
    if is_file_path:
        pdf_parser = PDFParser()
        pdf_content = pdf_parser.parse_pdf(pdf_path_or_content)
        print(f"Successfully parsed PDF: {pdf_path_or_content}")
    else:
        pdf_content = pdf_path_or_content
    
    pdf_processor = PDFContentProcessor()
    
    # Process the PDF content
    processed_content = pdf_processor.process_content(pdf_content)
    
    # Create agents
    doc_analysis_agent = DocumentAnalysisAgent(pdf_content=processed_content)
    summary_agent = SummaryAgent()
    web_scraper_agent = WebScraperAgent()
    matching_agent = MatchingAgent()
    
    # Create crew
    document_crew = Crew(
        agents=[
            doc_analysis_agent.get_agent(), 
            summary_agent.get_agent(),
            web_scraper_agent.get_agent(),
            matching_agent.get_agent()
        ],
        tasks=[
            doc_analysis_agent.get_task(),
            summary_agent.get_task(),
            web_scraper_agent.get_task(),
            matching_agent.get_task()
        ],
        verbose=True
    )
    
    # Start the crew
    result = document_crew.kickoff()
    
    # Print only the top 3 internships in the specified format
    print("\n\n=== Top 3 Internship Matches ===")
    print(result)
    
    # Return the result as a string for JSON serialization
    return str(result)

if __name__ == "__main__":
    main()
