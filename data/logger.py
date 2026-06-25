import json
import os
from datetime import datetime

# Path relative to where main.py will be executed from
LOG_FILE = "data/application_log.json"

def log_application(job_title: str, company: str, url: str, results: dict):
    """
    Logs a new application along with all generated outputs to a JSON file.
    """
    # 1. Check if the log file exists and load it, otherwise start an empty list
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        except json.JSONDecodeError:
            log_data = [] # In case the file exists but is empty or corrupted
    else:
        log_data = []
        
    # 2. Create the new entry dictionary
    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "job_title": job_title,
        "company": company,
        "url": url,
        "status": "Applied",
        "job_analysis": results.get("job_analysis", ""),
        "resume_cover_letter": results.get("resume_and_cover_letter", ""),
        "outreach_messages": results.get("outreach_messages", "")
    }
    
    # 3. Append the new entry to the array
    log_data.append(new_entry)
    
    # Ensure the data directory actually exists just in case
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # 4. Save the full list back to the JSON file with indent=2 for readability
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2)
        
    print(f"\n✅ Successfully logged application for {job_title} at {company} to {LOG_FILE}.")

def view_log():
    """
    Reads the application JSON log and prints a summary to the console.
    """
    # If the file doesn't exist, output the required message
    if not os.path.exists(LOG_FILE):
        print("No applications logged yet")
        return
        
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
    except json.JSONDecodeError:
        print("Error reading the log file. It might be corrupted.")
        return
        
    # Print the total number of applications
    print(f"\n--- Application Log ({len(log_data)} Total Applications) ---")
    
    # Print a summary for each entry
    for idx, entry in enumerate(log_data, 1):
        job_title = entry.get("job_title", "N/A")
        company = entry.get("company", "N/A")
        timestamp = entry.get("timestamp", "N/A")
        status = entry.get("status", "N/A")
        
        print(f"{idx}. {job_title} @ {company} | Applied on: {timestamp} | Status: {status}")
    
    print("-" * 60)
