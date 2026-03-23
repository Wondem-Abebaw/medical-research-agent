/**
 * StepViewer component for visualizing agent execution steps
 */
import React from 'react';
import { CheckCircle2, Loader2, Search, Database, Globe } from 'lucide-react';
import type { AgentStep } from '@/types';
import { formatDistanceToNow } from 'date-fns';

interface StepViewerProps {
  steps: AgentStep[];
  isLoading?: boolean;
}

const StepViewer: React.FC<StepViewerProps> = ({ steps, isLoading = false }) => {
  const getToolIcon = (toolName?: string) => {
    if (!toolName) return <Search className="w-4 h-4" />;
    
    if (toolName.includes('pubmed')) return <Search className="w-4 h-4 text-primary-600" />;
    if (toolName.includes('drug')) return <Database className="w-4 h-4 text-medical-600" />;
    if (toolName.includes('web')) return <Globe className="w-4 h-4 text-gray-600" />;
    
    return <Search className="w-4 h-4" />;
  };

  const formatTime = (timestamp: string) => {
    try {
      return formatDistanceToNow(new Date(timestamp), { addSuffix: true });
    } catch {
      return '';
    }
  };

  if (steps.length === 0 && !isLoading) {
    return null;
  }

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
        {isLoading ? (
          <Loader2 className="w-4 h-4 animate-spin text-primary-600" />
        ) : (
          <CheckCircle2 className="w-4 h-4 text-medical-600" />
        )}
        Agent Execution Steps
      </h3>

      <div className="space-y-3">
        {steps.map((step, index) => (
          <div
            key={index}
            className="bg-white border border-gray-200 rounded-md p-3 hover:border-primary-300 transition-colors"
          >
            {/* Step Header */}
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 mt-0.5">
                <div className="w-6 h-6 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center text-xs font-semibold">
                  {step.step_number}
                </div>
              </div>

              <div className="flex-1 min-w-0">
                {/* Action */}
                <div className="flex items-center gap-2 mb-1">
                  {getToolIcon(step.tool_name)}
                  <p className="text-sm font-medium text-gray-900">
                    {step.action}
                  </p>
                </div>

                {/* Tool Info */}
                {step.tool_name && (
                  <p className="text-xs text-gray-500 mb-2">
                    Tool: <span className="font-mono">{step.tool_name}</span>
                  </p>
                )}

                {/* Observation */}
                {step.observation && (
                  <p className="text-sm text-gray-700 mt-2 p-2 bg-gray-50 rounded border border-gray-100">
                    {step.observation}
                  </p>
                )}

                {/* Timestamp */}
                {step.timestamp && (
                  <p className="text-xs text-gray-400 mt-2">
                    {formatTime(step.timestamp)}
                  </p>
                )}
              </div>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="bg-white border border-gray-200 rounded-md p-3 animate-pulse">
            <div className="flex items-center gap-3">
              <Loader2 className="w-4 h-4 animate-spin text-primary-600" />
              <p className="text-sm text-gray-600">Processing...</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StepViewer;
