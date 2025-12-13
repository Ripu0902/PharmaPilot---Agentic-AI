from langchain_core.messages import SystemMessage, AIMessage
from services.llm_service import llm
from graph.state import State
from prompts.system_prompts import SUMMARIZER_PROMPT


def summarizer_agent(state: State) -> dict:
    """
    Summarizer Agent
    Synthesizes findings from multiple specialized agents into coherent reports
    """
    system_prompt = state.get("system_prompt", SUMMARIZER_PROMPT)
    messages = state.get("message", [])
    
    # Build message chain with system prompt
    full_messages = [SystemMessage(content=system_prompt)] + messages
    
    # Invoke LLM for final synthesis
    response = llm.invoke(full_messages)
    
    # Update state with summary response
    updated_messages = messages + [response]
    
    return {
        "message": updated_messages
    }
