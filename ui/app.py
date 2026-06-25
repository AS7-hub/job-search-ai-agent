import streamlit as st
import sys
import os

# Add the parent directory to sys.path so we can import from api, crew, and data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.usajobs import fetch_jobs
from crew.job_crew import run_job_crew
from data.logger import log_application

# PAGE CONFIG
st.set_page_config(page_title="AI Job Application Assistant", page_icon="🤖", layout="wide")

# SIDEBAR (left panel)
with st.sidebar:
    st.header("Your Details")
    candidate_name = st.text_input("Candidate Name")
    resume_text = st.text_area("Paste your resume here", height=300)
    
    st.subheader("Job Search")
    keyword = st.text_input("Job Keyword")
    location = st.text_input("Location (Optional)")
    results_count = st.slider("Number of Results", min_value=1, max_value=10, value=5)
    
    search_clicked = st.button("Search Jobs", type="primary")

# Initialize session state for storing jobs
if "jobs" not in st.session_state:
    st.session_state.jobs = []

# MAIN AREA Logic for Searching
if search_clicked:
    if not keyword.strip():
        st.error("Please enter a Job Keyword.")
    else:
        with st.spinner("Fetching jobs..."):
            try:
                jobs = fetch_jobs(keyword=keyword, location=location, results_per_page=results_count)
                st.session_state.jobs = jobs
                if jobs:
                    st.success(f"Found {len(jobs)} jobs successfully!")
                else:
                    st.warning("No jobs found matching your criteria.")
            except Exception as e:
                if str(e) == "401_UNAUTHORIZED":
                    st.error("API Authentication failed — check your USAJOBS_API_KEY and USAJOBS_USER_AGENT email in your .env file")
                else:
                    st.error(f"An error occurred: {e}")

# Main Area Logic for Displaying and Selecting Jobs
if st.session_state.jobs:
    st.subheader("Available Positions")
    
    # Create dropdown options formatted as "Title — Organization"
    job_options = [f"{job['title']} — {job['organization']}" for job in st.session_state.jobs]
    
    # Use selectbox to let user pick one of the options
    selected_idx = st.selectbox("Select a job:", range(len(job_options)), format_func=lambda x: job_options[x])
    selected_job = st.session_state.jobs[selected_idx]
    
    # Job Details Expander
    with st.expander("View Job Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Title:** {selected_job['title']}")
            st.write(f"**Organization:** {selected_job['organization']}")
            st.write(f"**Location:** {selected_job['location']}")
        with col2:
            st.write(f"**Salary Range:** {selected_job['salary_min']} - {selected_job['salary_max']}")
            st.write(f"**Close Date:** {selected_job['close_date']}")
            st.write(f"**Link:** [USAJOBS Posting]({selected_job['url']})")
            
        st.write("---")
        desc = selected_job['description']
        # Show only first 800 characters
        truncated_desc = desc[:800] + "..." if len(desc) > 800 else desc
        st.write(truncated_desc)
        
    st.write("") # Some vertical spacing
    generate_clicked = st.button("Generate Application Materials", type="primary")
    
    # Generation Logic
    if generate_clicked:
        # Validations
        if not candidate_name.strip():
            st.error("Please enter your Candidate Name in the sidebar.")
        elif not resume_text.strip():
            st.error("Please paste your resume in the sidebar.")
        else:
            results = None
            with st.spinner("AI Crew is working... This takes 1-2 minutes"):
                try:
                    results = run_job_crew(
                        job_description=selected_job['description'],
                        original_resume=resume_text,
                        job_title=selected_job['title'],
                        company=selected_job['organization'],
                        candidate_name=candidate_name
                    )
                except Exception as e:
                    st.error(f"An error occurred during generation: {e}")
                
            # If results were successfully generated and not overridden by the catch block returning empty
            if results and results.get("job_analysis"):
                st.success("Generation Complete!")
                
                # Display Results in Tabs
                tab1, tab2, tab3 = st.tabs(["Job Analysis", "Resume and Cover Letter", "Outreach Messages"])
                
                with tab1:
                    st.markdown(results.get("job_analysis", "No job analysis generated."))
                    
                with tab2:
                    rc_content = results.get("resume_and_cover_letter", "No resume/cover letter generated.")
                    st.markdown(rc_content)
                    
                    # File download
                    safe_title = selected_job['title'].replace(' ', '_').replace('/', '_')
                    st.download_button(
                        label="Download Resume and Cover Letter",
                        data=rc_content,
                        file_name=f"{safe_title}_materials.txt",
                        mime="text/plain"
                    )
                    
                with tab3:
                    outreach_content = results.get("outreach_messages", "No outreach messages generated.")
                    st.markdown(outreach_content)
                    
                    # File download
                    st.download_button(
                        label="Download Outreach Messages",
                        data=outreach_content,
                        file_name=f"{safe_title}_outreach.txt",
                        mime="text/plain"
                    )
                    
                # Log to JSON
                log_application(
                    job_title=selected_job['title'],
                    company=selected_job['organization'],
                    url=selected_job['url'],
                    results=results
                )
                
                st.info("Application logged successfully.")
            elif results:
                # If it returned empty strings from the except block in job_crew.py
                st.error("The AI generation failed. Please check the terminal logs.")
