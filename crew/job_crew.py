from crewai import Crew, Process

# Import agents and tasks creation functions
from agents.job_analyzer import create_job_analyzer, create_analysis_task
from agents.resume_agent import create_resume_agent, create_resume_task
from agents.messaging_agent import create_messaging_agent, create_messaging_task

def run_job_crew(job_description: str, original_resume: str, job_title: str, company: str, candidate_name: str) -> dict:
    """
    Initializes and runs the CrewAI pipeline sequentially to analyze a job, 
    tailor a resume/cover letter, and draft outreach messages.
    """
    
    # 1. Initialize Agents
    print("Initializing Job Analyzer Agent...")
    analyzer_agent = create_job_analyzer()
    
    print("Initializing Resume Writer Agent...")
    resume_agent = create_resume_agent()
    
    print("Initializing Messaging Agent...")
    messaging_agent = create_messaging_agent()
    
    # 2. Create Tasks
    print("Creating Job Analysis Task...")
    task1 = create_analysis_task(
        agent=analyzer_agent, 
        job_description=job_description
    )
    
    print("Creating Resume & Cover Letter Task...")
    task2 = create_resume_task(
        agent=resume_agent,
        original_resume=original_resume,
        job_analysis="Use the output from the previous task as the job analysis",
        job_title=job_title,
        company=company
    )
    
    print("Creating Outreach Messaging Task...")
    task3 = create_messaging_task(
        agent=messaging_agent,
        job_title=job_title,
        company=company,
        job_analysis="Use the output from the previous task as the job analysis",
        candidate_name=candidate_name
    )
    
    # 3. Assemble the Crew
    print("Assembling the Job Search Crew...")
    job_crew = Crew(
        agents=[analyzer_agent, resume_agent, messaging_agent],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=True
    )
    
    # 4. Kick off the execution
    print("Kicking off the Job Search Crew process! This may take a few minutes as LLMs generate responses...")
    try:
        job_crew.kickoff()
        
        # 5. Return the separated task outputs
        # Using str(task.output) to safely extract the string content regardless of CrewAI internal versioning
        return {
            "job_analysis": str(task1.output) if task1.output else "No output",
            "resume_and_cover_letter": str(task2.output) if task2.output else "No output",
            "outreach_messages": str(task3.output) if task3.output else "No output"
        }
    except Exception as e:
        print(f"\n❌ Error during crew execution: {e}")
        return {
            "job_analysis": "",
            "resume_and_cover_letter": "",
            "outreach_messages": ""
        }
