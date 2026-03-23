# 🚀 Medical Research Agent - Quick Start Guide

**Congratulations!** You now have a production-ready AI medical research agent that demonstrates your expertise in:
- LangGraph multi-agent orchestration
- Healthcare AI specialization
- Full-stack development (FastAPI + React)
- Production deployment (Docker)

---

## 📦 What You Have

```
medical-research-agent/
├── Backend (FastAPI + LangGraph)
│   - Multi-agent system with intelligent routing
│   - PubMed API integration (BioPython)
│   - FDA drug database integration
│   - Tavily medical web search
│   
├── Frontend (React + TypeScript)
│   - Modern chat interface
│   - Real-time agent step viewer
│   - Source citation display
│   - Responsive design
│   
└── DevOps
    - Docker Compose orchestration
    - Development scripts
    - Production deployment configs
```

---

## ⚡ 5-Minute Setup

### Step 1: Get Your API Keys (2 minutes)

**Required:**
1. **Google AI API Key** (Gemini)
   - Go to: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

**Optional (but recommended):**
2. **Tavily API Key** (for web search)
   - Go to: https://tavily.com
   - Sign up and get free API key

### Step 2: Configure Environment (1 minute)

```bash
cd medical-research-agent/backend
cp .env.example .env
```

Edit `backend/.env` and add your keys:
```env
GOOGLE_API_KEY=your_actual_google_api_key_here
PUBMED_EMAIL=your-email@example.com
TAVILY_API_KEY=your_tavily_key_here  # Optional
```

### Step 3: Launch with Docker (2 minutes)

```bash
cd medical-research-agent
./start.sh
```

That's it! The app will be running at:
- **Frontend:** http://localhost:80
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🛠️ Development Setup (Local Development)

### First Time Setup

```bash
cd medical-research-agent
./setup-dev.sh
```

This will:
- Set up Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies
- Create `.env` files

### Running in Development Mode

```bash
./run-dev.sh
```

