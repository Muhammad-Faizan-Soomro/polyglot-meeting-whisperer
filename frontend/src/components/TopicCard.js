// components/TopicCard.js
import React from 'react';

const TopicCard = ({ topics, isLoading }) => {
  return (
    <div className="glass-card p-6 mb-6">
      <div className="flex justify-between items-center mb-4 border-b border-white/10 pb-2">
        <h2 className="text-white text-lg font-semibold flex items-center gap-2">
          <span>🏷</span> Extracted Topics
        </h2>
      </div>
      <div className="min-h-[200px] bg-white/10 rounded-lg p-4">
        {isLoading ? (
          <p className="text-white/70 text-sm">Loading topics...</p>
        ) : topics.length > 0 ? (
          <ul className="space-y-3">
            {topics.map((topic, index) => (
              <li key={index} className="text-white/80 text-sm">
                <span className="font-semibold">{index + 1}. </span>{topic}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-white/70 text-sm">No topics extracted yet.</p>
        )}
      </div>
    </div>
  );
};

export default TopicCard;
