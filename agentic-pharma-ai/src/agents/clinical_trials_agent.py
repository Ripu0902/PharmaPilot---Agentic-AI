from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from services.llm_service import llm
from graph.state import State
from prompts.system_prompts import CLINICAL_TRIALS_PROMPT
from tools.clinical_trials_data import get_clinical_trial_data, format_trial_for_llm


def clinical_trials_agent(state: State) -> dict:
    """
    Clinical Trials Specialist Agent
    Analyzes clinical trial data, study designs, and patient outcomes
    Uses clinical trials data tool to fetch real data
    """
    system_prompt = state.get("clinical_trials_prompt", CLINICAL_TRIALS_PROMPT)
    messages = state.get("message", [])
    
    # Get the last user message to extract query
    last_message = messages[-1]
    query = last_message.content
    
    # Fetch clinical trial data using the data tool
    trial_data = get_clinical_trial_data(query)
    
    # Format trial data for LLM
    formatted_data = ""
    if trial_data.get("found"):
        trials = trial_data.get("trials", [])
        for trial in trials:
            formatted_data += format_trial_for_llm(trial) + "\n"
    
    # Create context message with fetched data
    data_context = f"""
Based on the following clinical trial data from our database:

{formatted_data if formatted_data else "No clinical trial data found for the query."}

Please provide your expert analysis and insights.
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