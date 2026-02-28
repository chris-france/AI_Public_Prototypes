import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const COLORS = ['#1472CF', '#F59E0B', '#10B981', '#EF4444', '#8B5CF6']

export default function CostPerInferenceChart({ results, gpuType }) {
  const { local, cloud } = results

  const data = [
    { name: `Local (${gpuType})`, value: local.per_1k },
    ...Object.entries(cloud).map(([name, d]) => ({ name, value: d.per_1k })),
  ]

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="font-semibold text-gray-900 mb-4">Cost per 1,000 Inferences</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis dataKey="name" tick={{ fontSize: 12 }} />
          <YAxis tickFormatter={v => `$${v}`} />
          <Tooltip formatter={v => `$${v.toFixed(4)}`} />
          <Bar dataKey="value" radius={[6, 6, 0, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
