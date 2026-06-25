from crewai import Agent, Task
from agents.llm_config import get_llm

def create_resume_agent() -> Agent:
    """
    Creates and returns a CrewAI Agent acting as a Professional Resume Writer and Career Coach.
    """
    llm = get_llm()
    
    return Agent(
        role="Professional Resume Writer and Career Coach",
        goal="create ATS-optimized tailored resumes and cover letters that maximize interview callbacks by matching candidate experience to job requirements",
        backstory="a certified professional resume writer with 94% client interview rate who reframes real experience using employer language, never fabricates anything, and understands ATS deeply",
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_resume_task(agent: Agent, original_resume: str, job_analysis: str, job_title: str, company: str) -> Task:
    """
    Creates a CrewAI Task instructing the resume agent to craft a tailored resume
    and cover letter based on the original resume and the job analysis insights.
    """
    
    description = (
        f"You are writing a resume and cover letter for the position of {job_title} at {company}.\n\n"
        f"--- ORIGINAL RESUME ---\n{original_resume}\n\n"
        f"--- JOB ANALYSIS ---\n{job_analysis}\n\n"
        "Your task consists of two parts:\n\n"
        "PART A - TAILORED RESUME:\n"
        "- Rewrite the professional summary (3-4 lines) for this specific role.\n"
        "- Reorder bullet points to highlight relevant experience first.\n"
        "- Insert top ATS keywords naturally into existing bullet points.\n"
        "- Add a Core Competencies section with matched skills.\n"
        "- Never fabricate — only reframe and reorder real experience.\n\n"
        "PART B - COVER LETTER (under 300 words):\n"
        "- Para 1: Hook — why this specific company and role.\n"
        "- Para 2: Match — connect top 3 achievements to top 3 needs.\n"
        "- Para 3: Confident call to action."
    )
    
    expected_output = (
        "Output the result with exactly two clearly separated sections using these exact headers:\n\n"
        "=== TAILORED RESUME ===\n"
        "[Insert Tailored Resume Here]\n\n"
        "=== COVER LETTER ===\n"
        "[Insert Cover Letter Here]"
    )
    
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
