import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const getColor = (score) => {
  if (score >= 70) return '#22c55e'
  if (score >= 50) return '#eab308'
  return '#ef4444'
}

export default function ComparisonChart({ scanResults = [], history = [] }) {
  // Prefer live scan results when available; fall back to history
  const modelScores = {}

  if (scanResults.length > 0) {
    for (const s of scanResults) {
      const pct = s.max_score > 0 ? (s.total_score / s.max_score) * 100 : 0
      if (!modelScores[s.model] || pct > modelScores[s.model]) {
        modelScores[s.model] = pct
      }
    }
  } else {
    for (const h of history) {
      const pct = h.max_score > 0 ? (h.total_score / h.max_score) * 100 : 0
      if (!modelScores[h.model_name] || pct > modelScores[h.model_name]) {
        modelScores[h.model_name] = pct
      }
    }
  }

  const data = Object.entries(modelScores)
    .sort((a, b) => b[1] - a[1])
    .map(([model, score]) => ({ model, score: Math.round(score) }))

  if (data.length === 0) return null

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="font-semibold text-gray-900 mb-4">Model Security Scores Comparison</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="model" tick={{ fontSize: 11 }} angle={data.length > 4 ? -45 : 0} textAnchor={data.length > 4 ? 'end' : 'middle'} height={data.length > 4 ? 80 : 40} />
          <YAxis domain={[0, 105]} tickFormatter={v => `${v}%`} />
          <Tooltip formatter={v => `${v}%`} />
          <Bar dataKey="score" radius={[6, 6, 0, 0]} label={{ position: 'top', formatter: v => `${v}%`, fontSize: 12 }}>
            {data.map((d, i) => (
              <Cell key={i} fill={getColor(d.score)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
