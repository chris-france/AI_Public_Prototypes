import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#1472CF', '#F59E0B', '#10B981', '#EF4444', '#8B5CF6']

const fmt = v => `$${v.toLocaleString()}`

export default function CumulativeCostChart({ data, gpuType }) {
  const { months, local, ...clouds } = data
  const providers = Object.keys(clouds)

  const chartData = months.map((m, i) => {
    const point = { month: m, [`Local (${gpuType})`]: Math.round(local[i]) }
    providers.forEach(p => { point[p] = Math.round(clouds[p][i]) })
    return point
  })

  const series = [`Local (${gpuType})`, ...providers]

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="font-semibold text-gray-900 mb-4">Cumulative Cost Over 36 Months</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="month" label={{ value: 'Month', position: 'insideBottom', offset: -5 }} />
          <YAxis tickFormatter={fmt} />
          <Tooltip formatter={fmt} />
          <Legend />
          {series.map((s, i) => (
            <Line key={s} type="monotone" dataKey={s} stroke={COLORS[i % COLORS.length]} strokeWidth={2} dot={false} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
