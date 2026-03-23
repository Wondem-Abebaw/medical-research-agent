# Medical Research Agent - Project Overview

## 📋 Project Summary

A production-ready full-stack AI application that combines LangGraph multi-agent orchestration with medical research APIs to provide evidence-based answers to clinical questions.

**Built for**: AI Engineering Portfolio (Healthcare AI Specialization)
**Tech Stack**: LangGraph, Gemini, FastAPI, React, TypeScript, Docker
**Purpose**: Demonstrate expertise in AI agents, healthcare domain knowledge, and full-stack development

---

## 🎯 What This Project Demonstrates

### AI Engineering Skills
✅ **LangGraph Multi-Agent System**: Intelligent query classification and dynamic tool routing  
✅ **Prompt Engineering**: Crafted system prompts for medical context and citation synthesis  
✅ **Tool Integration**: PubMed API, OpenFDA, Tavily Search integration  
✅ **LLM Orchestration**: Using Google Gemini for reasoning and synthesis  
✅ **Agent Patterns**: React-style reasoning with observation loops  

### Healthcare/Medical Domain
✅ **Medical Data Sources**: PubMed/NCBI integration via BioPython  
✅ **Drug Safety**: FDA adverse event reporting system integration  
✅ **Evidence-Based Medicine**: Citation tracking and source attribution  
✅ **Clinical Terminology**: Proper handling of medical concepts and disclaimers  
✅ **HIPAA Awareness**: Security-minded architecture (ready for compliance)  

### Full-Stack Development
✅ **Production Backend**: FastAPI with Pydantic, Docker, health checks  
✅ **Modern Frontend**: React + TypeScript + Tailwind CSS  
✅ **API Design**: RESTful API with OpenAPI documentation  
✅ **DevOps**: Docker Compose, CI/CD ready, comprehensive logging  
✅ **Type Safety**: End-to-end TypeScript with validated models  

---

## 📂 Project Structure

```
medical-research-agent/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── agents/             # LangGraph agent implementation
│   │   │   ├── graph.py        # Multi-node workflow graph
│   │   │   └── tools.py        # Medical research tools
│   │   ├── api/                # REST API endpoints
│   │   │   └── routes.py       # Agent query routes
│   │   ├── core/               # Configuration
│   │   │   └── config.py       # Pydantic Settings
│   │   ├── models/             # Data models
│   │   │   └── __init__.py     # Request/Response schemas
│   │   └── main.py             # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend container
│   └── .env.example            # Environment template
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── SourceCard.tsx
│   │   │   └── StepViewer.tsx
│   │   ├── services/           # API client
│   │   │   └── api.ts
│   │   ├── types/              # TypeScript definitions
│   │   │   └── index.ts
│   │   ├── App.tsx             # Root component
│   │   └── main.tsx            # Entry point
│   ├── package.json            # Node dependencies
│   ├── tailwind.config.js      # Tailwind CSS config
│   ├── Dockerfile              # Frontend container
│   └── nginx.conf              # Production server config
│
├── docker-compose.yml          # Full-stack orchestration
├── README.md                   # Comprehensive docs
├── API.md                      # API documentation
├── DEPLOYMENT.md               # Deployment guide
├── start.sh                    # Quick start script
├── setup-dev.sh                # Development setup
└── run-dev.sh                  # Dev runner
```

---

## 🔧 Key Technical Components

### 1. LangGraph Agent (`backend/app/agents/graph.py`)

**Multi-Node Architecture:**
```
Query → Classify → Route → [PubMed | Drug | Web] → Synthesize → Answer
```

**State Management:**
- TypedDict with query, steps, results, sources
- Annotated fields for state aggregation
- Error handling at each node

**Tool Routing:**
- Query classification using LLM
- Conditional routing based on query type
- Parallel tool execution capability

### 2. Medical Research Tools (`backend/app/agents/tools.py`)

**PubMed Search:**
- BioPython Entrez integration
- Returns: articles, authors, abstracts, PMIDs
- Structured JSON output for easy parsing

**Drug Interaction Checker:**
- OpenFDA Adverse Event Reporting System
- Async HTTP with aiohttp
- Frequency-ranked adverse reactions

**Medical Web Search:**
- Tavily API with domain filtering
- Trusted sources: NIH, CDC, WHO, Mayo Clinic
- Relevance-scored results

### 3. FastAPI Backend (`backend/app/main.py`)

