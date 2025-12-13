# FastAPI Orchestrator - Quick Start Guide

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements-api.txt
```

### 2. Configure LLM Service
Edit `src/services/llm_service.py` and add your API key:
```python
from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        api_key="your-openai-api-key",
        model="gpt-4",
        temperature=0.7
    )
```

### 3. Run the Application
```bash
cd agentic-pharma-ai
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### Main Orchestrator
**POST /query** - Route to appropriate agent based on query
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest clinical trials for cancer treatment?"}'
```

### Data Tools

**Clinical Trials**
```bash
# Search trials
curl "http://localhost:8000/data/clinical-trials?query=cancer"

# Get all trials
curl "http://localhost:8000/data/clinical-trials/all"
```

**Patents**
```bash
# Search patents
curl "http://localhost:8000/data/patents?query=formulation"

# Get active patents
curl "http://localhost:8000/data/patents/active"
```

**Regulatory**
```bash
# Search regulatory applications
curl "http://localhost:8000/data/regulatory?query=FDA"

# Get approved drugs
curl "http://localhost:8000/data/regulatory/approved"
```

**Journal Articles**
```bash
# Search journal articles
curl "http://localhost:8000/data/journal?query=cancer research"

# Get all articles
curl "http://localhost:8000/data/journal/all"
```

### System Info
**GET /health** - Health check
**GET /info** - API info and available agents

## Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI

Visit `http://localhost:8000/redoc` for ReDoc documentation

## Example Queries

### Clinical Trial Query
```json
POST /query
{
  "query": "What clinical trials are currently active for oncology?"
}
```

### Patent Query
```json
POST /query
{
  "query": "Search for patents related to drug formulation and delivery"
}
```

### Regulatory Query
```json
POST /query
{
  "query": "What FDA-approved drugs have black box warnings?"
}
```

### Journal Query
```json
POST /query
{
  "query": "Find recent research on cancer immunotherapy in Nature Medicine"
}
```

### Multi-Agent Query (Auto-synthesized)
```json
POST /query
{
  "query": "Compare clinical trials, patents, and regulatory status for cancer drugs approved in the last 5 years"
}
```

## Response Format

### Orchestrator Response
```json
{
  "query": "Your query here",
  "final_response": "AI-generated response with all agent insights",
  "agents_consulted": ["clinical_trials_agent", "patent_agent"],
  "agent_count": 2,
  "total_messages": 5,
  "synthesis_performed": true,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Data Tool Response
```json
{
  "tool_name": "clinical_trials",
  "found": true,
  "count": 3,
  "data": [
    {
      "trial_id": "NCT04567890",
      "title": "Phase 3 Trial",
      "status": "Recruiting",
      "success_rate": 0.82
    }
  ]
}
```

## Environment Variables (Optional)

Create `.env` file:
```
OPENAI_API_KEY=your-key-here
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
```

## Troubleshooting

**Issue**: "Module not found"
- Solution: Make sure you're in the `agentic-pharma-ai` directory and have all dependencies installed

**Issue**: "Connection refused on port 8000"
- Solution: Port may be in use. Run with: `uvicorn src.app:app --port 8001`

**Issue**: "LLM API Error"
- Solution: Check your API key in `src/services/llm_service.py`

**Issue**: "No module named 'src'"
- Solution: Make sure you're running from the `agentic-pharma-ai` directory, not the parent directory

## Architecture Overview

```
FastAPI App (src/app.py)
├── POST /query → Orchestrator
│   └── run_orchestrator() → Router → Agents
├── GET /data/clinical-trials → Clinical Trials Tool
├── GET /data/patents → Patent Tool
├── GET /data/regulatory → Regulatory Tool
└── GET /data/journal → Journal Tool

Agents:
├── clinical_trials_agent → Fetches clinical trial data
├── patent_agent → Fetches patent data
├── regulator_agent → Fetches regulatory data
├── scientific_journal_agent → Fetches journal data
└── summarizer_agent → Synthesizes multi-agent responses
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure LLM service
3. ✅ Start API server
4. ✅ Test endpoints via `/docs`
5. ⏭️ Integrate with frontend
6. ⏭️ Connect to real databases (replace dummy data)
7. ⏭️ Deploy to production

## Support

For issues or questions:
- Check the API docs at `/docs`
- Review agent logs in console output
- Check `src/logging/logger.py` for debug logs
