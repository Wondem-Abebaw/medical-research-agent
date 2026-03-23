"""
FastAPI routes for medical research agent.
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
import json
import asyncio
from datetime import datetime
from typing import AsyncGenerator

from app.models import (
    AgentRequest,
    AgentResponse,
    HealthCheckResponse,
    QueryType,
    AgentStep,
    SourceCitation
)
from app.agents import get_agent
from app.core.config import settings


router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    agent = get_agent()
    
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        services={
            "agent": "running",
            "google_ai": "configured" if settings.google_api_key else "not configured",
            "tavily": "configured" if settings.tavily_api_key else "not configured"
        }
    )


@router.post("/query", response_model=AgentResponse)
async def query_agent(request: AgentRequest):
    """
    Query the medical research agent.
    
    This endpoint processes medical research questions and returns comprehensive answers
    with citations from PubMed, drug databases, and trusted medical websites.
    """
    try:
        # Get agent instance
        agent = get_agent()
        
        # Run agent
        result = agent.run(
            query=request.query,
            max_results=request.max_results
        )
        
        # Handle errors
        if result.get("error"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
        # Convert sources to SourceCitation models
        sources = []
        for source in result.get("sources", []):
            sources.append(SourceCitation(
                title=source.get("title", ""),
                authors=source.get("authors"),
                journal=source.get("journal"),
                publication_date=source.get("publication_date"),
                pubmed_id=source.get("pubmed_id"),
                doi=source.get("doi"),
                url=source.get("url"),
                snippet=source.get("snippet")
            ))
        
        # Convert steps to AgentStep models
        steps = []
        for step_data in result.get("steps", []):
            steps.append(AgentStep(
                step_number=step_data.step_number,
                action=step_data.action,
                tool_name=step_data.tool_name,
                tool_input=step_data.tool_input,
                observation=step_data.observation,
                timestamp=step_data.timestamp
            ))
        
        # Build response
        response = AgentResponse(
            query=result["query"],
            answer=result["answer"],
            query_type=QueryType(result.get("query_type", "general")),
            sources=sources if request.include_citations else [],
            steps=steps,
            execution_time=result["execution_time"],
            session_id=request.session_id,
            error=None
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )


async def generate_streaming_response(query: str, max_results: int) -> AsyncGenerator[str, None]:
    """Generate streaming response for agent execution."""
    agent = get_agent()
    
    # Send initial message
    yield json.dumps({
        "type": "start",
        "message": "Processing your medical research question...",
        "timestamp": datetime.utcnow().isoformat()
    }) + "\n"
    
    try:
        # Run agent (in real production, this would be async)
        result = await asyncio.to_thread(agent.run, query, max_results)
        
        # Stream steps
        for step in result.get("steps", []):
            yield json.dumps({
                "type": "step",
                "step": {
                    "step_number": step.step_number,
                    "action": step.action,
                    "tool_name": step.tool_name,
                    "observation": step.observation,
                    "timestamp": step.timestamp.isoformat()
                }
            }) + "\n"
            await asyncio.sleep(0.1)  # Small delay for UX
        
        # Stream final answer
        yield json.dumps({
            "type": "answer",
            "data": {
                "query": result["query"],
                "answer": result["answer"],
                "query_type": result.get("query_type"),
                "sources": result.get("sources", []),
                "execution_time": result["execution_time"]
            }
        }) + "\n"
        
        # Send completion
        yield json.dumps({
            "type": "complete",
            "timestamp": datetime.utcnow().isoformat()
        }) + "\n"
        
    except Exception as e:
        yield json.dumps({
            "type": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }) + "\n"


@router.post("/query/stream")
async def query_agent_stream(request: AgentRequest):
    """
    Stream agent responses in real-time.
    
    Returns Server-Sent Events (SSE) stream of agent execution.
    """
    return StreamingResponse(
        generate_streaming_response(request.query, request.max_results),
        media_type="text/event-stream"
    )


@router.get("/tools")
async def list_tools():
    """List available medical research tools."""
    agent = get_agent()
    
    tools_info = []
    for tool in agent.tools:
        tools_info.append({
            "name": tool.name,
            "description": tool.description
        })
    
    return {
        "tools": tools_info,
        "count": len(tools_info)
    }
