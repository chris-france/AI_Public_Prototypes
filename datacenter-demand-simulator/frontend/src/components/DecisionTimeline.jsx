import { AlertTriangle, AlertCircle, Clock, CheckCircle } from 'lucide-react'

const URGENCY = {
  CRITICAL: { icon: AlertCircle, cls: 'border-red-500 bg-red-50', badge: 'bg-red-100 text-red-700' },
  HIGH: { icon: AlertTriangle, cls: 'border-amber-500 bg-amber-50', badge: 'bg-amber-100 text-amber-700' },
  MEDIUM: { icon: Clock, cls: 'border-france-blue bg-france-blue/5', badge: 'bg-blue-100 text-blue-700' },
  LOW: { icon: CheckCircle, cls: 'border-green-500 bg-green-50', badge: 'bg-green-100 text-green-700' },
}

export default function DecisionTimeline({ points }) {
  if (!points.length) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 text-center text-gray-400">
        No critical decision points identified within the projection horizon.
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <h3 className="font-semibold text-gray-900">Decision Points</h3>
      {points.map((dp, i) => {
        const u = URGENCY[dp.urgency] || URGENCY.LOW
        const Icon = u.icon
        return (
          <div key={i} className={`rounded-xl border-l-4 ${u.cls} p-4`}>
            <div className="flex items-start justify-between gap-4">
              <div className="flex items-center gap-3">
                <Icon size={20} className={u.badge.split(' ')[1]} />
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-gray-900">{dp.capacity_type}</span>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${u.badge}`}>{dp.urgency}</span>
                  </div>
                  <p className="text-sm text-gray-600 mt-0.5">Decision deadline: <strong>{dp.decision_deadline}</strong></p>
                </div>
              </div>
              <div className="text-right text-sm">
                <p className="text-gray-500">Utilization: <strong>{(dp.current_utilization * 100).toFixed(0)}%</strong></p>
                <p className="text-gray-500">Expansion: <strong>+{dp.expansion_percentage.toFixed(0)}%</strong></p>
                <p className="text-gray-400 text-xs">Lead time: {dp.lead_time_months}mo</p>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
