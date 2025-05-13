"""
Agent responsible for scraping websites like LinkedIn for internship opportunities.
"""
from crewai import Agent, Task
import config
import json
import re
from urllib.parse import quote

class WebScraperAgent:
    def __init__(self):
        self.tools = []  # Will use built-in requests library
        
    def get_agent(self):
        """Create and return the web scraper agent."""
        return Agent(
            role="Web Research Specialist",
            goal="Find real-world internship opportunities from online sources",
            backstory=(
                "You are an expert web researcher specialized in finding educational and "
                "career opportunities. With extensive experience in navigating employment "
                "platforms, you excel at discovering relevant internship "
                "opportunities that match specific candidate profiles."
            ),
            verbose=True,
            allow_delegation=False,
            llm='gemini/gemini-1.5-flash',
        )
    
    def get_task(self):
        """Create and return the web scraping task."""
        return Task(
            description=(
                "Using the candidate profile information extracted by the Document Analysis Agent, "
                "research and find real internship opportunities that match the candidate's "
                "skills, education, and interests. Use LinkedIn and job boards to find current opportunities."
            ),
            expected_output=(
                "A JSON structure containing: "
                "A list of 8-10 internship opportunities with title, company, location, and requirements. "
                "Each entry should include a source URL."
            ),
            agent=self.get_agent()
        )
    
    def search_linkedin_internships(self, profile_data):
        """
        Search LinkedIn for internships matching the candidate's profile.
        
        Args:
            profile_data: JSON structure containing candidate information
            
        Returns:
            List of internship opportunities found on LinkedIn
        """
        try:
            # Parse profile data if it's a string
            if isinstance(profile_data, str):
                profile = json.loads(profile_data)
            else:
                profile = profile_data
                
            # Extract relevant profile information
            skills = profile.get("skills", [])
            if isinstance(skills, str):
                skills = [skill.strip() for skill in skills.split(",")]
                
            education = profile.get("education", {})
            if isinstance(education, list):
                majors = [edu.get("field_of_study", "") for edu in education]
            else:
                majors = [education.get("field_of_study", "")]
            
            # Combine skills and majors for search terms
            search_terms = skills + majors
            
            # Simulate LinkedIn search results
            # In a real implementation, this would use web scraping or LinkedIn API
            print(f"Searching for internships matching: {', '.join(search_terms[:3])}")
            
            # Simulate an API call or web scraping
            results = self._simulate_linkedin_search(search_terms[:3])
            
            return results
            
        except Exception as e:
            return [{"error": f"LinkedIn search failed: {str(e)}"}]
    
    def _simulate_linkedin_search(self, search_terms):
        """
        Simulate LinkedIn search results for demonstration purposes.
        In a real implementation, this would use web scraping or LinkedIn API.
        """
        # Construct a query string from search terms
        query = "+".join([quote(term) for term in search_terms])
        base_url = "https://www.linkedin.com/jobs/search/?keywords="
        
        # Simulated search results based on provided terms
        simulated_results = []
        
        # Generate 10 diverse internship opportunities
        job_titles = [
            "Software Engineering Intern", 
            "Data Science Intern", 
            "Marketing Intern",
            "UX/UI Design Intern", 
            "Business Development Intern",
            "Research Assistant", 
            "Product Management Intern",
            "Content Creation Intern", 
            "IT Support Intern",
            "Finance Intern"
        ]
        
        companies = [
            "Google", "Microsoft", "Amazon", "Meta", "Apple",
            "IBM", "Deloitte", "Goldman Sachs", "Tesla", "Spotify"
        ]
        
        locations = [
            "Remote", "New York, NY", "San Francisco, CA", "Austin, TX", 
            "Seattle, WA", "Boston, MA", "Chicago, IL", "Los Angeles, CA"
        ]
        
        for i in range(10):
            job_index = i % len(job_titles)
            company_index = i % len(companies)
            location_index = i % len(locations)
            
            # Create more realistic URLs
            job_id = 1000 + i
            company_slug = companies[company_index].lower().replace(" ", "-")
            
            internship = {
                "title": job_titles[job_index],
                "company": companies[company_index],
                "location": locations[location_index],
                "description": f"Exciting opportunity to work at {companies[company_index]} and gain hands-on experience in {job_titles[job_index].split(' ')[0]}.",
                "requirements": [search_terms[i % len(search_terms)], "Communication skills", "Problem-solving", "Teamwork"],
                "url": f"https://www.linkedin.com/jobs/view/{job_id}/",
                "source": "LinkedIn"
            }
            simulated_results.append(internship)
        
        return simulated_results