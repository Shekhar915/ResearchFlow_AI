from langchain_google_genai import ChatGoogleGenerativeAI

from ResearchFlow.config.settings import GEMINI_API_KEY

LLM = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
    # Speed: little reasoning, bounded output, token streaming, no slow retries.
    thinking_level="low",
    max_output_tokens=1024,
    streaming=True,
    max_retries=1,
    timeout=60,
)
