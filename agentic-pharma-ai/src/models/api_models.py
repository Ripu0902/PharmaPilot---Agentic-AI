"""
Request and Response models for the Orchestrator API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class QueryRequest(BaseModel):
    """Request model for pharmaceutical research queries"""
    query: str = Field(..., description="The pharmaceutical research question")
    max_agents: Optional[int] = Field(default=5, description="Maximum number of agents to use")
    
    class Config:
        example = {
            "query": "What are the clinical trials and FDA approval status for cancer drug XYZ?",
            "max_agents": 5
        }


class AgentResponse(BaseModel):
    """Response from a single agent"""
    agent_name: str = Field(..., description="Name of the agent (clinical_trials, patent, etc)")
    response: str = Field(..., description="The agent's analysis and response")
    data_found: bool = Field(..., description="Whether relevant data was found")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        example = {
            "agent_name": "clinical_trials",
            "response": "Based on clinical trial NCT04567890...",
            "data_found": True,
            "timestamp": "2025-12-10T12:00:00"
        }


class OrchestratorResponse(BaseModel):
    """Response from the orchestrator"""
    query: str = Field(..., description="The original query")
    final_response: str = Field(..., description="Final synthesized response")
    agents_consulted: List[str] = Field(..., description="List of agents that were consulted")
    agent_count: int = Field(..., description="Number of agents consulted")
    total_messages: int = Field(..., description="Total messages in conversation")
    synthesis_performed: bool = Field(..., description="Whether synthesis was performed")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        example = {
            "query": "Clinical trials and FDA status for cancer drug XYZ",
            "final_response": "Cancer Drug XYZ is in Phase 3 trials with 82% efficacy...",
            "agents_consulted": ["clinical_trials", "regulatory"],
            "agent_count": 2,
            "total_messages": 4,
            "synthesis_performed": True,
            "timestamp": "2025-12-10T12:00:00"
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(default="1.0.0")
    
    class Config:
        example = {
            "status": "healthy",
            "timestamp": "2025-12-10T12:00:00",
            "version": "1.0.0"
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        example = {
            "error": "Invalid query",
            "detail": "Query must be at least 5 characters",
            "timestamp": "2025-12-10T12:00:00"
        }


class DataToolResponse(BaseModel):
    """Response from a data tool query"""
    tool_name: str = Field(..., description="Name of the data tool")
    found: bool = Field(..., description="Whether data was found")
    count: int = Field(..., description="Number of results found")
    data: List[Dict[str, Any]] = Field(default=[], description="The actual data")
    
    class Config:
        example = {
            "tool_name": "clinical_trials",
            "found": True,
            "count": 1,
            "data": [
                {
                    "title": "Phase 3 Clinical Trial for Cancer Drug XYZ",
                    "nct": "NCT04567890",
                    "efficacy_rate": "82%"
                }
            ]
        }
