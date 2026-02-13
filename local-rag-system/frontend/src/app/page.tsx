"use client";

import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Chat from "./components/Chat";
import Context from "./components/Context";
import Settings from "./components/Settings";

export interface ContextChunk {
  text: string;
  filename: string;
  page: number | null;
  chunk_index: number;
  score: number;
}

export interface ChatSettings {
  top_k: number;
  temperature: number;
  chunk_size: number;
}

export default function Home() {
  const [context, setContext] = useState<ContextChunk[]>([]);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [chatSettings, setChatSettings] = useState<ChatSettings>({
    top_k: 5,
    temperature: 0.7,
    chunk_size: 512,
  });
  const [refreshDocs, setRefreshDocs] = useState(0);

  return (
    <div className="flex h-screen">
      <Sidebar
        refreshKey={refreshDocs}
        onUpload={() => setRefreshDocs((n) => n + 1)}
      />
      <div className="flex-1 flex flex-col">
        <header className="flex items-center justify-between px-6 py-3 border-b border-gray-800">
          <h1 className="text-lg font-semibold">Local RAG Chat</h1>
          <button
            onClick={() => setSettingsOpen(true)}
            className="text-sm px-3 py-1.5 rounded bg-gray-800 hover:bg-gray-700"
          >
            Settings
          </button>
        </header>
        <Chat settings={chatSettings} onContext={setContext} />
      </div>
      <Context chunks={context} />
      {settingsOpen && (
        <Settings
          settings={chatSettings}
          onChange={setChatSettings}
          onClose={() => setSettingsOpen(false)}
        />
      )}
    </div>
  );
}
