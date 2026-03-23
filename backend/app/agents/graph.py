"""
LangGraph agent implementation for medical research.
"""
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import operator
import time
import json

from app.core.config import settings
from app.agents.tools import create_medical_tools
from app.models import AgentStep, QueryType


class AgentState(TypedDict):
    """State for the medical research agent."""
    # Input
    query: str
    query_type: QueryType
    max_results: int
    
    # Processing
    messages: Annotated[List[Dict[str, Any]], operator.add]
    steps: Annotated[List[AgentStep], operator.add]
    
    # Tool results
    pubmed_results: List[Dict[str, Any]]
    drug_info: List[Dict[str, Any]]
    web_results: List[Dict[str, Any]]
    
    # Output
    answer: str
    sources: List[Dict[str, Any]]
    error: str | None
    
    # Metadata
    iteration: int
    start_time: float


class MedicalResearchAgent:
    """LangGraph-based medical research agent."""
    
    def __init__(self):
        """Initialize the agent with LLM and tools."""
        # Initialize Gemini
        self.llm = ChatGoogleGenerativeAI(
            model=settings.model_name,
            google_api_key=settings.google_api_key,
            temperature=settings.temperature,
            max_output_tokens=settings.max_tokens
        )
        
        # Create tools
        self.tools = create_medical_tools()
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _classify_query(self, state: AgentState) -> AgentState:
        """Classify the type of medical query."""
        query = state["query"]
        
        # Use LLM to classify
        classification_prompt = f"""Classify this medical query into one of these categories:
- literature_search: Looking for research papers, studies, clinical trials
- drug_interaction: Questions about drug safety, side effects, interactions
- clinical_question: General clinical/medical questions, treatment protocols
- general: Other medical information requests

Query: {query}

Respond with ONLY the category name, nothing else."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=classification_prompt)])
            query_type = response.content.strip().lower()
            
            # Validate and set query type
            if query_type in ["literature_search", "drug_interaction", "clinical_question", "general"]:
                state["query_type"] = query_type
            else:
                state["query_type"] = "general"
                
        except Exception as e:
            print(f"Classification error: {e}")
            state["query_type"] = "general"
        
        return state
    
    def _route_query(self, state: AgentState) -> str:
        """Route query to appropriate tool based on classification."""
        query_type = state.get("query_type", "general")
        
        # Route based on query type
        if query_type == "literature_search":
            return "search_pubmed"
        elif query_type == "drug_interaction":
            return "check_drug"
        elif query_type == "clinical_question":
            return "search_web"
        else:
            # For general queries, use web search
            return "search_web"
    
    def _search_pubmed_node(self, state: AgentState) -> AgentState:
        """Node for searching PubMed."""
        query = state["query"]
        max_results = state.get("max_results", 5)
        
        step = AgentStep(
            step_number=state.get("iteration", 0) + 1,
            action="Searching PubMed for medical literature",
            tool_name="search_pubmed",
            tool_input={"query": query, "max_results": max_results}
        )
        
        try:
            # Get PubMed tool
            pubmed_tool = next(t for t in self.tools if t.name == "search_pubmed")
            result = pubmed_tool.func(query=query, max_results=max_results)
            
            # Parse results
            result_data = json.loads(result)
            articles = result_data.get("articles", [])
            
            step.observation = f"Found {len(articles)} articles"
            
            state["pubmed_results"] = articles
            state["steps"] = [step]
            state["iteration"] = state.get("iteration", 0) + 1
            
        except Exception as e:
            step.observation = f"Error: {str(e)}"
            state["error"] = str(e)
            state["steps"] = [step]
        
        return state
    
    def _check_drug_node(self, state: AgentState) -> AgentState:
        """Node for checking drug interactions."""
        query = state["query"]
        
        # Extract drug name from query using LLM
        extract_prompt = f"""Extract the drug name from this query. Return ONLY the drug name, nothing else.
