"""
Agent responsible for matching extracted profile information to suitable internships.
"""
from crewai import Agent, Task
import config
import json
from .web_scraper_agent import WebScraperAgent

class MatchingAgent:
    def __init__(self):
        self.tools = []  # No specific external tools needed for matching
        self.web_scraper = WebScraperAgent()  # Initialize the web scraper agent
    
    def get_agent(self):
        """Create and return the matching agent."""
        return Agent(
            role="Internship Matching Specialist",
            goal="Match student profiles to suitable internships",
            backstory=(
                "You are an expert in career development and educational opportunities. "
                "With years of experience in academic advising and career counseling, "
                "you excel at matching student profiles to relevant internships "
                "that align with their skills, interests, and career goals. "
                "You work with real-time data from various online sources to find "
                "the most current and relevant opportunities."
            ),
            verbose=True,
            allow_delegation=True,  # Allow delegation to web scraper agent
            llm='gemini/gemini-1.5-flash',
        )
    
    def get_task(self):
        """Create and return the matching task."""
        return Task(
            description=(
                "Using the structured information extracted by the Document Analysis Agent "
                "and processed by the Summary Agent, identify and suggest the 3 most suitable "
                "internships for this candidate. Work with the Web Scraper Agent to "
                "find real opportunities that match the candidate's profile. Focus on matching their "
                "skills, education, experience, and interests to appropriate opportunities."
            ),
            expected_output=(
                "A simple list of the top 3 internship opportunities in the following format:\n\n"
                "1- [Company Name]\n"
                "[Internship Title]\n"
                "link: [URL]\n\n"
                "2- [Company Name]\n"
                "[Internship Title]\n"
                "link: [URL]\n\n"
                "3- [Company Name]\n"
                "[Internship Title]\n"
                "link: [URL]"
            ),
            agent=self.get_agent()
        )
    
    def match_profile_to_opportunities(self, profile_data):
        """
        Match the candidate profile to suitable internships using web scraping.
        
        Args:
            profile_data: JSON structure containing candidate information
            
        Returns:
            String with top 3 internship matches formatted for direct output
        """
        try:
            # Get internship opportunities from LinkedIn
            internships = self.web_scraper.search_linkedin_internships(profile_data)
            
            # Calculate match scores
            scored_internships = self._score_internship_matches(internships, profile_data)
            
            # Get top 3 internships
            top_internships = scored_internships[:3]
            
            # Format the results according to the required format
            result = ""
            for i, internship in enumerate(top_internships, 1):
                result += f"{i}- {internship['company']}\n"
                result += f"{internship['title']}\n"
                result += f"link: {internship['url']}\n\n"
            
            # Remove the last newline if present
            result = result.rstrip("\n")
            
            return result
                
        except Exception as e:
            return f"Error finding internship matches: {str(e)}"
    
    def _score_internship_matches(self, internships, profile_data):
        """Score internship opportunities based on profile match."""
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
                
            interests = profile.get("interests", [])
            if isinstance(interests, str):
                interests = [interest.strip() for interest in interests.split(",")]
            
            # Score each internship
            scored_internships = []
            for internship in internships:
                score = 0
                
                # Check for skill matches
                if "requirements" in internship:
                    for skill in skills:
                        if any(skill.lower() in req.lower() or req.lower() in skill.lower() 
                               for req in internship["requirements"]):
                            score += 2
                
                # Check for field of study match
                if "description" in internship:
                    for major in majors:
                        if major.lower() in internship["description"].lower():
                            score += 3
                
                # Check for interest match
                for interest in interests:
                    if "description" in internship and interest.lower() in internship["description"].lower():
                        score += 1
                
                internship["match_score"] = score
                scored_internships.append(internship)
            
            # Sort by score and return
            return sorted(scored_internships, key=lambda x: x.get("match_score", 0), reverse=True)
            
        except Exception as e:
            return [{"error": f"Internship scoring failed: {str(e)}"}]