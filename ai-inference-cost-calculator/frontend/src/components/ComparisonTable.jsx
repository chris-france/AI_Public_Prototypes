const fmt = (v, d = 2) => v.toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: d, maximumFractionDigits: d })

export default function ComparisonTable({ results, gpuType }) {
  const { local, cloud } = results

  const rows = [
    { option: `Local (${gpuType})`, monthly: local.monthly, tco: local.three_year_tco, per1k: local.per_1k },
    ...Object.entries(cloud).map(([name, d]) => ({
      option: name, monthly: d.monthly, tco: d.three_year_tco, per1k: d.per_1k,
    })),
  ]

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-900">Detailed Comparison</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              <th className="px-6 py-3">Option</th>
              <th className="px-6 py-3 text-right">Monthly</th>
              <th className="px-6 py-3 text-right">3-Year TCO</th>
              <th className="px-6 py-3 text-right">Per 1k Inferences</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {rows.map((r, i) => (
              <tr key={i} className={i === 0 ? 'bg-france-blue/5 font-medium' : ''}>
                <td className="px-6 py-3">{r.option}</td>
                <td className="px-6 py-3 text-right">{fmt(r.monthly)}</td>
                <td className="px-6 py-3 text-right">{fmt(r.tco)}</td>
                <td className="px-6 py-3 text-right">{fmt(r.per1k, 4)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
