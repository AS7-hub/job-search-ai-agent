from crewai import Agent, Task
from agents.llm_config import get_llm

def create_job_analyzer() -> Agent:
    """
    Creates and returns a CrewAI Agent acting as a Senior Job Market Analyst.
    """
    # Retrieve our initialized Language Model
    llm = get_llm()
    
    # Initialize the CrewAI Agent with specific persona settings
    return Agent(
        role="Senior Job Market Analyst",
        goal="analyze job descriptions and extract requirements, skills, ATS keywords, and insights that help candidates tailor applications",
        backstory="an expert HR consultant with 15 years experience who understands ATS systems, knows which keywords matter, and can identify non-negotiable vs nice-to-have requirements",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_analysis_task(agent: Agent, job_description: str) -> Task:
    """
    Creates and returns a CrewAI Task that instructs the job analyzer agent
    to perform a detailed extraction on a specific job description.
    """
    # Define exactly what we want the Agent to do based on the input text
    description = (
        "Analyze the following job description and extract detailed insights.\n\n"
        "Job Description:\n"
        f"{job_description}\n\n"
        "Please extract and provide the following:\n"
        "1. Top 10 required technical skills\n"
        "2. Top 5 soft skills\n"
        "3. Years of experience required\n"
        "4. Education requirements\n"
        "5. Top 15 ATS keywords\n"
        "6. 3 most critical responsibilities\n"
        "7. Company culture signals\n"
        "8. Any red flags or unclear requirements"
    )
    
    # Define what the result format should look like
    expected_output = (
        "A structured report with clearly labeled sections for technical skills, soft skills, "
        "experience, education, ATS keywords, responsibilities, culture signals, and red flags "
        "so that other agents can easily read and use this information."
    )
    
    # Initialize and return the CrewAI Task bound to our specific agent
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
