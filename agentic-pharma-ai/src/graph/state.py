# placeholder
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class State(TypedDict):
    system_prompt: Annotated[str, "The master orchestrator system prompt."]
    clinical_trials_prompt: Annotated[str, "System prompt for clinical trials agent."]
    patent_prompt: Annotated[str, "System prompt for patent agent."]
    regulator_prompt: Annotated[str, "System prompt for regulatory agent."]
    scientific_journal_prompt: Annotated[str, "System prompt for scientific journal agent."]
    message : Annotated[list[HumanMessage | AIMessage], "The list of messages exchanged so far."]