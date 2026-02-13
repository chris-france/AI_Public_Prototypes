"use client";

import { useCallback, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";

const API = "http://localhost:8000";

interface Doc {
  filename: string;
  chunks: number;
  timestamp: number;
}

export default function Sidebar({
  refreshKey,
  onUpload,
}: {
  refreshKey: number;
  onUpload: () => void;
}) {
  const [docs, setDocs] = useState<Doc[]>([]);
  const [uploading, setUploading] = useState(false);

  const fetchDocs = useCallback(async () => {
    try {
      const res = await fetch(`${API}/collections`);
      const data = await res.json();
      setDocs(data.documents || []);
    } catch {}
  }, []);

  useEffect(() => {
    fetchDocs();
  }, [fetchDocs, refreshKey]);

  const onDrop = useCallback(
    async (files: File[]) => {
      setUploading(true);
      for (const file of files) {
        const form = new FormData();
        form.append("file", file);
        try {
          await fetch(`${API}/upload`, { method: "POST", body: form });
        } catch {}
      }
      setUploading(false);
      onUpload();
    },
    [onUpload]
  );

  const deleteDoc = async (filename: string) => {
    await fetch(`${API}/collections/${encodeURIComponent(filename)}`, {
      method: "DELETE",
    });
    onUpload();
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "text/plain": [".txt"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
    },
  });

  return (
    <aside className="w-72 border-r border-gray-800 flex flex-col">
      <div className="p-4 border-b border-gray-800">
        <h2 className="font-semibold mb-3">Documents</h2>
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-4 text-center text-sm cursor-pointer transition ${
            isDragActive
              ? "border-blue-500 bg-blue-500/10"
              : "border-gray-700 hover:border-gray-500"
          }`}
        >
          <input {...getInputProps()} />
          {uploading
            ? "Uploading..."
            : isDragActive
            ? "Drop files here"
            : "Drop PDF, TXT, or DOCX files here"}
        </div>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {docs.length === 0 && (
          <p className="text-sm text-gray-500">No documents yet</p>
        )}
        {docs.map((doc) => (
          <div
            key={doc.filename}
            className="flex items-center justify-between bg-gray-900 rounded p-2 text-sm"
          >
            <div className="min-w-0">
              <p className="truncate font-medium">{doc.filename}</p>
              <p className="text-gray-500 text-xs">{doc.chunks} chunks</p>
            </div>
            <button
              onClick={() => deleteDoc(doc.filename)}
              className="text-gray-500 hover:text-red-400 ml-2 shrink-0"
            >
              &times;
            </button>
          </div>
        ))}
      </div>
    </aside>
  );
}
