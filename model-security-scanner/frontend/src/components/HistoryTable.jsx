const statusBadge = (pct) => {
  if (pct >= 70) return { cls: 'bg-green-100 text-green-700' }
  if (pct >= 50) return { cls: 'bg-amber-100 text-amber-700' }
  return { cls: 'bg-red-100 text-red-700' }
}

export default function HistoryTable({ history }) {
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
              return (
                <tr key={h.id}>
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
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
