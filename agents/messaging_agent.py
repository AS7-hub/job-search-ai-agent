from crewai import Agent, Task
from agents.llm_config import get_llm

def create_messaging_agent() -> Agent:
    """
    Creates and returns a CrewAI Agent acting as a Professional Networking and Outreach Specialist.
    """
    llm = get_llm()
    
    return Agent(
        role="Professional Networking and Outreach Specialist",
        goal="write personalized authentic outreach messages that get responses, avoiding generic templates, making every message feel handcrafted and specific",
        backstory="a professional networker who has placed 500+ candidates, knows generic LinkedIn messages get ignored, writes short specific human messages with 45% response rate (triple industry average), never uses cliche phrases like 'Hope this message finds you well'",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_messaging_task(agent: Agent, job_title: str, company: str, job_analysis: str, candidate_name: str) -> Task:
    """
    Creates a CrewAI Task instructing the messaging agent to draft three different 
    outreach messages tailored to the job and company.
    """
    description = (
        f"You are drafting outreach messages for {candidate_name} applying for the {job_title} role at {company}.\n\n"
        f"--- JOB ANALYSIS FOR CONTEXT ---\n{job_analysis}\n\n"
        "Draft exactly three tailored outreach messages:\n\n"
        "MESSAGE 1 — LinkedIn Connection Request (under 300 characters):\n"
        "- Mention the specific role.\n"
        "- Give one specific reason for interest.\n"
        "- Use zero generic phrases.\n\n"
        "MESSAGE 2 — LinkedIn Follow-Up (100-150 words, sent after connecting):\n"
        "- Brief intro.\n"
        "- Connect one of the candidate's skills to one specific company need from the job analysis.\n"
        "- Include a soft ask that opens conversation without being pushy.\n\n"
        "MESSAGE 3 — Cold Email (150-200 words):\n"
        "- Must include a catchy Subject Line.\n"
        "- Reference a specific company or role detail.\n"
        "- Provide 2-3 sentences on relevant experience.\n"
        "- End with a polite, clear call to action."
    )
    
    expected_output = (
        "Output the result with exactly three clearly separated and labeled sections ready to copy-paste:\n\n"
        "=== MESSAGE 1: LINKEDIN CONNECTION REQUEST ===\n"
        "[Text here]\n\n"
        "=== MESSAGE 2: LINKEDIN FOLLOW-UP ===\n"
        "[Text here]\n\n"
        "=== MESSAGE 3: COLD EMAIL ===\n"
        "[Subject Line]\n"
        "[Email Body here]"
    )
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
