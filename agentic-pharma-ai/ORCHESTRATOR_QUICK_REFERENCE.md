# Orchestrator Quick Reference

## Files Created/Modified

### Core Implementation

| File | Purpose |
|------|---------|
| `src/graph/state.py` | **MODIFIED** - Added hybrid State with master + agent prompts |
| `src/prompts/system_prompts.py` | **NEW** - 6 system prompts (orchestrator + 5 agents) |
| `src/prompts/__init__.py` | **NEW** - Prompts package initialization |
| `src/orchestrator.py` | **NEW** - Main orchestrator module with entry functions |

### Agents

| File | Purpose |
|------|---------|
| `src/agents/clinical_trials_agent.py` | **MODIFIED** - Implemented with clinical_trials_prompt |
| `src/agents/patent_agent.py` | **MODIFIED** - Implemented with patent_prompt |
| `src/agents/regulator_agent.py` | **MODIFIED** - Implemented with regulator_prompt |
| `src/agents/scientific_journal_agent.py` | **MODIFIED** - Implemented with scientific_journal_prompt |
| `src/agents/summarizer_agent.py` | **MODIFIED** - Implemented with synthesis capability |

### Graph Components

| File | Purpose |
|------|---------|
| `src/graph/router.py` | **MODIFIED** - Intelligent query router with keyword + LLM fallback |
| `src/graph/graph_definition.py` | **MODIFIED** - LangGraph setup with all nodes and edges |

### Documentation

| File | Purpose |
|------|---------|
| `ORCHESTRATOR_GUIDE.md` | Comprehensive implementation guide |
| `IMPLEMENTATION_SUMMARY.md` | Summary of what was built and why |
| `ORCHESTRATOR_QUICK_REFERENCE.md` | This file - quick lookup |

---

## Quick Start

### 1. Basic Usage
```python
from src.orchestrator import run_orchestrator, format_response

query = "What are the latest FDA-approved cancer drugs?"
final_state = run_orchestrator(query)
response = format_response(final_state)
print(response)
```

### 2. Custom State
```python
from src.graph.state import State
from src.graph.graph_definition import build_graph
from langchain_core.messages import HumanMessage

state = {
    "system_prompt": "...",
    "clinical_trials_prompt": "...",
    "patent_prompt": "...",
    "regulator_prompt": "...",
    "scientific_journal_prompt": "...",
    "message": [HumanMessage(content="query")]
}

graph = build_graph()
result = graph.invoke(state)
```

### 3. Debug/Stream Output
```python
from src.orchestrator import initialize_state
from src.graph.graph_definition import build_graph

state = initialize_state("your query")
graph = build_graph()

for event in graph.stream(state):
    print(event)
```

---

## State Structure

```python
State = {
    "system_prompt": str,                    # Orchestrator prompt
    "clinical_trials_prompt": str,           # Clinical expert prompt
    "patent_prompt": str,                    # Patent expert prompt
    "regulator_prompt": str,                 # Regulatory expert prompt
    "scientific_journal_prompt": str,        # Literature expert prompt
    "message": [HumanMessage | AIMessage]   # Conversation history
}
```

---

## Agent Functions

### Clinical Trials Agent
```python
clinical_trials_agent(state: State) -> dict
```
- Queries about: clinical trials, patient outcomes, study designs
- Keywords: "clinical trial", "patient", "study", "efficacy", "phase"

### Patent Agent
```python
patent_agent(state: State) -> dict
```
- Queries about: patents, IP, drug formulations
- Keywords: "patent", "IP", "formulation", "chemical", "drug structure"

### Regulatory Agent
```python
regulatory_agent(state: State) -> dict
```
- Queries about: FDA, approval, compliance, safety
- Keywords: "FDA", "approval", "compliance", "safety", "adverse"

### Scientific Journal Agent
```python
scientific_journal_agent(state: State) -> dict
```
- Queries about: published research, literature, studies
- Keywords: "research", "literature", "published", "journal"

### Summarizer Agent
```python
summarizer_agent(state: State) -> dict
```
- Synthesizes multiple agent responses
- Auto-triggered when 2+ agents respond

---

## Router Logic

```python
route_query(state: State) -> str
# Returns: "clinical_trials" | "patent" | "regulatory" | "scientific_journal"
# Uses keyword matching, falls back to LLM for ambiguous queries
```

---

## Graph Flow

```
START
  → route_query (which agent?)
    ├→ clinical_trials_agent → decide_synthesis
    ├→ patent_agent → decide_synthesis
    ├→ regulatory_agent → decide_synthesis
    └→ scientific_journal_agent → decide_synthesis
       ├→ (multiple agents?) → summarizer_agent → END
       └→ (single agent?) → END
```

---

## Customization Points

