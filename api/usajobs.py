import os
import requests
import traceback
from dotenv import load_dotenv

def fetch_jobs(keyword: str, location: str = "", results_per_page: int = 5) -> list:
    """
    Fetches job listings from the USAJOBS API based on keyword and location.
    
    Args:
        keyword (str): The search keyword (e.g., 'Data Analyst').
        location (str): The location for the job search (default is empty).
        results_per_page (int): Number of results to return (default is 5).
        
    Returns:
        list: A list of dictionaries containing job details.
    """
    try:
        # Load environment variables from .env file
        load_dotenv()
        
        # Retrieve API Key and User Agent from environment
        api_key = os.getenv("USAJOBS_API_KEY")
        user_agent = os.getenv("USAJOBS_USER_AGENT")
        
        # Handle the case where environment variables aren't set properly
        if not api_key or not user_agent:
            print("Error: USAJOBS_API_KEY or USAJOBS_USER_AGENT is missing from environment.")
            return []

        # Strip whitespace to avoid issues with spaces after = in .env
        api_key = api_key.strip()
        user_agent = user_agent.strip()

        # API Endpoint for USAJOBS
        url = "https://data.usajobs.gov/api/search"
        
        # Required headers for authentication
        headers = {
            "Authorization-Key": api_key,
            "User-Agent": user_agent,
            "Host": "data.usajobs.gov"
        }
        
        # Query parameters
        params = {
            "Keyword": keyword,
            "LocationName": location,
            "ResultsPerPage": results_per_page,
            "WhoMayApply": "All"
        }
        
        # Make the GET request to the USAJOBS API
        response = requests.get(url, headers=headers, params=params)
        
        # Handle errors gracefully
        if response.status_code != 200:
            print(f"Error fetching jobs: Status {response.status_code}")
            print(f"Response: {response.text}")
            if response.status_code == 401:
                raise Exception("401_UNAUTHORIZED")
            return []
            
        return _parse_response(response)

    except Exception as e:
        if str(e) == "401_UNAUTHORIZED":
            raise e
        print(f"An exception occurred while fetching jobs: {e}")
        print(traceback.format_exc())
        return []


def _parse_response(response) -> list:
    """Parses a successful USAJOBS API response into a list of job dicts."""
    data = response.json()
    search_results = data.get("SearchResult", {}).get("SearchResultItems", [])

    if len(search_results) == 0:
        print("API connected successfully but 0 jobs returned for this keyword")

    parsed_jobs = []
    for item in search_results:
        job_data = item.get("MatchedObjectDescriptor", {})

        title = job_data.get("PositionTitle", "N/A")
        organization = job_data.get("OrganizationName", "N/A")
        location_display = job_data.get("PositionLocationDisplay", "N/A")
        job_url = job_data.get("PositionURI", "N/A")
        close_date = job_data.get("ApplicationCloseDate", "N/A")

        salary_min = "N/A"
        salary_max = "N/A"
        remuneration = job_data.get("PositionRemuneration", [])
        if remuneration and len(remuneration) > 0:
            salary_min = remuneration[0].get("MinimumRange", "N/A")
            salary_max = remuneration[0].get("MaximumRange", "N/A")

        # Extract detailed description (UserArea > Details > JobSummary)
        description = job_data.get("UserArea", {}).get("Details", {}).get("JobSummary", "N/A")

        parsed_jobs.append({
            "title": title,
            "organization": organization,
            "location": location_display,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "description": description,
            "url": job_url,
            "close_date": close_date
        })

    return parsed_jobs


# Test block
if __name__ == "__main__":
    print("Testing fetch_jobs for 'Data Analyst'...\n")
    jobs = fetch_jobs(keyword="Data Analyst")
    if jobs:
        print(f"\nSUCCESS: Got {len(jobs)} jobs!")
        for idx, job in enumerate(jobs, start=1):
            print(f"{idx}. {job['title']} @ {job['organization']}")
    else:
        print("\nFAILED: No jobs returned.")
