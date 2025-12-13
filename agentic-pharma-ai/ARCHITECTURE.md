# Pharmaceutical Research Orchestrator - Architecture

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER QUERY                                  │
│            "What are the latest FDA-approved drugs?"            │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │  initialize_state()    │
                    │  ✓ All 6 prompts      │
                    │  ✓ Message history    │
                    └────────┬───────────────┘
                             │
                             ▼
                  ┌──────────────────────────┐
                  │   build_graph()          │
                  │   Compile LangGraph      │
                  └────────┬─────────────────┘
                           │
                           ▼
          ┌────────────────────────────────────┐
          │      STATE (Shared)                │
          │ ┌──────────────────────────────┐  │
          │ │ system_prompt (orchestrator) │  │
          │ │ clinical_trials_prompt       │  │
          │ │ patent_prompt                │  │
          │ │ regulator_prompt             │  │
          │ │ scientific_journal_prompt    │  │
          │ │ message: [...]               │  │
          │ └──────────────────────────────┘  │
          └────┬───────────┬────────┬──────┬──┘
               │           │        │      │
        ┌──────▼────┐  ┌───▼──┐  ┌─▼──┐ ┌▼──────┐
        │   ROUTER   │  │      │  │    │ │       │
        │ (Keyword + │  │      │  │    │ │       │
        │   LLM      │  │      │  │    │ │       │
        │  Fallback) │  │      │  │    │ │       │
        └──────┬─────┘  │      │  │    │ │       │
               │        │      │  │    │ │       │
        ┌──────┴────────┴──────┴──┴────┴─┴───┐
        │                                    │
        ▼         ▼          ▼       ▼       ▼
    ┌────────┐ ┌───────┐ ┌────────┐ ┌──────────┐
    │Clinical│ │Patent │ │Regulat-│ │Scientific│
    │ Trials │ │ Agent │ │ory Agnt│ │ Journal  │
    │ Agent  │ │       │ │        │ │ Agent    │
    └────┬───┘ └───┬───┘ └───┬────┘ └────┬─────┘
         │         │         │           │
         │    Uses state prompts         │
         │    + message history          │
         │    + LLM service              │
         │                               │
         └───────────┬───────────────────┘
                     │
                     ▼
        ┌─────────────────────────────┐
        │  Message Accumulation       │
        │  [HumanMsg] →               │
        │  [HumanMsg, AIMsg(agent1)] →│
        │  [HumanMsg, AIMsg(...), AIMsg(agent2)]
        └────────────┬────────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │  decide_synthesis()      │
        │  (Multiple agents?)      │
        └────┬────────────┬────────┘
             │            │
          YES│            │NO
             ▼            ▼
        ┌────────────┐  ┌──────┐
        │Summarizer  │  │ END  │
        │Agent       │  │ ◄───┴──► Final Response
        │(combines)  │  └──────┘
        └─────┬──────┘
              │
              ▼
        ┌──────────────┐
        │  format_response()
        │  Extract AIMessage content
        └────────┬─────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │   USER RESPONSE          │
        │                          │
        │ Comprehensive Report:    │
        │ • Patent info            │
        │ • Clinical findings      │
        │ • Regulatory status      │
        │ • Literature review      │
        └──────────────────────────┘
```

---

## Data Flow Through Hybrid Architecture

### Example: Multi-Domain Query

**Query**: "What's the patent status and clinical effectiveness of drug X?"

```
Step 1: Route Query
┌─────────────────────────────────────┐
│ Input: "patent status + clinical"   │
│ Keyword Match: patent (1), clinical │
│ (3), patent (1)                     │
│ Decision: Route to patent first     │
└──────────────┬──────────────────────┘
               │
               ▼
Step 2: Patent Agent Processes
┌────────────────────────────────────┐
│ State Extracts:                    │
│ • patent_prompt: "You are a..."    │
│ • message: [HumanMessage]          │
│                                    │
│ Build: [SystemMsg(patent_prompt), │
│         HumanMessage]              │
│                                    │
│ LLM.invoke() → Patent Analysis    │
│                                    │
│ Return: message ← [HumanMsg,      │
│         AIMsg(patent analysis)]   │
└────────────────┬──────────────────┘
                 │
                 ▼
Step 3: Check Synthesis
┌──────────────────────────────────┐
│ should_synthesize(state)?         │
│ Count AIMessages: 1               │
│ Result: NO - continue routing     │
└──────────────┬───────────────────┘
               │
               ▼
