# Pharmaceutical Research Orchestrator - Implementation Guide

## Overview

This is a hybrid agentic AI system that uses a master orchestrator with specialized agents to handle pharmaceutical research queries. The orchestrator intelligently routes queries to appropriate domain experts and synthesizes their responses.

## Architecture

### State Structure (Hybrid Approach)

```python
State(TypedDict):
    system_prompt: str              # Master orchestrator system prompt
    clinical_trials_prompt: str     # Clinical trials agent prompt
    patent_prompt: str              # Patent agent prompt
    regulator_prompt: str           # Regulatory agent prompt
    scientific_journal_prompt: str  # Scientific journal agent prompt
    message: list[HumanMessage | AIMessage]  # Shared message history
```

### Agent Responsibilities

1. **Clinical Trials Agent** (`clinical_trials_agent.py`)
   - Analyzes clinical trial data and study designs
   - Understands patient demographics and outcomes
   - Evaluates treatment efficacy and safety profiles
   - Interprets phase-specific trial results (Phase I-IV)

2. **Patent Agent** (`patent_agent.py`)
   - Analyzes patent information and intellectual property
   - Understands drug formulations and chemical structures
   - Evaluates freedom to operate and patent landscapes
   - Assesses patent expiration and exclusivity periods

3. **Regulatory Agent** (`regulator_agent.py`)
   - Handles FDA approval pathways and requirements
   - Manages drug safety and adverse event monitoring
   - Ensures manufacturing compliance and quality standards
   - Processes regulatory submissions (IND, BLA, NDA)

4. **Scientific Journal Agent** (`scientific_journal_agent.py`)
   - Analyzes published peer-reviewed research
   - Understands experimental methodologies and results
   - Evaluates research quality and citations
   - Identifies research trends and knowledge gaps

5. **Summarizer Agent** (`summarizer_agent.py`)
   - Consolidates findings from multiple specialized agents
   - Creates coherent, comprehensive reports
   - Highlights key insights and actionable recommendations
   - Presents information in structured formats

### Routing Logic

The router (`router.py`) uses keyword matching with LLM fallback:

**Keyword Categories:**
- **Clinical Trials**: "clinical trial", "patient", "study", "efficacy", "phase", "outcome"
- **Patent**: "patent", "intellectual property", "ip", "formulation", "chemical", "drug structure"
- **Regulatory**: "fda", "approval", "compliance", "safety", "adverse", "regulation"
- **Journal**: "research", "literature", "published", "study", "journal", "peer review"

### Graph Flow

```
START
  ↓
route_query (conditional node)
  ├─→ clinical_trials_agent
  ├─→ patent_agent
  ├─→ regulatory_agent
  └─→ scientific_journal_agent
       ↓
    decide_synthesis (conditional)
       ├─→ END (single agent response)
       └─→ summarizer_agent → END
```

## Usage

### Basic Usage

```python
from orchestrator import run_orchestrator, format_response

# Run the orchestrator with a query
query = "What are the latest FDA-approved drugs for diabetes treatment?"
final_state = run_orchestrator(query)
response = format_response(final_state)

print(response)
```

### Advanced Usage - Direct State Initialization

```python
from langchain_core.messages import HumanMessage
from orchestrator import initialize_state
from graph.graph_definition import build_graph

# Create initial state
state = initialize_state("Your query here")

# Build and compile graph
graph = build_graph()

# Execute with streaming
for event in graph.stream(state):
    print(event)
```

### Customizing System Prompts

```python
from orchestrator import run_orchestrator
from graph.state import State
from langchain_core.messages import HumanMessage

# Custom prompts
custom_state = {
    "system_prompt": "Your custom orchestrator prompt",
    "clinical_trials_prompt": "Your custom clinical trials prompt",
    "patent_prompt": "Your custom patent prompt",
    "regulator_prompt": "Your custom regulatory prompt",
    "scientific_journal_prompt": "Your custom journal prompt",
    "message": [HumanMessage(content="Your query")]
}

# Execute with custom state
graph = build_graph()
final_state = graph.invoke(custom_state)
```

## File Structure

```
src/
├── orchestrator.py                 # Main orchestrator module
├── graph/
│   ├── state.py                   # State TypedDict definition
│   ├── graph_definition.py         # LangGraph setup and compilation
│   ├── router.py                   # Query routing logic
│   └── utils.py                    # Graph utilities
├── agents/
│   ├── __init__.py
│   ├── clinical_trials_agent.py   # Clinical trials expert
│   ├── patent_agent.py            # Patent expert
│   ├── regulator_agent.py         # Regulatory expert
│   ├── scientific_journal_agent.py# Literature expert
│   └── summarizer_agent.py        # Summary synthesis
├── prompts/
│   ├── __init__.py
│   └── system_prompts.py          # All system prompts
└── services/
    └── llm_service.py              # LLM service (uses configured LLM)
```

## System Prompts

All system prompts are defined in `src/prompts/system_prompts.py`:

- **ORCHESTRATOR_PROMPT**: Routes queries and maintains context
- **CLINICAL_TRIALS_PROMPT**: Domain expertise for clinical research
- **PATENT_PROMPT**: Domain expertise for intellectual property
- **REGULATORY_PROMPT**: Domain expertise for FDA and compliance
- **SCIENTIFIC_JOURNAL_PROMPT**: Domain expertise for published research
- **SUMMARIZER_PROMPT**: Synthesis and report generation

## Key Features

✅ **Intelligent Routing**: Routes queries to appropriate specialists
✅ **Parallel Agent Execution**: Can run multiple agents if needed
✅ **Automatic Synthesis**: Combines multiple agent responses
✅ **Hybrid Approach**: Master orchestrator + specialized agents
✅ **Extensible**: Easy to add new agents or modify prompts
✅ **Context Preservation**: Maintains message history across turns

## Integration Points

### With Your Existing Services

The orchestrator integrates with:

1. **LLM Service** (`services/llm_service.py`)
   - All agents use this for LLM invocations
   - Configure your preferred LLM here

2. **Search Service** (`services/search_service.py`)
   - Can be used by agents to find information
   - Extend agents to call this service

3. **Vector Store** (`services/vector_store_service.py`)
   - For RAG capabilities
   - Agents can retrieve relevant documents

4. **Database Services**
   - Clinical database for trial data
   - Patent database for patent information
   - etc.

## Customization Guide

### Adding a New Agent

1. Create `new_agent.py` in `src/agents/`
2. Add system prompt to `src/prompts/system_prompts.py`
3. Add prompt field to `State` in `src/graph/state.py`
4. Update router keywords if needed
5. Add node to graph in `src/graph/graph_definition.py`

### Modifying Routing Logic

Edit `router.py`:
- Add/modify keyword categories
- Adjust LLM-based routing
- Add custom routing rules

### Updating System Prompts

Edit `src/prompts/system_prompts.py`:
- Refine instructions for agents
- Add domain expertise
- Adjust tone and style

## Testing

To test the orchestrator:

```bash
cd src
python orchestrator.py
```

This runs the example usage and should produce agent responses to the sample query.

## Notes

- **State Initialization**: Always initialize all State fields to avoid KeyError
- **Message History**: The `message` list accumulates across agent calls
- **Agent Responses**: Each agent appends its response as an AIMessage
- **Synthesis**: Automatic when multiple agents contribute
- **Error Handling**: Implement in each agent as needed
