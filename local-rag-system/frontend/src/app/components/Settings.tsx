"use client";

import type { ChatSettings } from "../page";

export default function Settings({
  settings,
  onChange,
  onClose,
}: {
  settings: ChatSettings;
  onChange: (s: ChatSettings) => void;
  onClose: () => void;
}) {
  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 w-96">
        <h2 className="text-lg font-semibold mb-4">Settings</h2>

        <label className="block mb-4">
          <span className="text-sm text-gray-400">
            Top K retrieval: {settings.top_k}
          </span>
          <input
            type="range"
            min={1}
            max={20}
            value={settings.top_k}
            onChange={(e) =>
              onChange({ ...settings, top_k: Number(e.target.value) })
            }
            className="w-full mt-1"
          />
        </label>

        <label className="block mb-4">
          <span className="text-sm text-gray-400">
            Temperature: {settings.temperature.toFixed(2)}
          </span>
          <input
            type="range"
            min={0}
            max={100}
            value={settings.temperature * 100}
            onChange={(e) =>
              onChange({
                ...settings,
                temperature: Number(e.target.value) / 100,
              })
            }
            className="w-full mt-1"
          />
        </label>

        <label className="block mb-6">
          <span className="text-sm text-gray-400">
            Chunk size: {settings.chunk_size}
          </span>
          <input
            type="range"
            min={128}
            max={2048}
            step={64}
            value={settings.chunk_size}
            onChange={(e) =>
              onChange({ ...settings, chunk_size: Number(e.target.value) })
            }
            className="w-full mt-1"
          />
        </label>

        <button
          onClick={onClose}
          className="w-full py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-medium"
        >
          Close
        </button>
      </div>
    </div>
  );
}
