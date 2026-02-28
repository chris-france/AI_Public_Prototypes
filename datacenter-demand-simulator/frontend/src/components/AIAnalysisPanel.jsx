import { useState } from 'react'
import { Bot, Loader2 } from 'lucide-react'
import useOllamaStream from '../hooks/useOllamaStream'

export default function AIAnalysisPanel({ summary, ollamaAvailable, ollamaModels }) {
  const [model, setModel] = useState(ollamaModels?.[0] || 'qwen2.5:14b')
  const { text, streaming, start } = useOllamaStream()

  const handleAnalyze = () => {
    start('/api/ai-analysis', { summary, model })
  }

  if (!ollamaAvailable) {
    return (
      <div className="bg-amber-50 border border-amber-200 rounded-xl p-6 text-sm text-amber-700">
        <strong>Ollama is not available.</strong> Start Ollama locally to enable AI-powered analysis.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 flex items-center gap-4">
        <Bot size={20} className="text-france-blue" />
        <select value={model} onChange={e => setModel(e.target.value)}
          className="rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30">
          {ollamaModels?.map(m => <option key={m}>{m}</option>)}
        </select>
        <button onClick={handleAnalyze} disabled={streaming}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-lg bg-france-blue hover:bg-france-blue-dark text-white text-sm font-medium transition-colors disabled:opacity-50">
          {streaming ? <Loader2 size={14} className="animate-spin" /> : <Bot size={14} />}
          {streaming ? 'Analyzing...' : 'Generate Analysis'}
        </button>
      </div>

      {text && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="font-semibold text-gray-900 mb-3">Strategic Capacity Assessment</h3>
          <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">{text}{streaming && <span className="inline-block w-2 h-4 bg-france-blue animate-pulse ml-0.5" />}</div>
        </div>
      )}
    </div>
  )
}
