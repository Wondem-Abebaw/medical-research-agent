"""
Medical research tools for the LangGraph agent.
"""
from langchain.tools import Tool
from langchain_core.tools import StructuredTool
from typing import List, Optional, Dict, Any
import asyncio
from datetime import datetime
import aiohttp
from Bio import Entrez
import json

from app.core.config import settings
from app.models import PubMedArticle, DrugInteraction


class PubMedSearchTool:
    """Tool for searching PubMed/NCBI for medical literature."""
    
    def __init__(self):
        # Configure Entrez with email (required by NCBI)
        Entrez.email = settings.pubmed_email
        Entrez.tool = settings.pubmed_tool
    
    def search_pubmed(self, query: str, max_results: int = 5) -> str:
        """
        Search PubMed for medical literature.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return (default: 5)
            
        Returns:
            JSON string containing article information
        """
        try:
            # Search PubMed
            handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=max_results,
                sort="relevance"
            )
            search_results = Entrez.read(handle)
            handle.close()
            
            id_list = search_results.get("IdList", [])
            
            if not id_list:
                return json.dumps({"articles": [], "message": "No articles found"})
            
            # Fetch article details
            handle = Entrez.efetch(
                db="pubmed",
                id=id_list,
                rettype="medline",
                retmode="xml"
            )
            articles_xml = Entrez.read(handle)
            handle.close()
            
            articles = []
            for article in articles_xml['PubmedArticle']:
                try:
                    medline = article['MedlineCitation']
                    article_data = medline['Article']
                    
                    # Extract authors
                    authors = []
                    if 'AuthorList' in article_data:
                        for author in article_data['AuthorList'][:5]:  # Limit to first 5
                            if 'LastName' in author and 'ForeName' in author:
                                authors.append(f"{author['ForeName']} {author['LastName']}")
                    
                    # Extract abstract
                    abstract = ""
                    if 'Abstract' in article_data:
                        abstract_texts = article_data['Abstract'].get('AbstractText', [])
                        if isinstance(abstract_texts, list):
                            abstract = " ".join(str(text) for text in abstract_texts)
                        else:
                            abstract = str(abstract_texts)
                    
                    # Extract publication date
                    pub_date = ""
                    if 'Journal' in article_data:
                        journal_issue = article_data['Journal'].get('JournalIssue', {})
                        pub_date_dict = journal_issue.get('PubDate', {})
                        year = pub_date_dict.get('Year', '')
                        month = pub_date_dict.get('Month', '')
                        pub_date = f"{month} {year}".strip()
                    
                    pmid = str(medline['PMID'])
                    
                    article_obj = PubMedArticle(
                        pmid=pmid,
                        title=article_data.get('ArticleTitle', 'No title'),
                        authors=authors,
                        abstract=abstract,
                        journal=article_data.get('Journal', {}).get('Title', ''),
                        publication_date=pub_date,
                        doi=None,  # DOI extraction can be added if needed
                        url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    )
                    
                    articles.append(article_obj.model_dump())
                    
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue
            
            return json.dumps({
                "articles": articles,
                "count": len(articles),
                "query": query
            }, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "articles": [],
                "message": f"Error searching PubMed: {str(e)}"
            })


