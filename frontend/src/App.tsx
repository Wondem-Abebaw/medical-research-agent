/**
 * Main App component
 */
import React, { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle2, Loader2 } from 'lucide-react';
import ChatInterface from './components/ChatInterface';
import apiService from './services/api';

function App() {
  const [healthStatus, setHealthStatus] = useState<'checking' | 'healthy' | 'unhealthy'>('checking');
  const [errorMessage, setErrorMessage] = useState<string>('');

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      await apiService.ping();
      setHealthStatus('healthy');
    } catch (error: any) {
      console.error('Health check failed:', error);
      setHealthStatus('unhealthy');
      setErrorMessage(
        error.message || 'Unable to connect to the backend. Please ensure the API server is running.'
      );
    }
  };

  if (healthStatus === 'checking') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Connecting to Medical Research Agent...</p>
        </div>
      </div>
    );
  }

  if (healthStatus === 'unhealthy') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <AlertCircle className="w-6 h-6 text-red-600" />
            </div>
            <h1 className="text-xl font-bold text-gray-900">Connection Failed</h1>
          </div>
          
          <p className="text-gray-600 mb-6">{errorMessage}</p>
          
          <div className="bg-gray-50 rounded-lg p-4 mb-6">
            <p className="text-sm text-gray-700 mb-2">
              <strong>Quick troubleshooting:</strong>
            </p>
            <ul className="text-sm text-gray-600 space-y-1 list-disc list-inside">
              <li>Ensure the backend server is running on port 8000</li>
              <li>Check your .env file has GOOGLE_API_KEY configured</li>
              <li>Verify network connectivity</li>
            </ul>
          </div>

          <button
            onClick={checkHealth}
            className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <ChatInterface />
    </div>
  );
}

export default App;
