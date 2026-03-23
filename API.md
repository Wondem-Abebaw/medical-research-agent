# API Documentation

Comprehensive API documentation for the Medical Research Agent backend.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication

Currently, the API is open access. For production deployments, consider adding API key authentication.

## Endpoints

### Health Check

#### `GET /ping`

Simple health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

**Status Codes:**
- `200`: Service is running

---

#### `GET /api/v1/health`

Detailed health check with service status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-03-22T10:30:00Z",
  "services": {
    "agent": "running",
    "google_ai": "configured",
    "tavily": "configured"
  }
}
```

**Status Codes:**
- `200`: All services healthy

---

### Query Agent

#### `POST /api/v1/query`

Submit a medical research query to the agent.

**Request Body:**
```json
{
  "query": "What are the side effects of metformin?",
  "query_type": "drug_interaction",  // optional
  "session_id": "uuid-here",          // optional
  "max_results": 5,                   // optional, default: 5
  "include_citations": true           // optional, default: true
}
```

**Request Fields:**
- `query` (string, required): The medical research question (min 3 chars)
- `query_type` (string, optional): Query type classification
  - `literature_search`: Research papers/clinical trials
  - `drug_interaction`: Drug information
  - `clinical_question`: Clinical/treatment questions
  - `general`: General medical information
- `session_id` (string, optional): Session ID for conversation history
- `max_results` (integer, optional): Maximum results per tool (1-20)
- `include_citations` (boolean, optional): Include source citations

**Response:**
```json
{
  "query": "What are the side effects of metformin?",
  "answer": "Metformin is commonly associated with gastrointestinal side effects...",
  "query_type": "drug_interaction",
  "sources": [
    {
      "title": "Metformin Safety Profile",
      "authors": ["Smith J", "Johnson A"],
      "journal": "Journal of Diabetes",
      "publication_date": "March 2024",
      "pubmed_id": "12345678",
      "doi": "10.1234/jd.2024.001",
      "url": "https://pubmed.ncbi.nlm.nih.gov/12345678/",
      "snippet": "Study findings on metformin adverse events..."
    }
  ],
  "steps": [
    {
      "step_number": 1,
      "action": "Checking drug information for: metformin",
      "tool_name": "check_drug_info",
      "tool_input": {
        "drug_name": "metformin"
      },
      "observation": "Retrieved drug information for metformin",
      "timestamp": "2024-03-22T10:30:01Z"
    }
  ],
  "execution_time": 3.45,
  "session_id": "uuid-here",
  "error": null
}
```

**Response Fields:**
- `query`: Original query
- `answer`: Comprehensive answer from the agent
- `query_type`: Classified query type
- `sources`: Array of source citations
- `steps`: Array of execution steps
- `execution_time`: Time in seconds
- `session_id`: Session identifier (if provided)
- `error`: Error message (if any)

**Status Codes:**
- `200`: Success
- `422`: Validation error (invalid request body)
- `500`: Agent execution error

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the latest treatments for Type 2 diabetes?",
    "max_results": 5,
    "include_citations": true
  }'
```

---

#### `POST /api/v1/query/stream`

Stream agent responses in real-time (Server-Sent Events).

**Request Body:** Same as `/api/v1/query`

**Response:** Server-Sent Events stream

**Event Types:**

1. **Start Event**
```json
{
  "type": "start",
  "message": "Processing your medical research question...",
  "timestamp": "2024-03-22T10:30:00Z"
}
```

2. **Step Event**
```json
{
  "type": "step",
  "step": {
    "step_number": 1,
    "action": "Searching PubMed for medical literature",
    "tool_name": "search_pubmed",
    "observation": "Found 5 articles",
    "timestamp": "2024-03-22T10:30:01Z"
  }
}
```

3. **Answer Event**
```json
{
  "type": "answer",
  "data": {
    "query": "...",
    "answer": "...",
    "query_type": "literature_search",
    "sources": [...],
    "execution_time": 3.45
  }
}
```

4. **Complete Event**
```json
{
  "type": "complete",
  "timestamp": "2024-03-22T10:30:05Z"
}
```

5. **Error Event**
```json
{
  "type": "error",
  "error": "Error message here",
  "timestamp": "2024-03-22T10:30:02Z"
}
```

**Example JavaScript:**
```javascript
const eventSource = new EventSource('http://localhost:8000/api/v1/query/stream');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'start':
      console.log('Starting:', data.message);
      break;
    case 'step':
      console.log('Step:', data.step.action);
      break;
    case 'answer':
      console.log('Answer:', data.data.answer);
      break;
    case 'complete':
      eventSource.close();
      break;
    case 'error':
      console.error('Error:', data.error);
      eventSource.close();
      break;
  }
};
```

