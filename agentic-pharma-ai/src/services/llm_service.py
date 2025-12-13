# placeholder
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5-nano",
    stream_usage=True,
    temperature=0,
    # max_tokens=None,
    # timeout=None,
    # reasoning_effort="low",
    # max_retries=2,
    api_key=os.getenv("OPEN_API_KEY"),  # If you prefer to pass api key in directly
    # base_url="...",
    # organization="...",
    # other params...
)