**Production Features:**
- Pydantic Settings for configuration
- CORS middleware for frontend
- Health check endpoints
- OpenAPI documentation
- Structured logging
- Error handling middleware

### 4. React Frontend (`frontend/src/`)

**Component Architecture:**
- ChatInterface: Main conversation UI
- MessageBubble: User/Assistant messages with markdown
- SourceCard: Citation display with metadata
- StepViewer: Real-time agent execution viewer

**State Management:**
- React hooks for local state
- API service abstraction
- TypeScript for type safety

---

## 🚀 Running the Project

### Quick Start (Docker)
```bash
./start.sh
```

### Development Mode
```bash
./setup-dev.sh    # First time only
./run-dev.sh      # Start both services
```

### Manual Start

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Agent Workflow Example

**Query:** "What are the side effects of metformin?"

**Step 1: Classification**
- LLM classifies as `drug_interaction` query

**Step 2: Routing**
- Agent routes to `check_drug_info` tool

**Step 3: Tool Execution**
```python
tool_input = {"drug_name": "metformin"}
result = OpenFDA.search_adverse_events("metformin")
```

**Step 4: Synthesis**
```
Context: 
- Drug: metformin
- Common reactions: nausea (2,341 reports), diarrhea (1,892 reports)...
- Source: FDA FAERS

Prompt: Synthesize comprehensive answer with safety disclaimer
```

**Step 5: Response**
```
Answer: Metformin commonly causes gastrointestinal side effects...
Sources: [FDA FAERS citation]
Execution time: 3.2s
```

---

## 🎓 Educational Value

### For Interviewers/Reviewers

This project demonstrates:

1. **Domain Expertise**: Healthcare + AI engineering dual competency
2. **Production Mindset**: Docker, logging, error handling, health checks
3. **Modern Stack**: LangGraph (cutting-edge), FastAPI, React, TypeScript
4. **API Integration**: Multiple external APIs coordinated by LLM
5. **User Experience**: Clean UI, real-time feedback, comprehensive citations

### Unique Differentiators

- **Healthcare Focus**: Most portfolio projects are generic chatbots
- **LangGraph**: Advanced orchestration (not just LangChain)
- **Full Stack**: End-to-end implementation with production quality
- **Evidence-Based**: Proper citation tracking and source attribution
- **Compliance-Aware**: Medical disclaimers, HIPAA-mindful architecture

---

## 📈 Future Enhancements

### Phase 1 (Current) ✅
- [x] Multi-tool agent
- [x] PubMed + FDA + web search
- [x] React frontend with real-time UI
- [x] Docker deployment

### Phase 2 (Planned)
- [ ] Conversation memory (LangGraph checkpointing)
- [ ] Document upload for custom research corpus
- [ ] Multi-agent collaboration (research + clinical + safety agents)
- [ ] FHIR data integration

### Phase 3 (Advanced)
- [ ] Fine-tuned medical embeddings
- [ ] Clinical trial data integration (ClinicalTrials.gov)
- [ ] RAG over medical textbooks
- [ ] Compliance features (HIPAA, audit logs)

---

## 💼 Portfolio Positioning

**Resume Bullet:**
> Built production-grade AI medical research agent using LangGraph multi-agent orchestration, integrating PubMed API, FDA databases, and Google Gemini for evidence-based clinical Q&A. Full-stack TypeScript application with FastAPI backend and React frontend, deployed via Docker.

**LinkedIn Project Description:**
> Medical Research Agent - AI Healthcare Assistant  
> A LangGraph-powered application that answers clinical questions by orchestrating multiple medical data sources (PubMed, FDA, trusted health websites). Demonstrates expertise in AI agent design, healthcare domain knowledge, and production full-stack development. Tech: LangGraph, FastAPI, React, TypeScript, Docker.

**GitHub README Highlights:**
- Production-ready code quality
- Comprehensive documentation
- Docker deployment
- Healthcare AI specialization
- Full TypeScript coverage

---

## 📞 Support & Next Steps

**Documentation:**
- README.md - Quick start and features
- API.md - API endpoint documentation
- DEPLOYMENT.md - Production deployment guide

**Getting Help:**
- Check README.md troubleshooting section
- Review backend.log and frontend.log
- Verify API keys in backend/.env

**Contributing:**
- Fork and create feature branches
- Maintain TypeScript strict mode
- Add tests for new features
- Update documentation

---

**Status:** ✅ Production Ready  
**Last Updated:** March 2026  
**License:** MIT  
**Author:** Wonde (AI Engineer specializing in Healthcare)
