"""Orchestrator initialization and execution module.

This orchestrator performs simple planning to determine which specialist
agents should run for a given user query, invokes those agents sequentially,
and then synthesizes their outputs into a single final response.
"""
from typing import List

from langchain_core.messages import HumanMessage
from graph.state import State
from prompts.system_prompts import (
    ORCHESTRATOR_PROMPT,
    CLINICAL_TRIALS_PROMPT,
    PATENT_PROMPT,
    REGULATORY_PROMPT,
    SCIENTIFIC_JOURNAL_PROMPT,
    SUMMARIZER_PROMPT,
)


def initialize_state(user_query: str) -> State:
    """
    Initialize the state with system prompts and the initial user query
    
    Args:
        user_query: The user's initial question or request
        
    Returns:
        Initialized State dictionary
    """
    return {
        "system_prompt": ORCHESTRATOR_PROMPT,
        "clinical_trials_prompt": CLINICAL_TRIALS_PROMPT,
        "patent_prompt": PATENT_PROMPT,
        "regulator_prompt": REGULATORY_PROMPT,
        "scientific_journal_prompt": SCIENTIFIC_JOURNAL_PROMPT,
        "message": [HumanMessage(content=user_query)]
    }


def plan_agents(query: str) -> List[str]:
    """
    Simple planner: choose which agents should handle the query.
    Returns a list of agent keys (matching module names):
    `clinical_trials`, `patent`, `regulatory`, `scientific_journal`.
    """
    q = query.lower()
    agents = []

    # keywords
    if any(k in q for k in ["clinical trial", "nct", "study", "patient", "efficacy", "phase"]):
        agents.append("clinical_trials")
    if any(k in q for k in ["patent", "intellectual property", "ip", "formulation", "chemical"]):
        agents.append("patent")
    if any(k in q for k in ["fda", "approval", "compliance", "safety", "regulatory", "nda", "bla", "ind"]):
        agents.append("regulatory")
    if any(k in q for k in ["journal", "research", "published", "paper", "study", "literature", "immunotherapy", "nature"]):
        agents.append("scientific_journal")

    # If user explicitly asks to compare or all domains, include all
    if ("compare" in q or "all" in q or "across" in q) and len(agents) < 4:
        return ["clinical_trials", "patent", "regulatory", "scientific_journal"]

    # Default to clinical_trials if nothing matched
    return agents or ["clinical_trials"]


def _import_agent(agent_key: str):
    """Dynamically import agent callable by key."""
    if agent_key == "clinical_trials":
        from agents.clinical_trials_agent import clinical_trials_agent as fn
    elif agent_key == "patent":
        from agents.patent_agent import patent_agent as fn
    elif agent_key == "regulatory":
        from agents.regulator_agent import regulatory_agent as fn
    elif agent_key == "scientific_journal":
        from agents.scientific_journal_agent import scientific_journal_agent as fn
    elif agent_key == "summarizer":
        from agents.summarizer_agent import summarizer_agent as fn
    else:
        raise ValueError(f"Unknown agent: {agent_key}")
    return fn


def run_orchestrator(user_query: str) -> dict:
    """
    Execute the orchestrator using a simple plan-and-execute loop.

    Steps:
    1. Initialize state
    2. Plan which agents to run
    3. Invoke each agent sequentially, updating state
    4. If multiple agents produced responses, run `summarizer` to synthesize
    """
    state = initialize_state(user_query)

    # Decide which agents to run
    agent_keys = plan_agents(user_query)

    # Run each agent sequentially
    for key in agent_keys:
        agent_fn = _import_agent(key)
        try:
            result = agent_fn(state)
        except Exception as e:
            # Attach an error AIMessage-like placeholder
            from langchain_core.messages import AIMessage
            messages = state.get("message", [])
            messages.append(AIMessage(content=f"Agent {key} error: {e}"))
            state["message"] = messages
            continue

        # Expect agent result to contain an updated 'message' list
        if isinstance(result, dict) and result.get("message"):
            state["message"] = result["message"]

    # If more than one agent ran, synthesize
    if len(agent_keys) > 1:
        summarizer = _import_agent("summarizer")
        try:
            result = summarizer(state)
            if isinstance(result, dict) and result.get("message"):
                state["message"] = result["message"]
        except Exception:
            pass

    return state


def format_response(final_state: State) -> str:
    """
    Format the final state into a readable response
    
    Args:
        final_state: The final state returned from orchestrator
        
    Returns:
        Formatted response string
    """
    messages = final_state.get("message", [])
    
    if not messages:
        return "No response generated"
    
    # Get the last message (final response)
    last_message = messages[-1]
    
    return last_message.content


if __name__ == "__main__":
    # Example usage
    query = "What are the latest clinical trials for cancer treatment?"
    print(f"Query: {query}\n")
    print("=" * 80)
    
    final_state = run_orchestrator(query)
    response = format_response(final_state)
    
    print("Response:")
    print(response)
