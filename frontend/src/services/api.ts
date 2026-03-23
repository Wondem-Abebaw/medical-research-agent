/**
 * API service for communicating with the Medical Research Agent backend
 */
import axios, { AxiosInstance } from 'axios';
import type {
  AgentRequest,
  AgentResponse,
  HealthCheckResponse,
  ToolsResponse,
} from '@/types';

class ApiService {
  private client: AxiosInstance;
  private baseURL: string;

  constructor() {
    this.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 300000, // 5 minutes for long-running queries
    });

    // Add request interceptor for logging
    this.client.interceptors.request.use(
      (config) => {
        console.log('API Request:', config.method?.toUpperCase(), config.url);
        return config;
      },
      (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Add response interceptor for logging
    this.client.interceptors.response.use(
      (response) => {
        console.log('API Response:', response.status, response.config.url);
        return response;
      },
      (error) => {
        console.error('API Response Error:', error.response?.status, error.message);
        return Promise.reject(error);
      }
    );
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<HealthCheckResponse> {
    const response = await this.client.get<HealthCheckResponse>('/api/v1/health');
    return response.data;
  }

  /**
   * Query the medical research agent
   */
  async queryAgent(request: AgentRequest): Promise<AgentResponse> {
    const response = await this.client.post<AgentResponse>('/api/v1/query', request);
    return response.data;
  }

  /**
   * List available tools
   */
  async listTools(): Promise<ToolsResponse> {
    const response = await this.client.get<ToolsResponse>('/api/v1/tools');
    return response.data;
  }

  /**
   * Ping the server
   */
  async ping(): Promise<{ status: string }> {
    const response = await this.client.get<{ status: string }>('/ping');
    return response.data;
  }

  /**
   * Get base URL
   */
  getBaseURL(): string {
    return this.baseURL;
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;
