from langchain_core.messages import SystemMessage
from services.llm_service import llm
from graph.state import State
from prompts.system_prompts import ORCHESTRATOR_PROMPT


def route_query(state: State) -> str:
    """
    Router function that determines which agent(s) should handle the query
    Returns the next node in the graph to execute
    """
    system_prompt = state.get("system_prompt", ORCHESTRATOR_PROMPT)
    messages = state.get("message", [])
    
    # Get the last user message
    if not messages:
        return "clinical_trials"  # Default agent
    
    last_message = messages[-1]
    query = last_message.content.lower()
    
    # Keyword-based routing logic
    clinical_keywords = ["clinical trial", "patient", "study", "efficacy", "phase", "outcome"]
    patent_keywords = ["patent", "intellectual property", "ip", "formulation", "chemical", "drug structure"]
    regulatory_keywords = ["fda", "approval", "compliance", "safety", "adverse", "regulation"]
    journal_keywords = ["research", "literature", "published", "study", "journal", "peer review"]
    
    # Count keyword matches
    clinical_match = sum(1 for kw in clinical_keywords if kw in query)
    patent_match = sum(1 for kw in patent_keywords if kw in query)
    regulatory_match = sum(1 for kw in regulatory_keywords if kw in query)
    journal_match = sum(1 for kw in journal_keywords if kw in query)
    
    # Return agent with highest match count
    matches = {
        "clinical_trials": clinical_match,
        "patent": patent_match,
        "regulatory": regulatory_match,
        "scientific_journal": journal_match
    }
    
    # Get the agent with max matches (default to clinical_trials if tie)
    best_agent = max(matches, key=matches.get)
    
    # If no clear match, use LLM to decide
    if max(matches.values()) == 0:
        routing_prompt = f"""Based on this query, which pharmaceutical research expert should handle it?
        
Query: {query}

Choose one:
- clinical_trials: For clinical trial data, patient outcomes, study designs
- patent: For patent information, intellectual property, formulations
- regulatory: For FDA approval, regulatory compliance, drug safety
- scientific_journal: For published research, scientific literature

Respond with only the agent name (e.g., 'clinical_trials')"""
        
        response = llm.invoke([SystemMessage(content=routing_prompt)])
        response_text = response.content.lower()
        
        if "patent" in response_text:
            return "patent"
        elif "regulatory" in response_text:
            return "regulatory"
        elif "scientific" in response_text or "journal" in response_text:
            return "scientific_journal"
        else:
            return "clinical_trials"
    
    return best_agent


def should_synthesize(state: State) -> bool:
    """
    Determines if responses should be synthesized
    Returns True if multiple agents have contributed
    """
    messages = state.get("message", [])
    # Count AIMessage occurrences - if more than one agent has responded, synthesize
    ai_message_count = sum(1 for msg in messages if hasattr(msg, '__class__') and msg.__class__.__name__ == 'AIMessage')
    return ai_message_count > 1
