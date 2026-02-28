import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const SCENARIO_COLORS = {
  Conservative: '#22c55e',
  'Base Case': '#1472CF',
  Aggressive: '#F59E0B',
  'Technology Disruption': '#EF4444',
}

function CapacityChart({ scenarios, metric, title, unit }) {
  const scenarioNames = Object.keys(scenarios)
  const years = scenarios[scenarioNames[0]].years

  const data = years.map((year, i) => {
    const point = { year }
    for (const name of scenarioNames) {
      point[name] = scenarios[name][metric][i]
    }
    return point
  })

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <h4 className="font-semibold text-sm text-gray-900 mb-3">{title}</h4>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="year" tick={{ fontSize: 11 }} />
          <YAxis tickFormatter={v => unit === 'MW' ? v.toFixed(2) : v >= 1000 ? `${(v/1000).toFixed(1)}k` : v.toFixed(0)} tick={{ fontSize: 11 }} />
          <Tooltip formatter={(v) => [`${v.toLocaleString(undefined, { maximumFractionDigits: 1 })} ${unit}`, '']} />
          <Legend wrapperStyle={{ fontSize: 11 }} />
          {scenarioNames.map(name => (
            <Line key={name} type="monotone" dataKey={name} stroke={SCENARIO_COLORS[name] || '#888'} strokeWidth={2} dot={false} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function CapacityCharts({ scenarios }) {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <CapacityChart scenarios={scenarios} metric="compute" title="Compute Capacity" unit="Cores" />
      <CapacityChart scenarios={scenarios} metric="storage" title="Storage Capacity" unit="TB" />
      <CapacityChart scenarios={scenarios} metric="power" title="Power Requirement" unit="MW" />
      <CapacityChart scenarios={scenarios} metric="network" title="Network Bandwidth" unit="Gbps" />
    </div>
  )
}
