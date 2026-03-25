"""
Medical research tools for the LangGraph agent.
"""
from langchain_core.tools import StructuredTool
from typing import List, Optional, Dict, Any
from datetime import datetime
from Bio import Entrez
import json
import requests

from app.core.config import settings
from app.models import PubMedArticle, DrugInteraction


class PubMedSearchTool:
    """Tool for searching PubMed/NCBI for medical literature."""
    
    def __init__(self):
        Entrez.email = settings.pubmed_email
        Entrez.tool = settings.pubmed_tool
    
    def search_pubmed(self, query: str, max_results: int = 5) -> str:
        """Search PubMed for medical literature."""
        try:
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
                    
                    authors = []
                    if 'AuthorList' in article_data:
                        for author in article_data['AuthorList'][:5]:
                            if 'LastName' in author and 'ForeName' in author:
                                authors.append(f"{author['ForeName']} {author['LastName']}")
                    
                    abstract = ""
                    if 'Abstract' in article_data:
                        abstract_texts = article_data['Abstract'].get('AbstractText', [])
                        if isinstance(abstract_texts, list):
                            abstract = " ".join(str(text) for text in abstract_texts)
                        else:
                            abstract = str(abstract_texts)
                    
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
                        doi=None,
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
    
    def check_interaction(self, drug_name: str) -> str:
        """Check drug interactions and adverse events."""
        try:
            base_url = "https://api.fda.gov/drug/event.json"
            params = {
                "search": f'patient.drug.openfda.generic_name:"{drug_name}"',
                "limit": 10
            }
            
            response = requests.get(base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                reactions = {}
                for result in results[:20]:
                    patient_reactions = result.get('patient', {}).get('reaction', [])
                    for reaction in patient_reactions:
                        reaction_name = reaction.get('reactionmeddrapt', '').lower()
                        if reaction_name:
                            reactions[reaction_name] = reactions.get(reaction_name, 0) + 1
                
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
                    "error": f"API returned status {response.status_code}",
                    "message": "Could not retrieve drug interaction data"
                })
                    
        except Exception as e:
            return json.dumps({
                "drug": drug_name,
                "error": str(e),
                "message": f"Error checking drug interactions: {str(e)}"
            })


class TavilyMedicalSearchTool:
    """Tool for general medical research using Tavily."""
    
    def __init__(self):
        self.api_key = settings.tavily_api_key
    
    def search(self, query: str, max_results: int = 5) -> str:
        """Search for medical information using Tavily."""
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
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
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
                    "error": f"API returned status {response.status_code}",
                    "results": []
                })
                    
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "results": []
            })


pubmed_tool = PubMedSearchTool()
drug_tool = DrugInteractionTool()
tavily_tool = TavilyMedicalSearchTool()


def create_medical_tools() -> List[StructuredTool]:
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
            )
        ),
        
        StructuredTool.from_function(
            func=drug_tool.check_interaction,
            name="check_drug_info",
            description=(
                "Check drug information including adverse events and side effects using "
                "FDA data. Use this when asked about drug safety, side effects, or "
                "adverse reactions. Input should be a single drug name (generic or brand). "
                "Returns JSON with common adverse events from FDA reports."
            )
        ),
        
        StructuredTool.from_function(
            func=tavily_tool.search,
            name="search_medical_web",
            description=(
                "Search trusted medical websites (NIH, CDC, WHO, Mayo Clinic, etc.) for "
                "general health information, treatment guidelines, and patient education. "
                "Use this for clinical questions, treatment protocols, or when PubMed "
                "doesn't provide enough context. Input should be a medical question or topic. "
                "Returns JSON with search results from authoritative medical sources."
            )
        )
    ]
    
    return tools