Query: {query}"""
        
        try:
            response = self.llm.invoke([HumanMessage(content=extract_prompt)])
            drug_name = response.content.strip()
            
            step = AgentStep(
                step_number=state.get("iteration", 0) + 1,
                action=f"Checking drug information for: {drug_name}",
                tool_name="check_drug_info",
                tool_input={"drug_name": drug_name}
            )
            
            # Get drug tool
            drug_tool = next(t for t in self.tools if t.name == "check_drug_info")
            result = drug_tool.func(drug_name=drug_name)
            
            # Parse results
            result_data = json.loads(result)
            
            step.observation = f"Retrieved drug information for {drug_name}"
            
            state["drug_info"] = [result_data]
            state["steps"] = [step]
            state["iteration"] = state.get("iteration", 0) + 1
            
        except Exception as e:
            step = AgentStep(
                step_number=state.get("iteration", 0) + 1,
                action="Checking drug information",
                observation=f"Error: {str(e)}"
            )
            state["error"] = str(e)
            state["steps"] = [step]
        
        return state
    
    def _search_web_node(self, state: AgentState) -> AgentState:
        """Node for searching medical websites."""
        query = state["query"]
        max_results = state.get("max_results", 5)
        
        step = AgentStep(
            step_number=state.get("iteration", 0) + 1,
            action="Searching trusted medical websites",
            tool_name="search_medical_web",
            tool_input={"query": query, "max_results": max_results}
        )
        
        try:
            # Get web search tool
            web_tool = next(t for t in self.tools if t.name == "search_medical_web")
            result = web_tool.func(query=query, max_results=max_results)
            
            # Parse results
            result_data = json.loads(result)
            results = result_data.get("results", [])
            
            step.observation = f"Found {len(results)} web results"
            
            state["web_results"] = results
            state["steps"] = [step]
            state["iteration"] = state.get("iteration", 0) + 1
            
        except Exception as e:
            step.observation = f"Error: {str(e)}"
            state["error"] = str(e)
            state["steps"] = [step]
        
        return state
    
    def _synthesize_answer_node(self, state: AgentState) -> AgentState:
        """Synthesize final answer from all gathered information."""
        query = state["query"]
        query_type = state.get("query_type", "general")
        
        # Gather all results
        pubmed_results = state.get("pubmed_results", [])
        drug_info = state.get("drug_info", [])
        web_results = state.get("web_results", [])
        
        # Build context for LLM
        context_parts = []
        sources = []
        
        if pubmed_results:
            context_parts.append("=== PubMed Research Articles ===")
            for article in pubmed_results[:5]:
                context_parts.append(f"\nTitle: {article.get('title', 'N/A')}")
                context_parts.append(f"Authors: {', '.join(article.get('authors', []))}")
                context_parts.append(f"Journal: {article.get('journal', 'N/A')}")
                context_parts.append(f"Abstract: {article.get('abstract', 'N/A')[:500]}...")
                context_parts.append(f"URL: {article.get('url', 'N/A')}\n")
                
                # Add to sources
                sources.append({
                    "title": article.get("title"),
                    "authors": article.get("authors"),
                    "journal": article.get("journal"),
                    "pubmed_id": article.get("pmid"),
                    "url": article.get("url"),
                    "type": "research_article"
                })
        
        if drug_info:
            context_parts.append("\n=== Drug Safety Information ===")
            for drug in drug_info:
                context_parts.append(f"\nDrug: {drug.get('drug', 'N/A')}")
                context_parts.append(f"Source: {drug.get('source', 'N/A')}")
                
                adverse_events = drug.get('common_adverse_events', [])
                if adverse_events:
                    context_parts.append("Common Adverse Events:")
                    for event in adverse_events[:10]:
                        context_parts.append(f"  - {event.get('reaction', 'N/A')} ({event.get('reports', 0)} reports)")
                
                sources.append({
                    "title": f"Drug Information: {drug.get('drug')}",
                    "source": drug.get("source"),
                    "type": "drug_database"
                })
        
        if web_results:
            context_parts.append("\n=== Medical Web Resources ===")
            for result in web_results[:5]:
                context_parts.append(f"\nTitle: {result.get('title', 'N/A')}")
                context_parts.append(f"Content: {result.get('content', 'N/A')[:400]}...")
                context_parts.append(f"URL: {result.get('url', 'N/A')}\n")
                
                sources.append({
                    "title": result.get("title"),
                    "url": result.get("url"),
                    "type": "web_resource"
                })
        
        context = "\n".join(context_parts)
        
        # Create synthesis prompt
        synthesis_prompt = f"""You are a medical research assistant. Based on the following information, provide a comprehensive, accurate answer to the user's question.

