"""
Tool for processing PDF content and preparing it for analysis.
"""
from langchain.tools import BaseTool
from langchain.text_splitter import RecursiveCharacterTextSplitter
import config

class PDFContentProcessor(BaseTool):
    name: str = "PDFContentProcessor"
    description: str = (
        "A tool for processing and structuring extracted PDF content. "
        "Use this tool when you need to prepare PDF text for analysis. "
        "Input should be the raw text extracted from a PDF."
    )
    
    def _run(self, pdf_content: str) -> str:
        """
        Process the PDF content by splitting it into manageable chunks and 
        ensuring it is properly formatted for analysis.
        """
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.PDF_CHUNK_SIZE,
            chunk_overlap=config.PDF_CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Split the content into chunks
        chunks = text_splitter.split_text(pdf_content)
        
        # Process each chunk (basic cleanup)
        processed_chunks = []
        for chunk in chunks:
            # Basic cleaning
            cleaned_chunk = chunk.strip()
            if cleaned_chunk:
                processed_chunks.append(cleaned_chunk)
        
        # Join the chunks back together with appropriate markers
        processed_content = "\n\n--- SECTION BREAK ---\n\n".join(processed_chunks)
        
        return processed_content
    
    def process_content(self, pdf_content: str) -> str:
        """
        Public method to process PDF content directly without using the tool interface.
        """
        return self._run(pdf_content)