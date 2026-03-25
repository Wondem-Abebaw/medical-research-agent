"""
API routes for the Medical Research Agent.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from app.models import (
    AgentRequest,
    AgentResponse,
    SourceCitation,
    AgentStep,
    QueryType
)
from app.agents import get_agent
from app.core.memory import memory
from fastapi.responses import Response, FileResponse
import tempfile

router = APIRouter()


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "message": "Medical Research Agent API is running"}


@router.post("/query", response_model=AgentResponse)
async def query_agent(request: AgentRequest):
    """Query the medical research agent with conversation history."""
    try:
        session_id = memory.get_or_create_session(request.session_id)
        history = memory.get_history(session_id, last_n=4)
        
        memory.add_message(session_id, "user", request.query)
        
        agent = get_agent()
        result = agent.run(
            query=request.query,
            max_results=request.max_results,
            conversation_history=history
        )
        
        if result.get("answer"):
            memory.add_message(session_id, "assistant", result["answer"])
        
        if result.get("error"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )
        
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
        
        response = AgentResponse(
            query=result["query"],
            answer=result["answer"],
            query_type=QueryType(result.get("query_type", "general")),
            sources=sources if request.include_citations else [],
            steps=steps,
            execution_time=result["execution_time"],
            session_id=session_id,
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


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Detailed health check with system info."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "components": {
            "api": "operational",
            "agent": "operational",
            "tools": ["pubmed", "fda", "tavily"]
        }
    }


@router.get("/diagram")
async def get_workflow_diagram(format: str = "png"):
    """
    Get visual diagram of the agent workflow
    
    Parameters:
    - format: 'png', 'mermaid', or 'ascii'
    """
    try:
        agent = get_agent()
        
        if format == "png":
            # Generate PNG
            png_data = agent.graph.get_graph().draw_mermaid_png()
            return Response(content=png_data, media_type="image/png")
        
        elif format == "mermaid":
            # Generate Mermaid text
            mermaid_text = agent.graph.get_graph().draw_mermaid()
            return Response(content=mermaid_text, media_type="text/plain")
        
        elif format == "ascii":
            # Generate ASCII
            ascii_text = agent.graph.get_graph().draw_ascii()
            return Response(content=ascii_text, media_type="text/plain")
        
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid format. Use 'png', 'mermaid', or 'ascii'"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate diagram: {str(e)}"
        )


@router.get("/diagram/download")
async def download_diagram():
    """Download workflow diagram as PNG file"""
    try:
        agent = get_agent()
        png_data = agent.graph.get_graph().draw_mermaid_png()
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(png_data)
            tmp_path = tmp.name
        
        return FileResponse(
            tmp_path,
            media_type="image/png",
            filename="medical_research_agent_workflow.png"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate diagram: {str(e)}"
        )