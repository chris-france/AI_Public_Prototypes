import { BarChart3, TrendingUp, ShieldCheck, ShieldAlert } from 'lucide-react'

export default function SummaryStats({ history }) {
  if (!history || history.length === 0) return null

  // Best score per model
  const modelScores = {}
  for (const h of history) {
    const pct = h.max_score > 0 ? (h.total_score / h.max_score) * 100 : 0
    if (!modelScores[h.model_name] || pct > modelScores[h.model_name]) {
      modelScores[h.model_name] = pct
    }
  }

  const models = Object.keys(modelScores)
  const scores = Object.values(modelScores)
  if (models.length === 0) return null

  const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length
  const bestModel = models.reduce((a, b) => modelScores[a] > modelScores[b] ? a : b)
  const worstModel = models.reduce((a, b) => modelScores[a] < modelScores[b] ? a : b)

  const cards = [
    {
      icon: BarChart3,
      label: 'Models Scanned',
      value: models.length,
      color: 'text-france-blue',
      bg: 'bg-france-blue/5',
    },
    {
      icon: TrendingUp,
      label: 'Average Score',
      value: `${avgScore.toFixed(0)}%`,
      color: avgScore >= 70 ? 'text-green-600' : avgScore >= 50 ? 'text-amber-600' : 'text-red-600',
      bg: avgScore >= 70 ? 'bg-green-50' : avgScore >= 50 ? 'bg-amber-50' : 'bg-red-50',
    },
    {
      icon: ShieldCheck,
      label: 'Most Secure',
      value: bestModel.length > 18 ? bestModel.slice(0, 18) + '...' : bestModel,
      sub: `${modelScores[bestModel].toFixed(0)}%`,
      color: 'text-green-600',
      bg: 'bg-green-50',
    },
    {
      icon: ShieldAlert,
      label: 'Least Secure',
      value: worstModel.length > 18 ? worstModel.slice(0, 18) + '...' : worstModel,
      sub: `${modelScores[worstModel].toFixed(0)}%`,
      color: 'text-red-600',
      bg: 'bg-red-50',
    },
  ]

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((c, i) => (
        <div key={i} className={`${c.bg} rounded-xl p-4 border border-gray-100`}>
          <div className="flex items-center gap-2 mb-2">
            <c.icon size={16} className={c.color} />
            <span className="text-xs font-medium text-gray-500">{c.label}</span>
          </div>
          <div className={`text-lg font-bold ${c.color}`}>{c.value}</div>
          {c.sub && <div className="text-xs text-gray-500 mt-0.5">{c.sub}</div>}
        </div>
      ))}
    </div>
  )
}
