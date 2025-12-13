from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from services.llm_service import llm
from graph.state import State
from prompts.system_prompts import PATENT_PROMPT
from tools.patent_data import get_patent_data, format_patent_for_llm


def patent_agent(state: State) -> dict:
    """
    Patent Expert Agent
    Analyzes patent information, intellectual property, and drug formulations
    Uses patent data tool to fetch real data
    """
    system_prompt = state.get("patent_prompt", PATENT_PROMPT)
    messages = state.get("message", [])
    
    # Get the last user message to extract query
    last_message = messages[-1]
    query = last_message.content
    
    # Fetch patent data using the data tool
    patent_data = get_patent_data(query)
    
    # Format patent data for LLM
    formatted_data = ""
    if patent_data.get("found"):
        patents = patent_data.get("patents", [])
        for patent in patents:
            formatted_data += format_patent_for_llm(patent) + "\n"
    
    # Create context message with fetched data
    data_context = f"""
Based on the following patent data from our database:

{formatted_data if formatted_data else "No patent data found for the query."}

Please provide your expert analysis and insights on IP protection, freedom to operate, and patent landscape.
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
