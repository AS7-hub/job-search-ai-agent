# AI Job Application Assistant

This multi-agent job search system automates the tedious parts of applying to jobs on USAJOBS. It uses specialized AI agents to search for active roles, thoroughly analyze job requirements, craft customized ATS-optimized resumes and cover letters, and generate personalized outreach messages. 

## Tech Stack
- **Python 3**
- **CrewAI & LangChain**: For building and orchestrating the multi-agent AI pipeline.
- **Google Gemini (1.5 Flash)**: Language model used for analysis and generation.
- **Streamlit**: For the interactive web application interface.
- **USAJOBS API**: For live job search integration.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd "Multi-Agent Job Search System with CrewAI"
   ```

2. **Create and activate a virtual environment:**
   *Windows:*
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
   *Mac/Linux:*
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Environment Variables:**
   > **Note:** The `.env` file is explicitly ignored by Git to protect your secrets. You must create your own!
   
   Create a new file named  `.env` in the root directory and add your keys (you can copy the format from `.env.example`):
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   USAJOBS_API_KEY=your_usajobs_key_here
   USAJOBS_USER_AGENT=your_email@gmail.com
   ```

## How to Run

To launch the web interface, ensure your virtual environment is activated and run from the root directory:
```bash
streamlit run ui/app.py
```
