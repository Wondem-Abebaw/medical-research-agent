/**
 * ChatInterface - Main chat component for medical research queries
 */
import React, { useState, useRef, useEffect } from "react";
import { Send, Loader2, AlertTriangle, TrendingUp } from "lucide-react";
import MessageBubble from "./MessageBubble";
import StepViewer from "./StepViewer";
import SourceCard from "./SourceCard";
import apiService from "@/services/api";
import type { AgentResponse, AgentStep, SourceCitation } from "@/types";

interface Message {
  id: string;
  role: "user" | "assistant" | "error";
  content: string;
  timestamp: string;
  steps?: AgentStep[];
  sources?: SourceCitation[];
  executionTime?: number;
}

const EXAMPLE_QUERIES = [
  "What are the latest treatments for Type 2 diabetes?",
  "What are the side effects of metformin?",
  "What does recent research say about Alzheimer's prevention?",
  "Compare mRNA vaccines and traditional vaccines",
];

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showSteps, setShowSteps] = useState(true);
  const [currentSteps, setCurrentSteps] = useState<AgentStep[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentSteps]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const query = input.trim();
    if (!query || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: query,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setCurrentSteps([]);

    try {
      // Query the agent
      const response: AgentResponse = await apiService.queryAgent({
        query,
        max_results: 5,
        include_citations: true,
        session_id: sessionId,
      });

      if (response.session_id) {
        setSessionId(response.session_id);
      }

      // Add assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.answer,
        timestamp: new Date().toISOString(),
        steps: response.steps,
        sources: response.sources,
        executionTime: response.execution_time,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setCurrentSteps([]);
    } catch (error: any) {
      console.error("Query error:", error);

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "error",
        content:
          error.response?.data?.detail ||
          error.message ||
          "Failed to get response from the agent. Please try again.",
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleClick = (example: string) => {
    setInput(example);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex flex-col  bg-gray-50">
      {/* Header */}
      {/* <header className="bg-white border-b border-gray-200 px-6 py-4 flex-shrink-0">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-medical-600 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            Medical Research Agent
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            AI-powered medical research assistant with PubMed, drug databases,
            and clinical knowledge
          </p>
        </div>
      </header> */}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-1">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Welcome message */}
          {messages.length === 0 && !isLoading && (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-600 to-medical-600 rounded-2xl mx-auto mb-4 flex items-center justify-center">
                <TrendingUp className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Welcome to Medical Research Agent
              </h2>
              <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
                Ask medical research questions and get evidence-based answers
                from PubMed, drug databases, and trusted medical sources.
              </p>

              {/* Example queries */}
              <div className="max-w-2xl mx-auto">
                <p className="text-sm font-medium text-gray-700 mb-3">
                  Try these examples:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {EXAMPLE_QUERIES.map((example, index) => (
                    <button
                      key={index}
                      onClick={() => handleExampleClick(example)}
                      className="text-left p-4 bg-white border border-gray-200 rounded-lg hover:border-primary-400 hover:shadow-md transition-all text-sm text-gray-700"
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>

              {/* Disclaimer */}
              <div className="mt-8 max-w-2xl mx-auto bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="flex gap-3">
                  <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                  <div className="text-left">
                    <p className="text-sm font-medium text-yellow-900 mb-1">
                      Medical Disclaimer
                    </p>
                    <p className="text-xs text-yellow-800">
                      This tool provides information for research and
                      educational purposes only. It is not a substitute for
                      professional medical advice, diagnosis, or treatment.
                      Always consult with qualified healthcare providers for
                      medical decisions.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Chat messages */}
          {messages.map((message) => (
            <div key={message.id} className="space-y-4">
              <MessageBubble
                role={message.role}
                content={message.content}
                timestamp={message.timestamp}
              />

              {/* Steps and sources for assistant messages */}
              {message.role === "assistant" && (
                <div className="ml-11 space-y-4">
                  {/* Execution steps */}
                  {showSteps && message.steps && message.steps.length > 0 && (
                    <StepViewer steps={message.steps} />
                  )}

                  {/* Sources */}
                  {message.sources && message.sources.length > 0 && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-700 mb-3">
                        Sources & Citations ({message.sources.length})
                      </h3>
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                        {message.sources.map((source, index) => (
                          <SourceCard
                            key={index}
                            source={source}
                            index={index}
                          />
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Execution time */}
                  {message.executionTime && (
                    <p className="text-xs text-gray-500">
                      Completed in {message.executionTime.toFixed(2)}s
                    </p>
                  )}
                </div>
              )}
            </div>
          ))}

          {/* Loading steps */}
          {isLoading && currentSteps.length > 0 && (
            <div className="ml-11">
              <StepViewer steps={currentSteps} isLoading={true} />
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input form */}
      <div className="flex-shrink-0 bg-white border-t border-gray-200 px-6 py-4">
        <form onSubmit={handleSubmit} className="max-w-6xl mx-auto">
          <div className="flex gap-3 items-end">
            <div className="flex-1">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a medical research question..."
                disabled={isLoading}
                rows={1}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none disabled:bg-gray-100 disabled:cursor-not-allowed"
                style={{ minHeight: "52px", maxHeight: "200px" }}
              />
            </div>
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Researching...</span>
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span>Send</span>
                </>
              )}
            </button>
          </div>

          {/* Options */}
          <div className="flex items-center gap-4 mt-3">
            <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
              <input
                type="checkbox"
                checked={showSteps}
                onChange={(e) => setShowSteps(e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              Show execution steps
            </label>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;