---

### List Tools

#### `GET /api/v1/tools`

List available medical research tools.

**Response:**
```json
{
  "tools": [
    {
      "name": "search_pubmed",
      "description": "Search PubMed/NCBI for peer-reviewed medical literature..."
    },
    {
      "name": "check_drug_info",
      "description": "Check drug information including adverse events..."
    },
    {
      "name": "search_medical_web",
      "description": "Search trusted medical websites..."
    }
  ],
  "count": 3
}
```

**Status Codes:**
- `200`: Success

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid request parameters
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Agent execution failure
- `503 Service Unavailable`: External API unavailable

### Example Error Response

```json
{
  "detail": "Agent execution failed: Google API key not configured"
}
```

---

## Rate Limiting

Currently not implemented. For production, consider:
- 100 requests per minute per IP
- 1000 requests per hour per IP

---

## Data Models

### AgentRequest

```typescript
interface AgentRequest {
  query: string;                    // Required, min 3 chars
  query_type?: QueryType;           // Optional
  session_id?: string;              // Optional
  max_results?: number;             // Optional, 1-20
  include_citations?: boolean;      // Optional
}
```

### AgentResponse

```typescript
interface AgentResponse {
  query: string;
  answer: string;
  query_type: QueryType;
  sources: SourceCitation[];
  steps: AgentStep[];
  execution_time: number;
  session_id?: string;
  error?: string;
}
```

### SourceCitation

```typescript
interface SourceCitation {
  title: string;
  authors?: string[];
  journal?: string;
  publication_date?: string;
  pubmed_id?: string;
  doi?: string;
  url?: string;
  snippet?: string;
}
```

### AgentStep

```typescript
interface AgentStep {
  step_number: number;
  action: string;
  tool_name?: string;
  tool_input?: Record<string, any>;
  observation?: string;
  timestamp: string;
}
```

### QueryType

```typescript
type QueryType = 
  | 'literature_search'
  | 'clinical_trial'
  | 'drug_interaction'
  | 'clinical_question'
  | 'general';
```

---

## Interactive Documentation

When the API is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive documentation where you can:
- Test endpoints directly
- View request/response schemas
- See all available parameters
- Download OpenAPI specification

---

## Best Practices

### 1. Query Construction

**Good queries:**
- "What are the side effects of metformin?"
- "Latest research on Alzheimer's prevention"
- "Diagnostic criteria for Type 2 diabetes"

**Avoid:**
- Very vague queries: "Tell me about health"
- Personal medical advice: "Should I take this medication?"
- Non-medical topics

### 2. Performance

- Average response time: 2-5 seconds
- PubMed queries: 1-3 seconds
- Drug queries: 0.5-2 seconds
- Complex queries: 5-10 seconds

### 3. Caching

Results are not cached by default. Implement client-side caching for repeated queries.

### 4. Error Handling

Always check for the `error` field in responses:

```javascript
const response = await fetch('/api/v1/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'What is diabetes?' })
});

const data = await response.json();

if (data.error) {
  console.error('Agent error:', data.error);
  // Handle error
} else {
  console.log('Answer:', data.answer);
  // Use answer
}
```

---

## SDK Examples

### Python

```python
import requests

def query_agent(query: str):
    url = "http://localhost:8000/api/v1/query"
    payload = {
        "query": query,
        "max_results": 5,
        "include_citations": True
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    return response.json()

# Usage
result = query_agent("What are the side effects of aspirin?")
print(result['answer'])
```

### JavaScript/TypeScript

```typescript
async function queryAgent(query: string) {
  const response = await fetch('http://localhost:8000/api/v1/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      max_results: 5,
      include_citations: true,
    }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return await response.json();
}

// Usage
const result = await queryAgent('What is the mechanism of action of metformin?');
console.log(result.answer);
```

### cURL

```bash
# Basic query
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Latest research on COVID-19 vaccines"}'

# With all options
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the contraindications for aspirin?",
    "query_type": "drug_interaction",
    "max_results": 10,
    "include_citations": true
  }' | jq
```

---

## Versioning

Current API version: **v1**

Base path: `/api/v1`

Future versions will use: `/api/v2`, `/api/v3`, etc.

---

## Support

For API support:
- GitHub Issues: [Report issues]
- Email: support@example.com
- Documentation: Check `/docs` endpoint
