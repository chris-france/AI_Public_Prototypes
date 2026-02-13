"use client";

import type { ContextChunk } from "../page";

export default function Context({ chunks }: { chunks: ContextChunk[] }) {
  return (
    <aside className="w-80 border-l border-gray-800 flex flex-col">
      <div className="p-4 border-b border-gray-800">
        <h2 className="font-semibold">Retrieved Context</h2>
        <p className="text-xs text-gray-500 mt-1">
          {chunks.length > 0
            ? `${chunks.length} chunks retrieved`
            : "Context will appear here after a query"}
        </p>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {chunks.map((chunk, i) => (
          <div key={i} className="bg-gray-900 rounded-lg p-3 text-sm">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-blue-400">
                {chunk.filename}
                {chunk.page != null && ` p.${chunk.page}`}
              </span>
              <span
                className={`text-xs font-mono px-1.5 py-0.5 rounded ${
                  chunk.score > 0.7
                    ? "bg-green-900 text-green-300"
                    : chunk.score > 0.4
                    ? "bg-yellow-900 text-yellow-300"
                    : "bg-red-900 text-red-300"
                }`}
              >
                {(chunk.score * 100).toFixed(1)}%
              </span>
            </div>
            <p className="text-gray-300 text-xs leading-relaxed line-clamp-6">
              {chunk.text}
            </p>
          </div>
        ))}
      </div>
    </aside>
  );
}
