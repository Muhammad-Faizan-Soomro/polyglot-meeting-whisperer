// components/TranscriptCard.js
import React from 'react';

const TranscriptCard = ({ transcript, isLoading }) => {
  return (
    <div className="glass-card p-6 mb-6">
      <div className="flex justify-between items-center mb-4 border-b border-white/10 pb-2">
        <h2 className="text-white text-lg font-semibold flex items-center gap-2">
          <span>🌐</span> Original Transcript
        </h2>
      </div>
      <div className="min-h-[200px] bg-white/10 rounded-lg p-4 overflow-y-auto max-h-[300px]">
        {isLoading ? (
          <p className="text-white/70 text-sm">Loading transcript...</p>
        ) : transcript.length > 0 ? (
          <ul className="space-y-3">
            {transcript.map((line, index) => (
              <li key={index} className="text-white/80 text-sm">
                <span className="font-semibold">{line.speaker || 'Speaker'}:</span> {line.text}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-white/70 text-sm">No transcript available yet.</p>
        )}
      </div>
    </div>
  );
};

export default TranscriptCard;
