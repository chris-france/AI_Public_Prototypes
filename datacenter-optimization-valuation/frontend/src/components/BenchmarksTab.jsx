import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const fmtM = v => `$${(v / 1e6).toFixed(1)}M`

export default function BenchmarksTab() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/benchmarks').then(r => r.json()).then(setData)
  }, [])

  if (!data) return <div className="flex justify-center py-10"><div className="animate-spin rounded-full h-8 w-8 border-2 border-france-blue border-t-transparent" /></div>

  const regions = Object.values(data).sort((a, b) => a.capex_per_mw - b.capex_per_mw)
  const chartData = regions.map(r => ({ region: r.region.split(' ')[0], capex: +(r.capex_per_mw / 1e6).toFixed(1), comp: +(r.transaction_comp_per_mw / 1e6).toFixed(1) }))

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="font-semibold text-gray-900 mb-4">CapEx per MW by Region</h3>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis dataKey="region" tick={{ fontSize: 10 }} angle={-45} textAnchor="end" height={80} />
            <YAxis tickFormatter={v => `$${v}M`} />
            <Tooltip />
            <Bar dataKey="capex" name="CapEx/MW" fill="#1472CF" radius={[4, 4, 0, 0]} />
            <Bar dataKey="comp" name="Transaction Comp/MW" fill="#0891B2" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Regional Benchmarks</h3></div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                <th className="px-4 py-3">Region</th><th className="px-4 py-3 text-right">Tier</th>
                <th className="px-4 py-3 text-right">CapEx/MW</th><th className="px-4 py-3 text-right">Power $/kWh</th>
                <th className="px-4 py-3 text-right">PUE</th><th className="px-4 py-3 text-right">Utilization</th>
                <th className="px-4 py-3 text-right">Comp/MW</th><th className="px-4 py-3 text-right">Growth</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {regions.map(r => (
                <tr key={r.region}>
                  <td className="px-4 py-3 font-medium">{r.region}</td>
                  <td className="px-4 py-3 text-right">{r.tier}</td>
                  <td className="px-4 py-3 text-right">{fmtM(r.capex_per_mw)}</td>
                  <td className="px-4 py-3 text-right">${r.power_cost_kwh.toFixed(3)}</td>
                  <td className="px-4 py-3 text-right">{r.avg_pue.toFixed(2)}</td>
                  <td className="px-4 py-3 text-right">{(r.market_utilization * 100).toFixed(0)}%</td>
                  <td className="px-4 py-3 text-right">{fmtM(r.transaction_comp_per_mw)}</td>
                  <td className="px-4 py-3 text-right">{(r.demand_growth * 100).toFixed(0)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
