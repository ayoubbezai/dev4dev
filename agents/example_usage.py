"""
Example usage of the updated PDF processing system with web scraping capabilities.
"""
from main import main
import os
import sys

def run_example():
    """
    Run the example with either a provided PDF path or a default example.
    """
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    if not pdf_path:
        print("No PDF path provided. Please provide a path to a PDF file:")
        print("python example_usage_updated.py /path/to/your/resume.pdf")
        return
    
    # Verify the file exists
    if not os.path.exists(pdf_path):
        print(f"Error: The file {pdf_path} does not exist.")
        return
    
    # Verify it's a PDF
    if not pdf_path.lower().endswith('.pdf'):
        print(f"Error: The file {pdf_path} is not a PDF file.")
        return
    
    print(f"Processing Resume PDF: {pdf_path}")
    print("This will analyze the resume, search for real opportunities online, and provide recommendations.")
    
    # Process the PDF and get results
    result = main(pdf_path)
    
    
    return result

if __name__ == "__main__":
    run_example()
