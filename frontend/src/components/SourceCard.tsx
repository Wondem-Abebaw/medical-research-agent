/**
 * SourceCard component for displaying research citations
 */
import React from 'react';
import { ExternalLink, FileText, Database, Globe } from 'lucide-react';
import type { SourceCitation } from '@/types';

interface SourceCardProps {
  source: SourceCitation;
  index: number;
}

const SourceCard: React.FC<SourceCardProps> = ({ source, index }) => {
  const getIcon = () => {
    if (source.pubmed_id) return <FileText className="w-5 h-5 text-primary-600" />;
    if (source.type === 'drug_database') return <Database className="w-5 h-5 text-medical-600" />;
    return <Globe className="w-5 h-5 text-gray-600" />;
  };

  const getTypeLabel = () => {
    if (source.pubmed_id) return 'Research Article';
    if (source.type === 'drug_database') return 'Drug Database';
    return 'Web Resource';
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-1">
          {getIcon()}
        </div>
        
        <div className="flex-1 min-w-0">
          {/* Header */}
          <div className="flex items-start justify-between gap-2 mb-2">
            <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
              {getTypeLabel()} #{index + 1}
            </span>
            {source.url && (
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:text-primary-700 flex-shrink-0"
                title="Open in new tab"
              >
                <ExternalLink className="w-4 h-4" />
              </a>
            )}
          </div>

          {/* Title */}
          <h4 className="font-semibold text-gray-900 mb-2 line-clamp-2">
            {source.title}
          </h4>

          {/* Metadata */}
          <div className="space-y-1 text-sm text-gray-600">
            {source.authors && source.authors.length > 0 && (
              <p className="line-clamp-1">
                <span className="font-medium">Authors:</span>{' '}
                {source.authors.slice(0, 3).join(', ')}
                {source.authors.length > 3 && ` +${source.authors.length - 3} more`}
              </p>
            )}
            
            {source.journal && (
              <p className="line-clamp-1">
                <span className="font-medium">Journal:</span> {source.journal}
              </p>
            )}
            
            {source.publication_date && (
              <p>
                <span className="font-medium">Published:</span> {source.publication_date}
              </p>
            )}
            
            {source.pubmed_id && (
              <p className="font-mono text-xs">
                <span className="font-medium">PMID:</span> {source.pubmed_id}
              </p>
            )}
          </div>

          {/* Snippet */}
          {source.snippet && (
            <p className="mt-3 text-sm text-gray-700 line-clamp-3 italic">
              "{source.snippet}"
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default SourceCard;