Step 4: Route Next Query
┌──────────────────────────────────┐
│ Same message (now with patent)    │
│ Clinical keywords now dominant    │
│ Route to clinical_trials agent    │
└──────────────┬───────────────────┘
               │
               ▼
Step 5: Clinical Agent Processes
┌─────────────────────────────────┐
│ State Extracts:                 │
│ • clinical_trials_prompt: "..." │
│ • message: [HumanMsg,           │
│    AIMsg(patent)]  ◄─ See!      │
│                                 │
│ Build: [SystemMsg(clinical),    │
│         HumanMsg,               │
│         AIMsg(patent)]          │
│                                 │
│ LLM sees context! Better answer │
│                                 │
│ LLM.invoke() → Clinical Data    │
│                                 │
│ Return: message ← [HumanMsg,    │
│         AIMsg(patent),          │
│         AIMsg(clinical)]        │
└──────────────┬──────────────────┘
               │
               ▼
Step 6: Check Synthesis
┌──────────────────────────────────┐
│ should_synthesize(state)?         │
│ Count AIMessages: 2               │
│ Result: YES - Synthesize!        │
└──────────────┬───────────────────┘
               │
               ▼
Step 7: Summarizer Processes
┌──────────────────────────────────┐
│ State Extracts:                  │
│ • system_prompt + SUMMARIZER     │
│ • message: [HumanMsg,            │
│    AIMsg(patent),                │
│    AIMsg(clinical)]              │
│                                  │
│ LLM Synthesizes:                 │
│ "Based on patent data and        │
│  clinical trials, here's the     │
│  comprehensive analysis..."      │
└──────────────┬───────────────────┘
               │
               ▼
Step 8: Final Output
┌──────────────────────────────────┐
│ message: [HumanMsg,              │
│          AIMsg(patent),          │
│          AIMsg(clinical),        │
│          AIMsg(synthesis)]       │
│                                  │
│ format_response() extracts       │
│ last AIMsg content               │
│                                  │
│ User gets comprehensive answer!  │
└──────────────────────────────────┘
```

---

## State Transformation Flow

```
INITIAL STATE:
{
  "system_prompt": "You are an orchestrator...",
  "clinical_trials_prompt": "You are a clinical expert...",
  "patent_prompt": "You are a patent expert...",
  "regulator_prompt": "You are a regulatory expert...",
  "scientific_journal_prompt": "You are a literature expert...",
  "message": [
    HumanMessage("What's the patent status and clinical data?")
  ]
}
          │
          ▼
AFTER PATENT AGENT:
{
  "system_prompt": "...",
  "clinical_trials_prompt": "...",
  "patent_prompt": "...",
  "regulator_prompt": "...",
  "scientific_journal_prompt": "...",
  "message": [
    HumanMessage("What's the patent status and clinical data?"),
    AIMessage("Patent Analysis: Drug XYZ has 15 years of exclusivity...") ◄─ Added
  ]
}
          │
          ▼
AFTER CLINICAL AGENT:
{
  "system_prompt": "...",
  "clinical_trials_prompt": "...",
  "patent_prompt": "...",
  "regulator_prompt": "...",
  "scientific_journal_prompt": "...",
  "message": [
    HumanMessage("What's the patent status and clinical data?"),
    AIMessage("Patent Analysis: ..."),
    AIMessage("Clinical Trials: Phase 3 shows 85% efficacy...") ◄─ Added
  ]
}
          │
          ▼
AFTER SUMMARIZER:
{
  "system_prompt": "...",
  "clinical_trials_prompt": "...",
  "patent_prompt": "...",
  "regulator_prompt": "...",
  "scientific_journal_prompt": "...",
  "message": [
    HumanMessage("What's the patent status and clinical data?"),
    AIMessage("Patent Analysis: ..."),
    AIMessage("Clinical Trials: ..."),
    AIMessage("COMPREHENSIVE REPORT: Combining patent and clinical...") ◄─ Added
  ]
}
          │
          ▼
FINAL OUTPUT:
"COMPREHENSIVE REPORT: Combining patent and clinical findings, 
Drug XYZ offers strong IP protection through 2038 with proven 
clinical efficacy of 85% in Phase 3 trials..."
```

---

## Agent Execution Sequence (Sequential Model)

```
Timeline
───────────────────────────────────────────────────────────────

T0  Initialize State
    ├─ Create all 6 prompts
    ├─ Add HumanMessage
    └─ Ready to execute

T1  Graph.invoke(state)
    ├─ Route query
    └─ Decide: Patent Agent

T2  Patent Agent
    ├─ Extract patent_prompt
    ├─ Build message chain
    ├─ LLM processing: [████████] 1.2s
    └─ Return updated state

