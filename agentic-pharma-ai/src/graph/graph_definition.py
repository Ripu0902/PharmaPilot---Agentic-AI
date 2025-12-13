# LangGraph orchestrator setup
from langgraph.graph import StateGraph, START, END
from graph.state import State
from agents.clinical_trials_agent import clinical_trials_agent
from agents.patent_agent import patent_agent
from agents.regulator_agent import regulatory_agent
from agents.scientific_journal_agent import scientific_journal_agent
from agents.summarizer_agent import summarizer_agent
from graph.router import route_query, should_synthesize


# Create the state graph
graph_builder = StateGraph(State)

# Add nodes for each agent
graph_builder.add_node("clinical_trials", clinical_trials_agent)
graph_builder.add_node("patent", patent_agent)
graph_builder.add_node("regulatory", regulatory_agent)
graph_builder.add_node("scientific_journal", scientific_journal_agent)
graph_builder.add_node("summarizer", summarizer_agent)

# Add conditional entry point - route the initial query
graph_builder.add_conditional_edges(
    START,
    route_query,
    {
        "clinical_trials": "clinical_trials",
        "patent": "patent",
        "regulatory": "regulatory",
        "scientific_journal": "scientific_journal"
    }
)

# Conditional edge to decide whether to synthesize or end
def decide_synthesis(state: State) -> str:
    """Conditional edge to decide whether to synthesize or end"""
    if should_synthesize(state):
        return "summarizer"
    return END


# Add edges from agents to conditional synthesizer
graph_builder.add_conditional_edges(
    "clinical_trials",
    decide_synthesis,
    {"summarizer": "summarizer", END: END}
)
graph_builder.add_conditional_edges(
    "patent",
    decide_synthesis,
    {"summarizer": "summarizer", END: END}
)
graph_builder.add_conditional_edges(
    "regulatory",
    decide_synthesis,
    {"summarizer": "summarizer", END: END}
)
graph_builder.add_conditional_edges(
    "scientific_journal",
    decide_synthesis,
    {"summarizer": "summarizer", END: END}
)

# Summarizer always ends
graph_builder.add_edge("summarizer", END)

# Compile the graph
def build_graph():
    """Build and return the compiled graph"""
    return graph_builder.compile()

