"""
Pharmaceutical Research Orchestrator - FastAPI Application
Exposes the multi-agent orchestrator as REST API endpoints
"""

from fastapi import FastAPI, HTTPException, Query 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from typing import List, Dict, Any

# Import orchestrator
from orchestrator import run_orchestrator, format_response, initialize_state
from graph.state import State

# Import data tools
from tools.clinical_trials_data import get_clinical_trial_data, get_all_clinical_trials
from tools.patent_data import get_patent_data, get_active_patents
from tools.regulatory_data import get_regulatory_data, get_approved_drugs
from tools.scientific_journal_data import get_journal_data, get_all_articles

# Import API models
from models.api_models import (
    QueryRequest,
    OrchestratorResponse,
    HealthResponse,
    ErrorResponse,
    DataToolResponse
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Pharmaceutical Research Orchestrator API",
    description="Multi-agent AI system for pharmaceutical research analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        HealthResponse: Status and version information
    """
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )


@app.get("/info", tags=["Info"])
async def get_info():
    """
    Get API information and available agents
    
    Returns:
        Dictionary with API info and available agents
    """
    logger.info("API info requested")
    return {
        "name": "Pharmaceutical Research Orchestrator API",
        "version": "1.0.0",
        "agents": [
            {
                "name": "clinical_trials",
                "description": "Analyzes clinical trial data, study designs, and patient outcomes"
            },
            {
                "name": "patent",
                "description": "Analyzes patent information, intellectual property, and drug formulations"
            },
            {
                "name": "regulatory",
                "description": "Analyzes FDA approval pathways, drug safety, and compliance"
            },
            {
                "name": "scientific_journal",
                "description": "Analyzes published peer-reviewed research and scientific literature"
            }
        ],
        "endpoints": {
            "query": "/query",
            "query_clinical": "/data/clinical-trials",
            "query_patents": "/data/patents",
            "query_regulatory": "/data/regulatory",
            "query_journal": "/data/journal"
        }
    }


# ============================================================================
# MAIN ORCHESTRATOR ENDPOINT
# ============================================================================

@app.post("/query", response_model=OrchestratorResponse, tags=["Orchestrator"])
async def query_orchestrator(request: QueryRequest):
    """
    Submit a pharmaceutical research query to the orchestrator
    
    The orchestrator will:
    1. Route the query to appropriate specialist agents
    2. Each agent fetches relevant data from its database
    3. Agents provide expert analysis
    4. If multiple agents respond, automatically synthesize findings
    
    Args:
        request (QueryRequest): Query request with pharmaceutical question
        
    Returns:
        OrchestratorResponse: Final analysis with agent responses
        
    Raises:
        HTTPException: If query is invalid or processing fails
        
    Example:
        POST /query
        {
            "query": "What are the clinical trials for cancer drug XYZ?",
            "max_agents": 5
        }
    """
    try:
        # Validate query
        if not request.query or len(request.query.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Query must be at least 3 characters long"
            )
        
        logger.info(f"Processing query: {request.query}")
        
        # Run orchestrator
        final_state = run_orchestrator(request.query)
        
        # Get final response
        final_response = format_response(final_state)
        
        # Determine which agents were consulted
        messages = final_state.get("message", [])
        ai_messages = [m for m in messages if hasattr(m, '__class__') and 'AIMessage' in m.__class__.__name__]
        agent_count = len(ai_messages)
        
        # Determine if synthesis was performed
        synthesis_performed = agent_count > 1
        
        logger.info(f"Query processed successfully. Agents consulted: {agent_count}")
        
        return OrchestratorResponse(
            query=request.query,
            final_response=final_response,
            agents_consulted=[f"agent_{i}" for i in range(agent_count)],
            agent_count=agent_count,
            total_messages=len(messages),
            synthesis_performed=synthesis_performed,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


# ============================================================================
# DATA TOOL ENDPOINTS - Clinical Trials
# ============================================================================

@app.get("/data/clinical-trials", response_model=DataToolResponse, tags=["Data Tools"])
async def get_clinical_trials(query: str = Query(..., description="Search query for clinical trials")):
    """
    Search clinical trials database
    
    Args:
        query: Search term (drug name, NCT number, or phase)
        
    Returns:
        DataToolResponse: Clinical trial data matching the query
        
    Example:
        GET /data/clinical-trials?query=cancer
    """
    try:
        logger.info(f"Clinical trials search: {query}")
        
        result = get_clinical_trial_data(query)
        
        return DataToolResponse(
            tool_name="clinical_trials",
            found=result.get("found", False),
            count=len(result.get("trials", [])),
            data=result.get("trials", [])
        )
        
    except Exception as e:
        logger.error(f"Error searching clinical trials: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching clinical trials: {str(e)}"
        )


@app.get("/data/clinical-trials/all", response_model=DataToolResponse, tags=["Data Tools"])
async def get_all_trials():
    """
    Get all clinical trials from database
    
    Returns:
        DataToolResponse: All clinical trials
    """
    try:
        logger.info("Fetching all clinical trials")
        
        result = get_all_clinical_trials()
        
        return DataToolResponse(
            tool_name="clinical_trials",
            found=result.get("found", False),
            count=len(result.get("trials", [])),
            data=result.get("trials", [])
        )
        
    except Exception as e:
        logger.error(f"Error fetching clinical trials: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching clinical trials: {str(e)}"
        )


# ============================================================================
# DATA TOOL ENDPOINTS - Patents
# ============================================================================

@app.get("/data/patents", response_model=DataToolResponse, tags=["Data Tools"])
async def get_patents(query: str = Query(..., description="Search query for patents")):
    """
    Search patents database
    
    Args:
        query: Search term (patent number, drug name, or company)
        
    Returns:
        DataToolResponse: Patent data matching the query
        
    Example:
        GET /data/patents?query=US10234567
    """
    try:
        logger.info(f"Patent search: {query}")
        
        result = get_patent_data(query)
        
        return DataToolResponse(
            tool_name="patent",
            found=result.get("found", False),
            count=len(result.get("patents", [])),
            data=result.get("patents", [])
        )
        
    except Exception as e:
        logger.error(f"Error searching patents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching patents: {str(e)}"
        )


@app.get("/data/patents/active", response_model=DataToolResponse, tags=["Data Tools"])
async def get_active_patents_endpoint():
    """
    Get all active patents from database
    
    Returns:
        DataToolResponse: All active patents
    """
    try:
        logger.info("Fetching active patents")
        
        result = get_active_patents()
        
        return DataToolResponse(
            tool_name="patent",
            found=result.get("found", False),
            count=len(result.get("patents", [])),
            data=result.get("patents", [])
        )
        
    except Exception as e:
        logger.error(f"Error fetching active patents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching active patents: {str(e)}"
        )


# ============================================================================
# DATA TOOL ENDPOINTS - Regulatory
# ============================================================================

@app.get("/data/regulatory", response_model=DataToolResponse, tags=["Data Tools"])
async def get_regulatory(query: str = Query(..., description="Search query for regulatory data")):
    """
    Search regulatory database
    
    Args:
        query: Search term (drug name, application number, or manufacturer)
        
    Returns:
        DataToolResponse: Regulatory data matching the query
        
    Example:
        GET /data/regulatory?query=DTZ-100
    """
    try:
        logger.info(f"Regulatory search: {query}")
        
        result = get_regulatory_data(query)
        
        return DataToolResponse(
            tool_name="regulatory",
            found=result.get("found", False),
            count=len(result.get("applications", [])),
            data=result.get("applications", [])
        )
        
    except Exception as e:
        logger.error(f"Error searching regulatory data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching regulatory data: {str(e)}"
        )


@app.get("/data/regulatory/approved", response_model=DataToolResponse, tags=["Data Tools"])
async def get_approved_drugs_endpoint():
    """
    Get all FDA approved drugs from database
    
    Returns:
        DataToolResponse: All approved drugs
    """
    try:
        logger.info("Fetching approved drugs")
        
        result = get_approved_drugs()
        
        return DataToolResponse(
            tool_name="regulatory",
            found=result.get("found", False),
            count=len(result.get("applications", [])),
            data=result.get("applications", [])
        )
        
    except Exception as e:
        logger.error(f"Error fetching approved drugs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching approved drugs: {str(e)}"
        )


# ============================================================================
# DATA TOOL ENDPOINTS - Scientific Journal
# ============================================================================

@app.get("/data/journal", response_model=DataToolResponse, tags=["Data Tools"])
async def get_journal(query: str = Query(..., description="Search query for journal articles")):
    """
    Search scientific journal database
    
    Args:
        query: Search term (DOI, title, author, or keyword)
        
    Returns:
        DataToolResponse: Journal articles matching the query
        
    Example:
        GET /data/journal?query=cancer
    """
    try:
        logger.info(f"Journal search: {query}")
        
        result = get_journal_data(query)
        
        return DataToolResponse(
            tool_name="scientific_journal",
            found=result.get("found", False),
            count=len(result.get("articles", [])),
            data=result.get("articles", [])
        )
        
    except Exception as e:
        logger.error(f"Error searching journal: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching journal: {str(e)}"
        )


@app.get("/data/journal/all", response_model=DataToolResponse, tags=["Data Tools"])
async def get_all_journal_articles():
    """
    Get all journal articles from database
    
    Returns:
        DataToolResponse: All journal articles
    """
    try:
        logger.info("Fetching all journal articles")
        
        result = get_all_articles()
        
        return DataToolResponse(
            tool_name="scientific_journal",
            found=result.get("found", False),
            count=len(result.get("articles", [])),
            data=result.get("articles", [])
        )
        
    except Exception as e:
        logger.error(f"Error fetching journal articles: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching journal articles: {str(e)}"
        )


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information
    """
    return {
        "name": "Pharmaceutical Research Orchestrator API",
        "version": "1.0.0",
        "description": "Multi-agent AI system for pharmaceutical research analysis",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "query": "/query",
            "clinical_trials": "/data/clinical-trials",
            "patents": "/data/patents",
            "regulatory": "/data/regulatory",
            "journal": "/data/journal"
        }
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        },
    )


# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log application startup"""
    logger.info("Application started successfully")
    logger.info("Endpoints available at http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown"""
    logger.info("Application shutting down")


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
