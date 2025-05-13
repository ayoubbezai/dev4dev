"""
Tool for parsing PDF files and extracting their content for analysis.
"""
from langchain.tools import BaseTool
from pypdf import PdfReader
import os
import io
import config
from typing import Union, BinaryIO

class PDFParser(BaseTool):
    name: str = "PDFParser"
    description: str = (
        "A tool for parsing PDF files and extracting their content. "
        "Use this tool when you need to extract text from a PDF file. "
        "Input should be a file path or file object containing a PDF."
    )
    
    def _run(self, input_data: Union[str, BinaryIO]) -> str:
        """
        Parse a PDF file and extract its text content.
        Input can be either a file path (string) or a file-like object.
        """
        try:
            # Handle input as either a file path or a file-like object
            if isinstance(input_data, str):
                # Check if the input is a valid file path
                if os.path.exists(input_data) and input_data.lower().endswith('.pdf'):
                    pdf_file = input_data
                else:
                    return f"Error: The provided path '{input_data}' is not a valid PDF file."
            else:
                # Assume input_data is a file-like object
                pdf_file = input_data
            
            # Extract text from the PDF
            extracted_text = self._extract_text_from_pdf(pdf_file)
            
            if not extracted_text:
                return "Warning: No text content was extracted from the PDF."
            
            return extracted_text
            
        except Exception as e:
            return f"PDF parsing failed: {str(e)}"
    
    def _extract_text_from_pdf(self, pdf_file: Union[str, BinaryIO]) -> str:
        """
        Extract text from a PDF file using PyPDF.
        """
        reader = PdfReader(pdf_file)
        text_content = []
        
        # Extract text from each page
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_content.append(f"--- Page {page_num + 1} ---\n{page_text}")
        
        return "\n\n".join(text_content)
    
    def parse_pdf(self, pdf_file: Union[str, BinaryIO]) -> str:
        """
        Public method to parse PDF directly without using the tool interface.
        """
        return self._run(pdf_file)


# For LlamaParse integration (if LAMA_API_KEY is provided)
if hasattr(config, 'LAMA_API_KEY') and config.LAMA_API_KEY:
    try:
        from llama_parse import LlamaParse
        
        class LlamaIndexParserTool(BaseTool):
            name: str = "LlamaIndexParserTool"
            description: str = "Parses PDF files using LlamaParse and returns clean text for analysis."
            
            def __init__(self):
                self.parser = LlamaParse(
                    api_key=config.LAMA_API_KEY,
                    result_type=getattr(config, 'result_type', 'text'),
                    verbose=True,
                )
            
            def _run(self, file_path: str) -> str:
                """Run the LlamaParse tool on a given file path."""
                documents = self.parser.load_data(file_path)
                return "\n".join([doc.text for doc in documents])
            
            def parse_pdf(self, file_path: str) -> str:
                """
                Public method to parse PDF directly without using the tool interface.
                """
                return self._run(file_path)
    
    except ImportError:
        print("LlamaParse not installed. Only using PyPDF parser.")