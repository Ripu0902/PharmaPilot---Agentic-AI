

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

OPEN_API_KEY = os.getenv("OPEN_API_KEY")


model = ChatOpenAI(model="gpt-5-nano",
    stream_usage=True,
    temperature=0,
    # max_tokens=None,
    # timeout=None,
    # reasoning_effort="low",
    # max_retries=2,
    api_key=OPEN_API_KEY,  # If you prefer to pass api key in directly
    # base_url="...",
    # organization="...",
    # other params...
)


messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Marathi. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]

from pydantic import BaseModel, Field

class GetWeather(BaseModel):

    """Get the current weather in a given location"""

    location: str = Field(..., description="The city and state, e.g. San Francisco, CA")


model_with_tools = model.bind_tools([GetWeather])



ai_msg = model_with_tools.invoke(
    "what is the weather like in Pune, India?",
)

print(ai_msg)



