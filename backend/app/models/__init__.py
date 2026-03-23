"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class QueryType(str, Enum):
    """Type of medical query."""
    LITERATURE_SEARCH = "literature_search"
    CLINICAL_TRIAL = "clinical_trial"
    DRUG_INTERACTION = "drug_interaction"
    CLINICAL_QUESTION = "clinical_question"
    GENERAL = "general"


class AgentRequest(BaseModel):
    """Request model for agent queries."""
    query: str = Field(..., description="User's medical research question", min_length=3)
    query_type: Optional[QueryType] = Field(None, description="Type of query (auto-detected if not provided)")
    session_id: Optional[str] = Field(None, description="Session ID for conversation history")
    max_results: Optional[int] = Field(5, description="Maximum number of results to return", ge=1, le=20)
    include_citations: bool = Field(True, description="Include source citations in response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the latest treatments for Alzheimer's disease?",
                "query_type": "literature_search",
                "max_results": 5
            }
        }


class SourceCitation(BaseModel):
    """Citation information for sources."""
    title: str
    authors: Optional[List[str]] = None
    journal: Optional[str] = None
    publication_date: Optional[str] = None
    pubmed_id: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    snippet: Optional[str] = None


class AgentStep(BaseModel):
    """Individual step in agent execution."""
    step_number: int
    action: str
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AgentResponse(BaseModel):
    """Response model from agent."""
    query: str
    answer: str
    query_type: QueryType
    sources: List[SourceCitation] = []
    steps: List[AgentStep] = []
    execution_time: float
    session_id: Optional[str] = None
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What are the side effects of metformin?",
                "answer": "Metformin commonly causes gastrointestinal side effects...",
                "query_type": "drug_interaction",
                "sources": [],
                "steps": [],
                "execution_time": 3.45
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    services: Dict[str, str] = {}


class PubMedArticle(BaseModel):
    """PubMed article information."""
    pmid: str
    title: str
    authors: List[str] = []
    abstract: Optional[str] = None
    journal: Optional[str] = None
    publication_date: Optional[str] = None
    doi: Optional[str] = None
    url: str
    
    @property
    def citation(self) -> SourceCitation:
        """Convert to SourceCitation format."""
        return SourceCitation(
            title=self.title,
            authors=self.authors,
            journal=self.journal,
            publication_date=self.publication_date,
            pubmed_id=self.pmid,
            doi=self.doi,
            url=self.url,
            snippet=self.abstract[:200] + "..." if self.abstract and len(self.abstract) > 200 else self.abstract
        )


class DrugInteraction(BaseModel):
    """Drug interaction information."""
    drug1: str
    drug2: Optional[str] = None
    severity: Optional[str] = None
    description: str
    source: str
