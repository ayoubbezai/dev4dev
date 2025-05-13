# Resume Opportunity Matcher

A framework for processing resumes (PDF) and automatically matching them to suitable internship opportunities using CrewAI, LangChain, and Google's Gemini AI.

## Project Overview

This application analyzes a candidate's resume (in PDF format), extracts structured information about their skills, education, and experience, and then searches for real-world internship opportunities that match their profile. The system uses a team of AI agents working together through the CrewAI framework, with Gemini AI powering the underlying intelligence.

## Main Features

- **PDF Resume Analysis**: Extract structured information from PDF resumes
- **Web Scraping Integration**: Find real-world internship opportunities from online sources
- **Intelligent Matching**: Match candidate profiles to suitable internships based on skills, education, and interests
- **Multiple Interfaces**:
  - Web API through Flask
  - GUI desktop application
  - Command-line interface

## Project Structure

```
.
├── .env                    # Environment variables and API keys
├── app.py                  # Flask web service
├── config.py               # Configuration settings
├── example_usage.py        # CLI example usage script
├── gui_app.py              # Desktop GUI application
├── main.py                 # Core processing logic
├── requirements.txt        # Project dependencies
├── render.yaml             # Render.com deployment configuration
├── agents/                 # AI agent definitions
│   ├── __init__.py
│   ├── document_analysis_agent.py  # Analyzes PDF content
│   ├── summary_agent.py            # Creates concise summaries
│   ├── web_scraper_agent.py        # Searches for internship opportunities
│   └── matching_agent.py           # Matches profiles to internships
└── tools/                  # Tool definitions
    ├── __init__.py
    ├── base_tool.py
    ├── pdf_parser.py       # Extracts text from PDF files
    ├── pdf_processor.py    # Processes extracted PDF text
    └── information_extractor.py  # Extracts structured information
```

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your environment variables by creating a `.env` file with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   LAMA_API_KEY=your_lama_api_key_here_if_needed
   ```

## Usage Options

### Web API (Flask)

Start the Flask server:

```bash
python app.py
```

Then send POST requests to the `/process-pdf` endpoint with a PDF file in the `file` field of a multipart/form-data request.

Health check endpoint is available at `/health`.

### GUI Application

Launch the desktop application:

```bash
python gui_app.py
```

The GUI allows you to:
1. Browse and select a resume PDF
2. Process the resume with one click
3. View and save results

### Command Line

Process a resume PDF directly:

```bash
python example_usage.py path/to/your/resume.pdf
```

### API Integration

Import and use in your Python code:

```python
from main import main

# Process a resume PDF
result = main("path/to/resume.pdf")
print(result)
```

## Agent Workflow

1. **Document Analysis Agent**: Analyzes the PDF content and extracts structured information
2. **Summary Agent**: Creates a concise summary of the extracted information
3. **Web Scraper Agent**: Searches online sources for relevant internship opportunities
4. **Matching Agent**: Matches the candidate profile to the most suitable internships

## Deployment

The application can be deployed to Render.com using the provided `render.yaml` configuration file.

## Requirements

- Python 3.8+
- Google API key with access to Gemini models
- CrewAI, LangChain, and other dependencies listed in requirements.txt

## License

University of Batna 2
