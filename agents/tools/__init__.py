"""
Imports and exports for the tools module.
"""
from .pdf_processor import PDFContentProcessor
from .information_extractor import InformationExtractor
from .pdf_parser import PDFParser

# Import LlamaIndexParserTool conditionally if config has LAMA_API_KEY
import config
if hasattr(config, 'LAMA_API_KEY') and config.LAMA_API_KEY:
    try:
        from .pdf_parser import LlamaIndexParserTool
        __all__ = ['PDFContentProcessor', 'InformationExtractor', 'PDFParser', 'LlamaIndexParserTool']
    except ImportError:
        __all__ = ['PDFContentProcessor', 'InformationExtractor', 'PDFParser']
else:
    __all__ = ['PDFContentProcessor', 'InformationExtractor', 'PDFParser']