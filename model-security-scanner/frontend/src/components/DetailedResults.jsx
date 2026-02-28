import { useState } from 'react'
import { ChevronDown, ChevronRight, CheckCircle, AlertTriangle, XCircle, CircleDot } from 'lucide-react'

const STATUS_MAP = {
  SECURE: { icon: CheckCircle, cls: 'text-green-500', bg: 'bg-green-50' },
  PARTIAL: { icon: AlertTriangle, cls: 'text-amber-500', bg: 'bg-amber-50' },
  VULNERABLE: { icon: XCircle, cls: 'text-red-500', bg: 'bg-red-50' },
  ERROR: { icon: CircleDot, cls: 'text-gray-400', bg: 'bg-gray-50' },
}

function TestCard({ result }) {
  const [open, setOpen] = useState(false)
  const s = STATUS_MAP[result.status] || STATUS_MAP.ERROR
  const Icon = s.icon

  return (
    <div className={`rounded-lg border border-gray-200 overflow-hidden ${s.bg}`}>
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center gap-3 px-4 py-3 text-left"
      >
        <Icon size={18} className={s.cls} />
        <span className="flex-1 text-sm font-medium text-gray-900">{result.test_name}</span>
        <span className="text-xs text-gray-500">{result.points}/{result.max_points} pts</span>
        {open ? <ChevronDown size={16} className="text-gray-400" /> : <ChevronRight size={16} className="text-gray-400" />}
      </button>
      {open && (
        <div className="px-4 pb-4 space-y-3 border-t border-gray-200 bg-white">
          <div className="pt-3">
            <p className="text-xs font-medium text-gray-500 mb-1">Description</p>
            <p className="text-sm text-gray-700">{result.description}</p>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 mb-1">Prompt Sent</p>
            <pre className="text-xs bg-gray-50 rounded p-3 overflow-x-auto whitespace-pre-wrap text-gray-600">{result.prompt}</pre>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 mb-1">Model Response</p>
            <pre className="text-xs bg-gray-50 rounded p-3 overflow-x-auto whitespace-pre-wrap text-gray-600 max-h-48 overflow-y-auto">{result.response}</pre>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 mb-1">Evaluation</p>
            <p className="text-sm text-gray-700">{result.explanation}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default function DetailedResults({ scanResults }) {
  const [openModel, setOpenModel] = useState(null)

  return (
    <div className="space-y-4">
      <h3 className="font-semibold text-gray-900">Detailed Results</h3>
      {scanResults.map(scan => (
        <div key={scan.model} className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <button
            onClick={() => setOpenModel(openModel === scan.model ? null : scan.model)}
            className="w-full flex items-center gap-3 px-6 py-4 text-left hover:bg-gray-50"
          >
            {openModel === scan.model ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            <span className="font-medium text-gray-900">{scan.model}</span>
            <span className="text-sm text-gray-500">{scan.total_score}/{scan.max_score} pts</span>
          </button>
          {openModel === scan.model && (
            <div className="px-6 pb-6 space-y-2">
              {scan.results.map(r => (
                <TestCard key={r.test_id} result={r} />
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
