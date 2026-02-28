import { useState } from 'react'
import { ChevronDown, ChevronRight, CheckCircle, AlertTriangle, XCircle, CircleDot } from 'lucide-react'

const statusBadge = (pct) => {
  if (pct >= 70) return { cls: 'bg-green-100 text-green-700' }
  if (pct >= 50) return { cls: 'bg-amber-100 text-amber-700' }
  return { cls: 'bg-red-100 text-red-700' }
}

const STATUS_ICON = {
  SECURE: { icon: CheckCircle, cls: 'text-green-500', bg: 'bg-green-50' },
  PARTIAL: { icon: AlertTriangle, cls: 'text-amber-500', bg: 'bg-amber-50' },
  VULNERABLE: { icon: XCircle, cls: 'text-red-500', bg: 'bg-red-50' },
  ERROR: { icon: CircleDot, cls: 'text-gray-400', bg: 'bg-gray-50' },
}

function TestDetail({ result }) {
  const [open, setOpen] = useState(false)
  const s = STATUS_ICON[result.status] || STATUS_ICON.ERROR
  const Icon = s.icon

  return (
    <div className={`rounded-lg border border-gray-200 overflow-hidden ${s.bg}`}>
      <button onClick={() => setOpen(!open)} className="w-full flex items-center gap-3 px-4 py-2.5 text-left">
        <Icon size={16} className={s.cls} />
        <span className="flex-1 text-xs font-medium text-gray-900">{result.test_name}</span>
        <span className="text-xs text-gray-500">{result.points}/{result.max_points} pts</span>
        {open ? <ChevronDown size={14} className="text-gray-400" /> : <ChevronRight size={14} className="text-gray-400" />}
      </button>
      {open && (
        <div className="px-4 pb-3 space-y-2 border-t border-gray-200 bg-white">
          <div className="pt-2">
            <p className="text-xs font-medium text-gray-500 mb-1">Description</p>
            <p className="text-xs text-gray-700">{result.description}</p>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 mb-1">Prompt Sent</p>
            <pre className="text-xs bg-gray-50 rounded p-2 overflow-x-auto whitespace-pre-wrap text-gray-600">{result.prompt}</pre>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 mb-1">Model Response</p>
            <pre className="text-xs bg-gray-50 rounded p-2 overflow-x-auto whitespace-pre-wrap text-gray-600 max-h-40 overflow-y-auto">{result.response}</pre>
          </div>
          <div>
            <p className="text-xs font-medium text-gray-500 mb-1">Evaluation</p>
            <p className="text-xs text-gray-700">{result.explanation}</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default function HistoryTable({ history }) {
  const [expandedId, setExpandedId] = useState(null)

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
        <h3 className="font-semibold text-gray-900">Scan History</h3>
        <div className="flex gap-2">
          <a href="/api/export/csv" className="px-3 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-xs font-medium text-gray-700 transition-colors">
            Export CSV
          </a>
          <a href="/api/export/json" className="px-3 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-xs font-medium text-gray-700 transition-colors">
            Export JSON
          </a>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              <th className="px-6 py-3 w-8"></th>
              <th className="px-6 py-3">ID</th>
              <th className="px-6 py-3">Model</th>
              <th className="px-6 py-3">Date</th>
              <th className="px-6 py-3 text-right">Score</th>
              <th className="px-6 py-3 text-right">Percentage</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {history.map(h => {
              const pct = h.max_score > 0 ? (h.total_score / h.max_score) * 100 : 0
              const badge = statusBadge(pct)
              const isExpanded = expandedId === h.id
              return (
                <>
                  <tr
                    key={h.id}
                    className="cursor-pointer hover:bg-gray-50 transition-colors"
                    onClick={() => setExpandedId(isExpanded ? null : h.id)}
                  >
                    <td className="pl-6 py-3">
                      {isExpanded
                        ? <ChevronDown size={14} className="text-gray-400" />
                        : <ChevronRight size={14} className="text-gray-400" />
                      }
                    </td>
                    <td className="px-6 py-3 text-gray-400">#{h.id}</td>
                    <td className="px-6 py-3 font-medium">{h.model_name}</td>
                    <td className="px-6 py-3 text-gray-500">{h.scan_date.slice(0, 19).replace('T', ' ')}</td>
                    <td className="px-6 py-3 text-right">{h.total_score}/{h.max_score}</td>
                    <td className="px-6 py-3 text-right">
                      <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${badge.cls}`}>
                        {pct.toFixed(0)}%
                      </span>
                    </td>
                  </tr>
                  {isExpanded && h.results && h.results.length > 0 && (
                    <tr key={`${h.id}-detail`}>
                      <td colSpan={6} className="px-6 py-4 bg-gray-50">
                        <div className="space-y-2 max-w-4xl">
                          {h.results.map(r => (
                            <TestDetail key={r.test_id} result={r} />
                          ))}
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