### Add New Agent
1. Create `src/agents/new_agent.py`:
   ```python
   def new_agent(state: State) -> dict:
       prompt = state.get("new_agent_prompt")
       messages = state.get("message", [])
       response = llm.invoke([SystemMessage(prompt)] + messages)
       return {"message": messages + [response]}
   ```

2. Add prompt to `src/prompts/system_prompts.py`:
   ```python
   NEW_AGENT_PROMPT = "..."
   ```

3. Add field to `src/graph/state.py`:
   ```python
   new_agent_prompt: Annotated[str, "..."]
   ```

4. Update `src/graph/graph_definition.py`:
   ```python
   graph_builder.add_node("new_agent", new_agent)
   graph_builder.add_conditional_edges("new_agent", decide_synthesis, ...)
   ```

### Modify Routing
Edit `src/graph/router.py`:
- Add keywords to categories
- Update `route_query()` logic
- Change LLM fallback behavior

### Change System Prompts
Edit `src/prompts/system_prompts.py`:
- Modify any PROMPT variable
- Effects apply on next orchestrator run

---

## Testing

### Test Single Agent
```python
from src.agents.clinical_trials_agent import clinical_trials_agent
from langchain_core.messages import HumanMessage

state = {
    "system_prompt": "...",
    "clinical_trials_prompt": "...",
    "patent_prompt": "...",
    "regulator_prompt": "...",
    "scientific_journal_prompt": "...",
    "message": [HumanMessage(content="clinical trial query")]
}

result = clinical_trials_agent(state)
print(result["message"][-1].content)
```

### Test Router
```python
from src.graph.router import route_query
from langchain_core.messages import HumanMessage

state = {"message": [HumanMessage(content="patent question")]}
agent = route_query(state)
print(agent)  # Should print "patent"
```

### Test Full Pipeline
```python
python src/orchestrator.py
```

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| KeyError on state access | Ensure all fields initialized in `initialize_state()` |
| Agent returns empty response | Check LLM service is configured |
| Router picks wrong agent | Add keywords or use custom routing logic |
| Synthesis not triggered | Check `should_synthesize()` in `router.py` |
| Import errors | Ensure `src/` is in Python path |

---

## Configuration

### LLM Service
Edit `src/services/llm_service.py`:
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0)
```

### Data Sources (Optional)
Extend agents to use:
- `services/search_service.py` - Web search
- `services/vector_store_service.py` - RAG
- `tools/clinical_db_connector.py` - Trial data
- `tools/patent_api_connector.py` - Patent data

---

## Performance Notes

- **First call**: ~2-3s (includes LLM inference)
- **Multi-agent calls**: Sequential by default (can be parallelized)
- **Message history**: Grows with each turn (monitor for long sessions)
- **LLM costs**: Increases with message length + number of agents

---

## Architecture Advantages

✅ **Modular**: Each agent is independent
✅ **Scalable**: Easy to add new agents
✅ **Specialized**: Each agent has domain expertise
✅ **Flexible**: Mix master control + agent autonomy
✅ **Transparent**: Clear routing and synthesis logic
✅ **Maintainable**: Well-documented and organized

---

## Architecture Disadvantages

⚠️ **Complexity**: More moving parts than single orchestrator
⚠️ **Latency**: Sequential agent execution (can parallelize)
⚠️ **Costs**: Multiple LLM calls (one per agent per query)
⚠️ **Context**: Message history can grow large

---

## Best Practices

1. **Initialize State Properly**
   ```python
   state = initialize_state(query)  # Always use this
   ```

2. **Customize Prompts**
   - Tailor prompts to your specific domain
   - Update system_prompts.py, not inline

3. **Monitor Agent Selection**
   - Log which agent handles each query
   - Verify routing decisions make sense

4. **Test Edge Cases**
   - Multi-domain queries
   - Ambiguous queries
   - Queries with no matches

5. **Manage Message History**
   - Archive old messages for long sessions
   - Consider summarizing history periodically

---

## Integration Examples

### With Streamlit UI
```python
from src.orchestrator import run_orchestrator, format_response

query = st.text_input("Ask a pharmaceutical question:")
if st.button("Search"):
    final_state = run_orchestrator(query)
    response = format_response(final_state)
    st.write(response)
```

### With FastAPI
```python
from fastapi import FastAPI
from src.orchestrator import run_orchestrator, format_response

app = FastAPI()

@app.post("/query")
async def query_orchestrator(query: str):
    final_state = run_orchestrator(query)
    return {"response": format_response(final_state)}
```

### With Database Storage
```python
from src.orchestrator import run_orchestrator, format_response

query = "..."
final_state = run_orchestrator(query)
response = format_response(final_state)

# Store in database
db.save_query(query, response, final_state["message"])
```

---

**For detailed information, see:**
- `ORCHESTRATOR_GUIDE.md` - Full guide
- `IMPLEMENTATION_SUMMARY.md` - What was built and why
