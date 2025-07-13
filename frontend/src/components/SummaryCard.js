import React from 'react';

const SummaryCard = ({ summary, isLoading }) => {
  return (
    <div className="glass-card p-6 mb-6">
      <div className="flex justify-between items-center mb-4 border-b border-white/10 pb-2">
        <h2 className="text-white text-lg font-semibold flex items-center gap-2">
          <span>📋</span> Meeting Summary
        </h2>
      </div>
      <div className="min-h-[200px] bg-white/10 rounded-lg p-4">
        {isLoading ? (
          <p className="text-white/70 text-sm">Loading summary...</p>
        ) : summary ? (
          <p className="text-white/80 text-sm">{summary}</p>
        ) : (
          <p className="text-white/70 text-sm">No summary available yet.</p>
        )}
      </div>
    </div>
  );
};

export default SummaryCard;
