import  { useEffect, useState } from 'react';

interface WorkflowDiagramProps {
  apiUrl?: string;
}

export default function WorkflowDiagram({ 
  apiUrl = `${process.env.VITE_API_URL }api/v1`
}: WorkflowDiagramProps) {
  const [diagramUrl, setDiagramUrl] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDiagram();
  }, []);

  const loadDiagram = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch PNG diagram
      const response = await fetch(`${apiUrl}/diagram?format=png`);
      
      if (!response.ok) {
        throw new Error('Failed to load diagram');
      }
      
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setDiagramUrl(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const downloadDiagram = async () => {
    try {
      const response = await fetch(`${apiUrl}/diagram/download`);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = 'workflow_diagram.png';
      a.click();
      
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download failed:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-gray-600">Loading diagram...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <p className="text-red-600">Error: {error}</p>
        <button 
          onClick={loadDiagram}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">
          Agent Workflow Diagram for Educational Purposes
        </h2>
        <button
          onClick={downloadDiagram}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
        >
          Download PNG
        </button>
      </div>
      
      <div className="border border-gray-200 rounded-lg overflow-hidden bg-white p-4">
        <img 
          src={diagramUrl} 
          alt="Agent Workflow Diagram"
          className="w-full h-auto"
        />
      </div>
      
      <div className="text-sm text-gray-600">
        <p className="font-semibold mb-2">Workflow Explanation:</p>
        <ul className="space-y-1 list-disc list-inside">
          <li><strong>classify:</strong> Determines query type (drug/literature/clinical)</li>
          <li><strong>Router:</strong> Routes to appropriate tool based on classification</li>
          <li><strong>search_pubmed:</strong> Searches medical literature</li>
          <li><strong>check_drug:</strong> Retrieves FDA drug information</li>
          <li><strong>search_web:</strong> Searches trusted medical websites</li>
          <li><strong>synthesize:</strong> Generates final answer from gathered data</li>
        </ul>
      </div>
    </div>
  );
}