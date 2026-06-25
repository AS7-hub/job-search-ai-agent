import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    """
    Initializes and returns a ChatGoogleGenerativeAI instance.
    """
    # Load environment variables from a .env file
    load_dotenv()
    
    # Read GEMINI_API_KEY from the environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in the environment. Please set it in the .env file.")
        
    # Create and return the ChatGoogleGenerativeAI instance
    # Temperature controls the randomness of the model's output.
    # A temperature of 0.7 provides a good balance between creativity and determinism,
    # meaning the responses will be somewhat creative but still focused and coherent.
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        google_api_key=api_key
    )
    
    return llm