This starts:
- Backend with hot reload (http://localhost:8000)
- Frontend with hot reload (http://localhost:5173)

---

## 🧪 Testing the Agent

### Example Queries to Try

1. **PubMed Research:**
   - "What are the latest treatments for Type 2 diabetes?"
   - "What does recent research say about Alzheimer's prevention?"

2. **Drug Information:**
   - "What are the side effects of metformin?"
   - "Tell me about adverse events for aspirin"

3. **Clinical Questions:**
   - "Compare mRNA vaccines and traditional vaccines"
   - "What are the treatment protocols for hypertension?"

### What to Look For

✅ **Query Classification:** Agent automatically detects query type  
✅ **Tool Routing:** Routes to PubMed, FDA, or web search  
✅ **Source Citations:** Each answer includes sources with links  
✅ **Execution Steps:** See the agent's reasoning process  
✅ **Professional UI:** Clean, medical-themed interface  

---

## 📊 Project Architecture

### Backend Flow
```
User Query → FastAPI → LangGraph Agent
                ↓
        Classify Query Type
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
PubMed      FDA API    Tavily
Search      Search     Search
    └───────────┼───────────┘
                ↓
        Synthesize Answer
                ↓
    Return with Citations
```

### Key Technologies

**Backend:**
- `langchain==0.1.6` - Base framework
- `langgraph==0.0.20` - Multi-agent orchestration
- `langchain-google-genai==0.0.6` - Gemini integration
- `fastapi==0.109.0` - REST API
- `biopython==1.83` - PubMed integration
- `pydantic==2.5.3` - Data validation

**Frontend:**
- `react==18.2.0` - UI framework
- `typescript==5.3.3` - Type safety
- `vite==5.0.12` - Build tool
- `tailwindcss==3.4.1` - Styling
- `axios==1.6.5` - HTTP client

---

## 🎯 Portfolio & Resume Usage

### LinkedIn Project Description

```
Medical Research Agent - AI Healthcare Assistant

Built a production-ready AI agent using LangGraph for intelligent 
orchestration of medical data sources (PubMed, FDA databases, trusted 
health websites). The system answers clinical questions with evidence-based 
responses and comprehensive citations.

Tech Stack: LangGraph, Google Gemini, FastAPI, React, TypeScript, Docker
Features: Multi-agent routing, real-time execution tracking, citation 
management, responsive UI

This project demonstrates expertise in AI agent design, healthcare domain 
knowledge, and full-stack production development.
```

### Resume Bullet Points

```
• Developed AI medical research agent using LangGraph multi-agent 
  orchestration, integrating PubMed API, FDA adverse event database, 
  and Google Gemini for evidence-based clinical Q&A

• Built full-stack TypeScript application with FastAPI backend and 
  React frontend, featuring real-time agent execution tracking and 
  comprehensive source citation system

• Implemented production-ready deployment with Docker Compose, 
  health monitoring, and comprehensive API documentation
```

### GitHub Repository Description

```
🏥 AI-powered medical research assistant built with LangGraph & Gemini

Production-ready agent that searches PubMed, FDA databases, and medical 
websites to answer clinical questions with evidence-based citations.

Tech: LangGraph • FastAPI • React • TypeScript • Docker

Features:
✓ Multi-agent orchestration with intelligent routing
✓ Real-time execution tracking
✓ Comprehensive citation management
✓ Production deployment ready
```

---

## 📁 Project Structure Explained

### Backend (`backend/`)

```
app/
├── agents/
│   ├── graph.py      # LangGraph workflow with multi-node architecture
│   └── tools.py      # PubMed, FDA, Tavily tool implementations
├── api/
│   └── routes.py     # FastAPI endpoints (/query, /health, /tools)
├── core/
│   └── config.py     # Pydantic Settings for configuration
├── models/
│   └── __init__.py   # TypedDict models matching frontend types
└── main.py           # FastAPI app with CORS and middleware
```

**Key Files:**
- `graph.py`: Multi-node LangGraph agent with state management
- `tools.py`: Integration with medical APIs
- `routes.py`: REST API endpoints
- `config.py`: Environment-based configuration

### Frontend (`frontend/`)

```
src/
├── components/
│   ├── ChatInterface.tsx   # Main chat UI
│   ├── MessageBubble.tsx   # User/Assistant messages
│   ├── SourceCard.tsx      # Citation display
│   └── StepViewer.tsx      # Agent execution steps
├── services/
│   └── api.ts              # Axios client for backend
├── types/
│   └── index.ts            # TypeScript definitions
└── App.tsx                 # Root component with health check
```

**Key Files:**
- `ChatInterface.tsx`: Main conversation component
- `api.ts`: Type-safe API client
- `types/index.ts`: Shared TypeScript types

---

## 🔍 API Endpoints

### Health Check
```bash
GET /api/v1/health
```
Returns service status and configuration info

### Query Agent
```bash
POST /api/v1/query
Body: {
  "query": "What are the side effects of metformin?",
  "max_results": 5,
  "include_citations": true
}
```
Returns comprehensive answer with sources and execution steps

### List Tools
```bash
GET /api/v1/tools
```
Returns available medical research tools

### Interactive API Docs
```
http://localhost:8000/docs
```

---

## 🚨 Troubleshooting

### Backend Won't Start

**Problem:** `GOOGLE_API_KEY` not found
```bash
# Solution:
cd backend
cat .env  # Verify GOOGLE_API_KEY is set
```

**Problem:** Port 8000 already in use
```bash
# Solution:
# Option 1: Kill existing process
lsof -ti:8000 | xargs kill -9

# Option 2: Change port in backend/.env
PORT=8001
```

### Frontend Won't Connect

**Problem:** CORS error in browser console
```bash
# Solution:
# Verify backend is running
curl http://localhost:8000/ping

# Check CORS settings in backend/.env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:80
```

### Docker Issues

**Problem:** Docker Compose fails
```bash
# Solution:
# Check Docker is running
docker ps

# Rebuild containers
docker-compose down
docker-compose up --build
```

---

## 📚 Next Steps

### 1. Add to GitHub
```bash
cd medical-research-agent
git init
git add .
git commit -m "Initial commit: Medical Research Agent"
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

### 2. Enhance the Project

**Easy Additions:**
- Add more example queries
- Customize UI colors/branding
- Add conversation history
- Implement user sessions

**Medium Complexity:**
- Add RAG with vector database
- Implement conversation memory
- Add document upload for research
- Create export to PDF feature

**Advanced:**
- Multi-agent collaboration
- Fine-tuned medical embeddings
- FHIR data integration
- Clinical trial database integration

### 3. Deploy to Production

**Options:**
- Google Cloud Run (recommended for Gemini integration)
- AWS ECS/Fargate
- Azure Container Instances
- Railway.app or Render.com (easiest)

See `DEPLOYMENT.md` for detailed instructions.

---

## 🎓 Learning Resources

### LangGraph
- Official Docs: https://langchain-ai.github.io/langgraph/
- Multi-Agent Tutorial: https://langchain-ai.github.io/langgraph/tutorials/

### Medical APIs
- PubMed API: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- OpenFDA: https://open.fda.gov/apis/
- BioPython: https://biopython.org/wiki/Documentation

### Healthcare AI
- Google Med-PaLM: Research papers on medical LLMs
- Clinical NLP: BERT models for medical text

---

## ✅ Project Completion Checklist

- [x] Backend with LangGraph multi-agent system
- [x] Three medical research tools integrated
- [x] FastAPI REST API with documentation
- [x] React TypeScript frontend
- [x] Real-time execution tracking
- [x] Source citation system
- [x] Docker deployment
- [x] Development scripts
- [x] Comprehensive documentation
- [x] Production-ready code quality

---

## 🎉 You're Ready!

This project is **portfolio-ready** and demonstrates:
✅ Advanced AI engineering (LangGraph)
✅ Healthcare domain expertise
✅ Full-stack development skills
✅ Production deployment knowledge

**Next Interview Question:**
*"Tell me about a challenging project you built recently."*

**Your Answer:**
*"I built a medical research agent that orchestrates multiple AI tools using LangGraph to answer clinical questions. It integrates PubMed for research papers, FDA databases for drug information, and uses Google Gemini for intelligent synthesis. The full-stack TypeScript application features real-time agent execution tracking and comprehensive citation management. I deployed it with Docker and it's production-ready with health monitoring and API documentation."*

---

**Questions?** Check:
- `README.md` - Comprehensive project documentation
- `API.md` - API endpoint reference
- `DEPLOYMENT.md` - Production deployment guide
- `PROJECT_OVERVIEW.md` - Technical deep dive

**Good luck with your AI engineering interviews!** 🚀🏥
