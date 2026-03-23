/**
 * TypeScript types matching backend Pydantic models
 */

export type QueryType = 
  | 'literature_search'
  | 'clinical_trial'
  | 'drug_interaction'
  | 'clinical_question'
  | 'general';

export interface AgentRequest {
  query: string;
  query_type?: QueryType;
  session_id?: string;
  max_results?: number;
  include_citations?: boolean;
}

export interface SourceCitation {
  title: string;
  authors?: string[];
  journal?: string;
  publication_date?: string;
  pubmed_id?: string;
  doi?: string;
  url?: string;
  snippet?: string;
  type?: 'research_article' | 'drug_database' | 'web_resource';
}

export interface AgentStep {
  step_number: number;
  action: string;
  tool_name?: string;
  tool_input?: Record<string, any>;
  observation?: string;
  timestamp: string;
}

export interface AgentResponse {
  query: string;
  answer: string;
  query_type: QueryType;
  sources: SourceCitation[];
  steps: AgentStep[];
  execution_time: number;
  session_id?: string;
  error?: string;
}

export interface HealthCheckResponse {
  status: string;
  version: string;
  timestamp: string;
  services: Record<string, string>;
}

export interface Tool {
  name: string;
  description: string;
}

export interface ToolsResponse {
  tools: Tool[];
  count: number;
}

// Streaming response types
export type StreamMessageType = 'start' | 'step' | 'answer' | 'complete' | 'error';

export interface StreamMessage {
  type: StreamMessageType;
  message?: string;
  step?: AgentStep;
  data?: Partial<AgentResponse>;
  error?: string;
  timestamp: string;
}
