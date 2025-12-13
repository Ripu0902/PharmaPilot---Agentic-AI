from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from services.llm_service import llm
from graph.state import State
from prompts.system_prompts import REGULATORY_PROMPT
from tools.regulatory_data import get_regulatory_data, format_regulatory_for_llm


def regulatory_agent(state: State) -> dict:
    """
    Regulatory Compliance Expert Agent
    Analyzes FDA approval pathways, drug safety, and compliance requirements
    Uses regulatory data tool to fetch real data
    """
    system_prompt = state.get("regulator_prompt", REGULATORY_PROMPT)
    messages = state.get("message", [])
    
    # Get the last user message to extract query
    last_message = messages[-1]
    query = last_message.content
    
    # Fetch regulatory data using the data tool
    reg_data = get_regulatory_data(query)
    
    # Format regulatory data for LLM
    formatted_data = ""
    if reg_data.get("found"):
        applications = reg_data.get("applications", [])
        for app in applications:
            formatted_data += format_regulatory_for_llm(app) + "\n"
    
    # Create context message with fetched data
    data_context = f"""
Based on the following regulatory data from our database:

{formatted_data if formatted_data else "No regulatory data found for the query."}

Please provide your expert analysis and insights on FDA approval status, compliance requirements, and safety considerations.
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
