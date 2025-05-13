"""
Tool for extracting structured information from text content.
"""
from langchain.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import config

class InformationExtractor(BaseTool):
    name: str = "InformationExtractor"
    description: str = (
        "A tool for extracting structured information from text content. "
        "Use this tool when you need to identify and extract specific information "
        "like entities, topics, facts, or relationships from document text. "
        "Input should be the text content and specifications about what to extract."
    )
    
    def _run(self, input_data: str) -> str:
        """
        Extract specified information from the provided text.
        Input should be a JSON string with 'content' and 'extraction_type' fields.
        """
        try:
            # Parse the input JSON
            if isinstance(input_data, str):
                try:
                    data = json.loads(input_data)
                except json.JSONDecodeError:
                    # If input is not valid JSON, assume it's just text content
                    data = {
                        "content": input_data,
                        "extraction_type": "general"  # Default to general extraction
                    }
            else:
                data = input_data
            
            content = data.get("content", "")
            extraction_type = data.get("extraction_type", "general")
            
            # Initialize Gemini model
            llm = ChatGoogleGenerativeAI(
                model=config.GEMINI_MODEL,
                google_api_key=config.GOOGLE_API_KEY,
                temperature=0.2  # Lower temperature for more deterministic extraction
            )
            
            # Create an appropriate prompt based on extraction type
            if extraction_type == "entities":
                prompt = f"""
                Extract all named entities from the following text. Include people, organizations, 
                locations, dates, and other named entities. Format the output as JSON.
                
                TEXT: {content}
                
                Output format example:
                {{
                    "people": ["Name1", "Name2", ...],
                    "organizations": ["Org1", "Org2", ...],
                    "locations": ["Location1", "Location2", ...],
                    "dates": ["Date1", "Date2", ...],
                    "other_entities": ["Entity1", "Entity2", ...]
                }}
                """
            elif extraction_type == "topics":
                prompt = f"""
                Identify the main topics and themes in the following text. 
                For each topic, provide a brief description. Format the output as JSON.
                
                TEXT: {content}
                
                Output format example:
                {{
                    "topics": [
                        {{"name": "Topic1", "description": "Description of Topic1"}},
                        {{"name": "Topic2", "description": "Description of Topic2"}},
                        ...
                    ]
                }}
                """
            else:  # general extraction
                prompt = f"""
                Extract structured information from the following text. Include:
                1. Key entities (people, organizations, locations)
                2. Main topics or themes
                3. Important facts or data points
                4. Relationships between entities
                5. Any time-sensitive information or dates
                
                Format the output as a detailed JSON structure.
                
                TEXT: {content}
                """
            
            # Get the response from the LLM
            response = llm.invoke(prompt)
            extraction_result = response.content
            
            # Ensure the response is valid JSON
            try:
                json.loads(extraction_result)
                return extraction_result
            except json.JSONDecodeError:
                # If not valid JSON, wrap the text in a JSON structure
                return json.dumps({"extracted_information": extraction_result})
                
        except Exception as e:
            return json.dumps({"error": f"Information extraction failed: {str(e)}"})