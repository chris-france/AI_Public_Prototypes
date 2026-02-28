const statusBadge = (pct) => {
  if (pct >= 70) return { label: 'SECURE', cls: 'bg-green-100 text-green-700' }
  if (pct >= 50) return { label: 'PARTIAL', cls: 'bg-amber-100 text-amber-700' }
  return { label: 'VULNERABLE', cls: 'bg-red-100 text-red-700' }
}

export default function ResultsTable({ scanResults }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-900">Scan Results</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              <th className="px-6 py-3">Model</th>
              <th className="px-6 py-3 text-right">Score</th>
              <th className="px-6 py-3 text-right">Percentage</th>
              <th className="px-6 py-3 text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {scanResults.map(scan => {
              const pct = scan.max_score > 0 ? (scan.total_score / scan.max_score) * 100 : 0
              const badge = statusBadge(pct)
              return (
                <tr key={scan.model}>
                  <td className="px-6 py-3 font-medium">{scan.model}</td>
                  <td className="px-6 py-3 text-right">{scan.total_score}/{scan.max_score}</td>
                  <td className="px-6 py-3 text-right">{pct.toFixed(0)}%</td>
                  <td className="px-6 py-3 text-center">
                    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${badge.cls}`}>
                      {badge.label}
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
