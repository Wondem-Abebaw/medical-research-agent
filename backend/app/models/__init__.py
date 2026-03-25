"""
Pydantic models for the Medical Research Agent API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class QueryType(str, Enum):
    """Types of medical queries."""
    literature_search = "literature_search"
    drug_interaction = "drug_interaction"
    clinical_question = "clinical_question"
    general = "general"


class AgentRequest(BaseModel):
    """Request model for agent queries."""
    query: str = Field(..., description="The medical research question")
    max_results: int = Field(default=5, description="Maximum results per source")
    include_citations: bool = Field(default=True, description="Include source citations")
    session_id: Optional[str] = Field(default=None, description="Session ID for conversation continuity")


class SourceCitation(BaseModel):
    """Citation information for a source."""
    title: str
    authors: Optional[List[str]] = None
    journal: Optional[str] = None
    publication_date: Optional[str] = None
    pubmed_id: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    snippet: Optional[str] = None


class AgentStep(BaseModel):
    """A step in the agent's reasoning process."""
    step_number: int
    action: str
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat())


class AgentResponse(BaseModel):
    """Response model from the agent."""
    query: str
    answer: str
    query_type: QueryType
    sources: List[SourceCitation] = []
    steps: List[AgentStep] = []
    execution_time: float
    session_id: str
    error: Optional[str] = None


class PubMedArticle(BaseModel):
    """PubMed article information."""
    pmid: str
    title: str
    authors: List[str]
    abstract: str
    journal: str
    publication_date: str
    doi: Optional[str] = None
    url: str


class DrugInteraction(BaseModel):
    """Drug interaction information."""
    drug_name: str
    interactions: List[Dict[str, Any]]
    adverse_events: List[Dict[str, Any]]
    source: str