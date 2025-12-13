# placeholder

from services.llm_service import llm
from graph.state import State

def orchestration_agent(state: State):
    return {"messages" : [llm.invoke(state["message"])]}