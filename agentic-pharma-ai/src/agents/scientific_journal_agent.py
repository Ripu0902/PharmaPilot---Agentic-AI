from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from services.llm_service import llm
from graph.state import State
from prompts.system_prompts import SCIENTIFIC_JOURNAL_PROMPT
from tools.scientific_journal_data import get_journal_data, format_article_for_llm


def scientific_journal_agent(state: State) -> dict:
    """
    Scientific Literature Research Specialist Agent
    Analyzes published peer-reviewed research and scientific literature
    Uses scientific journal data tool to fetch real data
    """
    system_prompt = state.get("scientific_journal_prompt", SCIENTIFIC_JOURNAL_PROMPT)
    messages = state.get("message", [])
    
    # Get the last user message to extract query
    last_message = messages[-1]
    query = last_message.content
    
    # Fetch journal data using the data tool
    journal_data = get_journal_data(query)
    
    # Format journal data for LLM
    formatted_data = ""
    if journal_data.get("found"):
        articles = journal_data.get("articles", [])
        for article in articles:
            formatted_data += format_article_for_llm(article) + "\n"
    
    # Create context message with fetched data
    data_context = f"""
Based on the following scientific literature data from our database:

{formatted_data if formatted_data else "No scientific literature found for the query."}

Please provide your expert analysis and insights on published research, study quality, and scientific evidence.
"""
    
    # Build message chain with system prompt and data context
    full_messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=data_context),
        *messages
    ]
    
    # Invoke LLM
    response = llm.invoke(full_messages)
    
    # Update state with agent response
    updated_messages = messages + [response]
    
    return {
        "message": updated_messages
    }
