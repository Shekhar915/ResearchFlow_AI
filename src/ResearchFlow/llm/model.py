from langchain_google_genai import ChatGoogleGenerativeAI

from ResearchFlow.config.settings import GEMINI_API_KEY

LLM = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
)
