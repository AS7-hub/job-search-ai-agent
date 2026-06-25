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
        # 1. Load environment variables from .env file
        load_dotenv()
        
        # 2. Retrieve API Key and User Agent from environment
        api_key = os.getenv("USAJOBS_API_KEY")
        user_agent = os.getenv("USAJOBS_USER_AGENT")
        
        # DEBUG LOGGING 1
        if api_key:
            print("API Key found: YES")
        else:
            print("API Key found: NO - CHECK .env")
        
        # Handle the case where environment variables aren't set properly
        if not api_key or not user_agent:
            print("Error: USAJOBS_API_KEY or USAJOBS_USER_AGENT is missing from environment.")
            return []

        api_key = api_key.strip()
        user_agent = user_agent.strip()

        # API Endpoint for USAJOBS
        url = "https://data.usajobs.gov/api/search"
        
        # 3. Required headers for authentication
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
            "WhoMayApply": "All",
            "api_key": api_key # added as backup
        }
        
        # Print exact headers (mask key)
        masked_key = api_key[:4] + "***" if len(api_key) > 4 else "***"
        print(f"DEBUG HEADERS: {{'Authorization-Key': '{masked_key}', 'User-Agent': '{user_agent}', 'Host': 'data.usajobs.gov'}}")
        
        # Make the GET request to the USAJOBS API
        response = requests.get(url, headers=headers, params=params)
        
        # DEBUG LOGGING 2
        print(f"Called URL: {response.url}")
        print(f"Status Code: {response.status_code}")
        
        # 401 Retry Logic
        if response.status_code == 401:
            print("Received 401. Falling back to public test endpoint...")
            fallback_url = "https://data.usajobs.gov/api/search"
            fallback_params = {
                "Keyword": "Engineer",
                "ResultsPerPage": 3
            }
            fallback_headers = {
                "Authorization-Key": api_key,
                "User-Agent": user_agent
            }
            response = requests.get(fallback_url, headers=fallback_headers, params=fallback_params)
            print(f"Fallback URL: {response.url}")
            print(f"Fallback Status Code: {response.status_code}")
            if response.status_code == 401:
                raise Exception("401_UNAUTHORIZED")
        
        # Handle errors gracefully: check if the request was successful
        if response.status_code != 200:
            print(f"Error fetching jobs: Received status code {response.status_code}")
            print(f"Response Details: {response.text}")
            return []
            
        data = response.json()
        
        # Extract the search results array
        search_results = data.get("SearchResult", {}).get("SearchResultItems", [])
        
        # DEBUG LOGGING 3
        if len(search_results) == 0:
            print("API connected successfully but 0 jobs returned for this keyword")
            
        parsed_jobs = []
        for item in search_results:
            job_data = item.get("MatchedObjectDescriptor", {})
            
            # Extract basic information
            title = job_data.get("PositionTitle", "N/A")
            organization = job_data.get("OrganizationName", "N/A")
            location_display = job_data.get("PositionLocationDisplay", "N/A")
            job_url = job_data.get("PositionURI", "N/A")
            close_date = job_data.get("ApplicationCloseDate", "N/A")
            
            # Extract salary information from the first remuneration item (PositionRemuneration[0])
            salary_min = "N/A"
            salary_max = "N/A"
            remuneration = job_data.get("PositionRemuneration", [])
            if remuneration and len(remuneration) > 0:
                salary_min = remuneration[0].get("MinimumRange", "N/A")
                salary_max = remuneration[0].get("MaximumRange", "N/A")
                
            # Extract detailed description (UserArea > Details > JobSummary)
            description = job_data.get("UserArea", {}).get("Details", {}).get("JobSummary", "N/A")
            
            # Append the structured dictionary to our list
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
            
        # Return the final parsed list
        return parsed_jobs

    except Exception as e:
        print(f"An exception occurred while fetching jobs: {e}")
        if str(e) == "401_UNAUTHORIZED":
            raise e
        print(traceback.format_exc())
        return []

# Test block
if __name__ == "__main__":
    print("Testing fetch_jobs for 'Data Analyst'...\n")
    
    # Perform search
    jobs = fetch_jobs(keyword="Data Analyst")
    
    # Print out results
    if jobs:
        for idx, job in enumerate(jobs, start=1):
            print(f"{idx}. {job['title']}")
            print(f"   Organization: {job['organization']}")
            print("-" * 50)
    else:
        print("No jobs found or there was an error during the API request.")