T3  Route next/Synthesis check
    ├─ Decision: Need Clinical too
    └─ Decide: Clinical Agent

T4  Clinical Agent
    ├─ Extract clinical_trials_prompt
    ├─ Build message chain (sees patent response!)
    ├─ LLM processing: [████████] 1.1s
    └─ Return updated state

T5  Synthesis check
    ├─ Count: 2 AIMessages
    └─ Decide: Synthesize!

T6  Summarizer Agent
    ├─ Extract system_prompt
    ├─ Build message chain (sees all responses!)
    ├─ LLM processing: [██████] 0.8s
    └─ Return final state

T7  Format Response
    ├─ Extract last AIMessage
    ├─ Return content
    └─ ✓ Done (Total: 4.1s)

Optional: Parallel Mode
T2-T4 Could run patent + clinical in parallel if needed
      (Would save ~1.1s, reduce total to ~3s)
```

---

## Prompt Hierarchy

```
SYSTEM PROMPTS (Applied in sequence)

Level 0: Master Context
┌──────────────────────────────────────┐
│ system_prompt (ORCHESTRATOR_PROMPT)  │
│ "You are an expert pharmaceutical    │
│  research orchestrator AI. Your role │
│  is to analyze queries, route them, │
│  and synthesize responses..."        │
│                                      │
│ Applied in: Synthesizer Agent        │
└──────────────────────────────────────┘

Level 1: Specialized Expertise
┌──────────────────────────────────────┐
│ clinical_trials_prompt               │
│ "You are a Clinical Trials Research  │
│  Specialist..."                      │
│                                      │
│ patent_prompt                        │
│ "You are a Pharmaceutical Patent     │
│  Expert..."                          │
│                                      │
│ regulator_prompt                     │
│ "You are a Regulatory Compliance     │
│  Expert..."                          │
│                                      │
│ scientific_journal_prompt            │
│ "You are a Scientific Literature     │
│  Research Specialist..."             │
│                                      │
│ Applied in: Respective agents        │
└──────────────────────────────────────┘

Result: Each agent acts as expert in its domain
        while seeing other agents' responses
        in message history!
```

---

## Router Decision Tree

```
User Query Input
        │
        ▼
Count Keyword Matches
        │
    ┌───┼────┬──────┬──────────┐
    │   │    │      │          │
    ▼   ▼    ▼      ▼          ▼
Clinical Patent Regulatory Journal
   3      1      0         0

Highest Score: Clinical (3 matches)
        │
        ▼
Return: "clinical_trials" agent
        │
        ▼
Execute clinical_trials_agent(state)


Alternative: Ambiguous Query
        │
        ▼
Count Keyword Matches
        │
    ┌───┼────┬──────┬──────────┐
    │   │    │      │          │
    ▼   ▼    ▼      ▼          ▼
Clinical Patent Regulatory Journal
   0      0      0         0

No clear winner! Use LLM Fallback:
        │
        ▼
LLM: "Based on this query [details],
      which specialist should handle it?"
        │
        ▼
LLM Response: "regulatory"
        │
        ▼
Return: "regulatory" agent
```

---

## Benefits of Hybrid Architecture

```
✓ ORCHESTRATOR BENEFITS         ✓ AGENT BENEFITS
├─ Central coordination          ├─ Domain expertise
├─ Message routing               ├─ Specialized prompts
├─ Response synthesis            ├─ Focused responses
├─ Context awareness             ├─ Quality improvement
└─ Multi-agent harmony           └─ Scalability

COMBINED = BEST OF BOTH
├─ Intelligent routing
├─ Expert responses
├─ Smart synthesis
└─ Excellent user experience
```

---

## Integration Points

```
┌──────────────────────────────────────────┐
│         PHARMACEUTICAL RESEARCH          │
│            ORCHESTRATOR                  │
└──────────────────────────────────────────┘
           │         │        │         │
    ┌──────▼─┐  ┌────▼──┐  ┌─▼────┐  ┌▼────────┐
    │  LLM   │  │Search │  │Vector│  │Database │
    │Service │  │Service│  │Store │  │Services │
    └────────┘  └───────┘  └──────┘  └─────────┘

Each agent can leverage these services:
- llm_service.py: LLM invocations
- search_service.py: Information retrieval
- vector_store_service.py: RAG capabilities
- Clinical/Patent/Regulatory DBs: Data access
```

---

**See ORCHESTRATOR_GUIDE.md and IMPLEMENTATION_SUMMARY.md for complete details.**
