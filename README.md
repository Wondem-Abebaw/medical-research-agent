# Medical Research Agent 🏥🤖

A production-ready AI-powered medical research assistant that searches PubMed, drug databases, and trusted medical sources to provide evidence-based answers to clinical questions.

![Tech Stack](https://img.shields.io/badge/LangGraph-Agent-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![TypeScript](https://img.shields.io/badge/TypeScript-Typed-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🎯 Features

### Core Capabilities
- **PubMed Search**: Query peer-reviewed medical literature from NCBI/PubMed
- **Drug Information**: Check drug interactions and adverse events from FDA databases
- **Medical Web Search**: Search trusted medical sources (NIH, CDC, WHO, Mayo Clinic)
- **Intelligent Routing**: LangGraph-based agent automatically routes queries to appropriate tools
- **Evidence-Based Answers**: Comprehensive answers with citations and source attribution
- **Real-Time Execution**: View agent steps and reasoning in real-time

### Technical Highlights
- **LangGraph Multi-Agent System**: Intelligent query classification and tool routing
- **Production-Ready**: Docker containers, health checks, error handling, logging
- **Full-Stack TypeScript**: Type-safe frontend with React + TypeScript
- **Modern UI**: Tailwind CSS with responsive design
- **RESTful API**: FastAPI backend with OpenAPI documentation
- **Streaming Support**: Real-time agent execution updates

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                          │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐  │
│  │ ChatInterface│ MessageBubble│  SourceCard  │  StepViewer  │  │
│  └──────────────┴──────────────┴──────────────┴──────────────┘  │
│                           ↓ HTTP/REST                            │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   LangGraph Agent                         │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐          │   │
│  │  │  Classify  │→ │   Route    │→ │ Synthesize │          │   │
│  │  └────────────┘  └─────┬──────┘  └────────────┘          │   │
│  │                         ↓                                 │   │
│  │           ┌─────────────┼─────────────┐                  │   │
│  │           ↓             ↓             ↓                  │   │
│  │    ┌──────────┐  ┌──────────┐  ┌──────────┐             │   │
│  │    │  PubMed  │  │   Drug   │  │   Web    │             │   │
│  │    │  Search  │  │  Checker │  │  Search  │             │   │
│  │    └──────────┘  └──────────┘  └──────────┘             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    External APIs                                 │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐  │
│  │   NCBI/      │   OpenFDA    │    Tavily    │   Google     │  │
│  │   PubMed     │   API        │    Search    │   Gemini     │  │
│  └──────────────┴──────────────┴──────────────┴──────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Workflow

1. **Query Classification**: LLM classifies query type (literature, drug, clinical, general)
2. **Tool Routing**: Routes to appropriate tool(s) based on classification
3. **Tool Execution**: Searches PubMed, drug databases, or medical websites
4. **Answer Synthesis**: LLM synthesizes comprehensive answer with citations

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- OR: Python 3.11+ and Node.js 20+ (for local development)
- Google AI API Key (Gemini)
- Tavily API Key (optional, for web search)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd medical-research-agent
```

2. **Set up environment variables**
```bash
# Backend
cp backend/.env.example backend/.env
# Edit backend/.env and add your API keys
```

Required in `backend/.env`:
```env
GOOGLE_API_KEY=your_google_api_key_here
PUBMED_EMAIL=your-email@example.com
TAVILY_API_KEY=your_tavily_api_key_here  # Optional
```

3. **Start the application**
```bash
docker-compose up -d
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env

# Run development server
npm run dev
```

Access at http://localhost:5173

## 📚 Usage

### Example Queries

**Literature Search:**
```
What are the latest treatments for Type 2 diabetes?
What does recent research say about Alzheimer's prevention?
```

**Drug Information:**
```
What are the side effects of metformin?
Are there any drug interactions between aspirin and ibuprofen?
```

**Clinical Questions:**
```
What are the diagnostic criteria for ADHD in adults?
How effective are mRNA vaccines compared to traditional vaccines?
```

### API Usage

#### Query Endpoint

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the side effects of metformin?",
    "max_results": 5,
    "include_citations": true
  }'
```

#### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Agent Framework**: LangGraph 0.0.20
- **LLM**: Google Gemini (via langchain-google-genai)
- **Tools**: 
  - BioPython (PubMed/NCBI API)
  - Tavily (Medical web search)
  - OpenFDA API (Drug information)
- **Validation**: Pydantic 2.5+
- **Runtime**: Python 3.11

### Frontend
- **Framework**: React 18.2
- **Language**: TypeScript 5.3
- **Build Tool**: Vite 5.0
- **Styling**: Tailwind CSS 3.4
- **HTTP Client**: Axios 1.6
- **Markdown**: react-markdown 9.0
- **Icons**: lucide-react 0.309

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Web Server**: Nginx (production frontend)
- **API Documentation**: OpenAPI/Swagger

## 📁 Project Structure

```
medical-research-agent/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── graph.py          # LangGraph agent implementation
│   │   │   └── tools.py          # Medical research tools
│   │   ├── api/
│   │   │   └── routes.py         # FastAPI routes
│   │   ├── core/
│   │   │   └── config.py         # Configuration management
│   │   ├── models/
│   │   │   └── __init__.py       # Pydantic models
│   │   └── main.py               # FastAPI application
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── SourceCard.tsx
│   │   │   └── StepViewer.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## 🔧 Configuration

### Backend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Google AI API key for Gemini | Yes | - |
| `TAVILY_API_KEY` | Tavily search API key | No | - |
| `PUBMED_EMAIL` | Email for NCBI API (required by NCBI) | Yes | - |
| `MODEL_NAME` | Gemini model name | No | `gemini-1.5-flash` |
| `TEMPERATURE` | LLM temperature | No | `0.7` |
| `DEBUG` | Enable debug mode | No | `false` |

### Frontend Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Backend API URL | No | `http://localhost:8000` |

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🚨 Medical Disclaimer

**IMPORTANT**: This tool is for research and educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions you may have regarding a medical condition.

## 🔒 Data Privacy

- No patient data is stored
- All queries are processed in real-time
- API keys are stored securely in environment variables
- No persistent storage of medical information

## 🤝 Contributing

Contributions are welcome! This project is part of a learning path for AI engineering in healthcare.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **NCBI/PubMed** for medical literature access
- **FDA** for drug safety data
- **Google** for Gemini AI
- **Anthropic** for LangChain/LangGraph inspiration
- **Tavily** for medical web search

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue]
- Email: your-email@example.com

## 🗺️ Roadmap

- [ ] Add session/conversation history
- [ ] Implement user authentication
- [ ] Add more medical databases (DrugBank, ClinicalTrials.gov)
- [ ] Support for medical imaging analysis
- [ ] HIPAA compliance features
- [ ] Deploy to cloud (GCP Cloud Run)
- [ ] Add voice input/output
- [ ] Multi-language support

---

**Built with ❤️ as part of the AI Engineer in Healthcare learning path**
