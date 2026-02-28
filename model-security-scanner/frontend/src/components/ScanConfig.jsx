import { Search, Key, Loader2, CheckCircle } from 'lucide-react'

export default function ScanConfig({ models, loading, selectedModels, setSelectedModels, claudeApiKey, setClaudeApiKey, onScan, scanning }) {
  const toggleModel = (model) => {
    setSelectedModels(prev =>
      prev.includes(model) ? prev.filter(m => m !== model) : [...prev, model]
    )
  }

  const selectAllOllama = () => {
    const allSelected = models.ollama.every(m => selectedModels.includes(m))
    if (allSelected) {
      setSelectedModels(prev => prev.filter(m => !models.ollama.includes(m)))
    } else {
      setSelectedModels(prev => [...new Set([...prev, ...models.ollama])])
    }
  }

  const ollamaSelected = models.ollama.filter(m => selectedModels.includes(m)).length
  const claudeSelected = models.claude.filter(m => selectedModels.includes(m)).length

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <Search size={18} className="text-france-blue" />
          <h2 className="font-semibold text-gray-900">Scan Configuration</h2>
        </div>
        {selectedModels.length > 0 && (
          <span className="text-xs font-medium text-france-blue bg-france-blue/10 px-2.5 py-1 rounded-full">
            {selectedModels.length} selected
          </span>
        )}
      </div>

      {loading ? (
        <div className="flex items-center gap-2 text-gray-400 py-4">
          <Loader2 size={16} className="animate-spin" /> Loading models...
        </div>
      ) : (
        <div className="space-y-5">
          {/* Ollama Models */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-700">
                Ollama Models
                {ollamaSelected > 0 && <span className="text-france-blue ml-1">({ollamaSelected})</span>}
              </h3>
              {models.ollama.length > 0 && (
                <button
                  onClick={selectAllOllama}
                  className="text-xs text-france-blue hover:text-france-blue-dark font-medium"
                >
                  {models.ollama.every(m => selectedModels.includes(m)) ? 'Deselect All' : 'Select All'}
                </button>
              )}
            </div>
            {models.ollama.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {models.ollama.map(m => (
                  <button
                    key={m}
                    onClick={() => toggleModel(m)}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                      selectedModels.includes(m)
                        ? 'bg-france-blue text-white shadow-sm'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {selectedModels.includes(m) && <CheckCircle size={13} />}
                    {m}
                  </button>
                ))}
              </div>
            ) : (
              <p className="text-sm text-amber-600 bg-amber-50 px-3 py-2 rounded-lg">
                No Ollama models found. Is Ollama running?
              </p>
            )}
          </div>

          {/* Divider */}
          <div className="border-t border-gray-100" />

          {/* Claude API */}
          <div>
            <h3 className="text-sm font-medium text-gray-700 mb-2">
              Claude API
              {claudeSelected > 0 && <span className="text-france-blue ml-1">({claudeSelected})</span>}
            </h3>
            <div className="space-y-3">
              <div className="max-w-sm">
                <div className="relative">
                  <Key size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                  <input
                    type="password"
                    placeholder="Anthropic API Key"
                    value={claudeApiKey}
                    onChange={e => setClaudeApiKey(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue"
                  />
                </div>
              </div>
              <div className="flex flex-wrap gap-2">
                {models.claude.map(m => {
                  const shortName = m.replace('claude-', '').split('-202')[0]
                  return (
                    <button
                      key={m}
                      onClick={() => claudeApiKey && toggleModel(m)}
                      disabled={!claudeApiKey}
                      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all disabled:opacity-40 disabled:cursor-not-allowed ${
                        selectedModels.includes(m)
                          ? 'bg-france-blue text-white shadow-sm'
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      {selectedModels.includes(m) && <CheckCircle size={13} />}
                      {shortName}
                    </button>
                  )
                })}
              </div>
              {!claudeApiKey && (
                <p className="text-xs text-gray-400">Enter an API key to enable Claude models</p>
              )}
            </div>
          </div>

          {/* Divider */}
          <div className="border-t border-gray-100" />

          {/* Scan Button */}
          <div className="flex items-center gap-4">
            <button
              onClick={onScan}
              disabled={selectedModels.length === 0 || scanning}
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded-lg bg-france-blue hover:bg-france-blue-dark text-white font-semibold text-sm transition-colors disabled:opacity-40 disabled:cursor-not-allowed shadow-sm"
            >
              {scanning ? <Loader2 size={16} className="animate-spin" /> : <Search size={16} />}
              {scanning ? 'Scanning...' : `Scan Selected (${selectedModels.length})`}
            </button>
            {selectedModels.length === 0 && (
              <span className="text-xs text-gray-400">Select at least one model to begin</span>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
