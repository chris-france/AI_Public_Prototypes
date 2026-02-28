import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = { Conservative: '#22c55e', 'Base Case': '#1472CF', Aggressive: '#F59E0B', 'Technology Disruption': '#EF4444' }

export default function ScenarioComparison({ scenarios, comparison }) {
  const names = Object.keys(comparison.scenarios)
  const metrics = ['compute', 'storage', 'power']
  const labels = { compute: 'Compute (Cores)', storage: 'Storage (TB)', power: 'Power (MW)' }

  const data = metrics.map(m => {
    const row = { metric: labels[m] }
    for (const n of names) {
      row[n] = Math.round(comparison.scenarios[n][m])
    }
    return row
  })

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="font-semibold text-gray-900 mb-4">Scenario Comparison (Year {comparison.horizon})</h3>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis dataKey="metric" tick={{ fontSize: 12 }} />
            <YAxis tickFormatter={v => v >= 1000 ? `${(v/1000).toFixed(1)}k` : v} />
            <Tooltip />
            <Legend />
            {names.map(n => (
              <Bar key={n} dataKey={n} fill={COLORS[n]} radius={[4, 4, 0, 0]} />
            ))}
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Risk Heatmap */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="font-semibold text-gray-900 mb-4">Growth Risk Heatmap</h3>
        <div className="grid grid-cols-5 gap-1 text-xs">
          <div className="font-medium text-gray-500 p-2" />
          {names.map(n => <div key={n} className="font-medium text-gray-700 p-2 text-center">{n}</div>)}
          {['compute', 'storage', 'power', 'network'].map(metric => {
            const vals = names.map(n => scenarios[n][metric][scenarios[n][metric].length - 1])
            const max = Math.max(...vals)
            return (
              <div key={metric} className="contents">
                <div className="font-medium text-gray-600 p-2 capitalize">{metric}</div>
                {vals.map((v, i) => {
                  const intensity = v / max
                  const bg = intensity > 0.8 ? 'bg-red-200' : intensity > 0.5 ? 'bg-amber-200' : 'bg-green-200'
                  return <div key={i} className={`${bg} p-2 text-center rounded font-medium`}>{v >= 1000 ? `${(v/1000).toFixed(1)}k` : v.toFixed(1)}</div>
                })}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