class DrugInteractionTool:
    """Tool for checking drug interactions using OpenFDA API."""
    
    async def check_interaction(self, drug_name: str) -> str:
        """
        Check drug interactions and adverse events.
        
        Args:
            drug_name: Name of the drug to check
            
        Returns:
            JSON string containing drug interaction information
        """
        try:
            # OpenFDA API endpoint for drug adverse events
            base_url = "https://api.fda.gov/drug/event.json"
            
            # Search for drug adverse events
            params = {
                "search": f'patient.drug.openfda.generic_name:"{drug_name}"',
                "limit": 10
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = data.get('results', [])
                        
                        # Extract common reactions
                        reactions = {}
                        for result in results[:20]:
                            patient_reactions = result.get('patient', {}).get('reaction', [])
                            for reaction in patient_reactions:
                                reaction_name = reaction.get('reactionmeddrapt', '').lower()
                                if reaction_name:
                                    reactions[reaction_name] = reactions.get(reaction_name, 0) + 1
                        
                        # Sort by frequency
                        common_reactions = sorted(
                            reactions.items(),
                            key=lambda x: x[1],
                            reverse=True
                        )[:10]
                        
                        return json.dumps({
                            "drug": drug_name,
                            "common_adverse_events": [
                                {"reaction": r[0], "reports": r[1]}
                                for r in common_reactions
                            ],
                            "total_reports": len(results),
                            "source": "FDA Adverse Event Reporting System (FAERS)",
                            "disclaimer": "This data is from FDA reports and should not replace medical advice."
                        }, indent=2)
                    else:
                        return json.dumps({
                            "drug": drug_name,
                            "error": f"API returned status {response.status}",
                            "message": "Could not retrieve drug interaction data"
                        })
                        
        except Exception as e:
            return json.dumps({
                "drug": drug_name,
                "error": str(e),
                "message": f"Error checking drug interactions: {str(e)}"
            })
    
    def check_interaction_sync(self, drug_name: str) -> str:
        """Synchronous wrapper for check_interaction."""
        return asyncio.run(self.check_interaction(drug_name))


class TavilyMedicalSearchTool:
    """Tool for general medical research using Tavily."""
    
    def __init__(self):
        self.api_key = settings.tavily_api_key
    
    async def search(self, query: str, max_results: int = 5) -> str:
        """
        Search for medical information using Tavily.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            JSON string with search results
        """
        if not self.api_key:
            return json.dumps({
                "error": "Tavily API key not configured",
                "results": []
            })
        
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": self.api_key,
                "query": query,
                "search_depth": "advanced",
                "max_results": max_results,
                "include_domains": [
                    "nih.gov",
                    "cdc.gov",
                    "who.int",
                    "mayoclinic.org",
                    "pubmed.ncbi.nlm.nih.gov",
                    "nejm.org",
                    "thelancet.com"
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = data.get('results', [])
                        
                        return json.dumps({
                            "results": [
                                {
                                    "title": r.get('title'),
                                    "url": r.get('url'),
                                    "content": r.get('content'),
                                    "score": r.get('score')
                                }
                                for r in results
                            ],
                            "query": query,
                            "source": "Tavily Search"
                        }, indent=2)
                    else:
                        return json.dumps({
                            "error": f"API returned status {response.status}",
                            "results": []
                        })
                        
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "results": []
            })
    
    def search_sync(self, query: str, max_results: int = 5) -> str:
        """Synchronous wrapper for search."""
        return asyncio.run(self.search(query, max_results))


# Initialize tool instances
pubmed_tool = PubMedSearchTool()
drug_tool = DrugInteractionTool()
tavily_tool = TavilyMedicalSearchTool()


# Create LangChain tools
def create_medical_tools() -> List[Tool]:
    """Create and return all medical research tools."""
    
    tools = [
        StructuredTool.from_function(
            func=pubmed_tool.search_pubmed,
            name="search_pubmed",
            description=(
                "Search PubMed/NCBI for peer-reviewed medical literature, research papers, "
                "and clinical studies. Use this for evidence-based medical information, "
                "research findings, clinical trials, and scientific studies. "
                "Input should be a clear medical search query. "
                "Returns JSON with article titles, authors, abstracts, and PubMed IDs."
            ),
            args_schema=None  # Will be inferred from function signature
        ),
        
        StructuredTool.from_function(
            func=drug_tool.check_interaction_sync,
            name="check_drug_info",
            description=(
                "Check drug information including adverse events and side effects using "
                "FDA data. Use this when asked about drug safety, side effects, or "
                "adverse reactions. Input should be a single drug name (generic or brand). "
                "Returns JSON with common adverse events from FDA reports."
            ),
            args_schema=None
        ),
        
        StructuredTool.from_function(
            func=tavily_tool.search_sync,
            name="search_medical_web",
            description=(
                "Search trusted medical websites (NIH, CDC, WHO, Mayo Clinic, etc.) for "
                "general health information, treatment guidelines, and patient education. "
                "Use this for clinical questions, treatment protocols, or when PubMed "
                "doesn't provide enough context. Input should be a medical question or topic. "
                "Returns JSON with search results from authoritative medical sources."
            ),
            args_schema=None
        )
    ]
    
    return tools