User Question: {query}
Query Type: {query_type}

Available Information:
{context}

Instructions:
1. Provide a clear, comprehensive answer based ONLY on the information provided above
2. Cite specific sources when making claims
3. If the information is insufficient, acknowledge the limitations
4. Use medical terminology appropriately but explain complex concepts
5. Include relevant statistics or findings from the research
6. For drug information, always include safety disclaimers
7. Structure your answer in a clear, logical way

Answer:"""
        
        try:
            response = self.llm.invoke([HumanMessage(content=synthesis_prompt)])
            answer = response.content.strip()
            
            step = AgentStep(
                step_number=state.get("iteration", 0) + 1,
                action="Synthesizing comprehensive answer from all sources",
                observation=f"Generated answer with {len(sources)} citations"
            )
            
            state["answer"] = answer
            state["sources"] = sources
            state["steps"] = [step]
            state["iteration"] = state.get("iteration", 0) + 1
            
        except Exception as e:
            state["error"] = f"Error synthesizing answer: {str(e)}"
            state["answer"] = "I apologize, but I encountered an error while synthesizing the answer."
        
        return state
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("classify", self._classify_query)
        workflow.add_node("search_pubmed", self._search_pubmed_node)
        workflow.add_node("check_drug", self._check_drug_node)
        workflow.add_node("search_web", self._search_web_node)
        workflow.add_node("synthesize", self._synthesize_answer_node)
        
        # Set entry point
        workflow.set_entry_point("classify")
        
        # Add conditional routing from classify
        workflow.add_conditional_edges(
            "classify",
            self._route_query,
            {
                "search_pubmed": "search_pubmed",
                "check_drug": "check_drug",
                "search_web": "search_web"
            }
        )
        
        # All tool nodes go to synthesize
        workflow.add_edge("search_pubmed", "synthesize")
        workflow.add_edge("check_drug", "synthesize")
        workflow.add_edge("search_web", "synthesize")
        
        # Synthesize is the end
        workflow.add_edge("synthesize", END)
        
        return workflow.compile()
    
    def run(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Run the agent on a query.
        
        Args:
            query: The medical research question
            max_results: Maximum results to return
            
        Returns:
            Dictionary with answer, sources, and execution details
        """
        # Initialize state
        initial_state: AgentState = {
            "query": query,
            "query_type": "general",
            "max_results": max_results,
            "messages": [],
            "steps": [],
            "pubmed_results": [],
            "drug_info": [],
            "web_results": [],
            "answer": "",
            "sources": [],
            "error": None,
            "iteration": 0,
            "start_time": time.time()
        }
        
        # Run the graph
        try:
            final_state = self.graph.invoke(initial_state)
            
            execution_time = time.time() - final_state["start_time"]
            
            return {
                "query": query,
                "query_type": final_state.get("query_type", "general"),
                "answer": final_state.get("answer", ""),
                "sources": final_state.get("sources", []),
                "steps": final_state.get("steps", []),
                "execution_time": execution_time,
                "error": final_state.get("error")
            }
            
        except Exception as e:
            return {
                "query": query,
                "query_type": "general",
                "answer": "",
                "sources": [],
                "steps": [],
                "execution_time": time.time() - initial_state["start_time"],
                "error": str(e)
            }


# Global agent instance
_agent_instance = None


def get_agent() -> MedicalResearchAgent:
    """Get or create the global agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = MedicalResearchAgent()
    return _agent_instance
