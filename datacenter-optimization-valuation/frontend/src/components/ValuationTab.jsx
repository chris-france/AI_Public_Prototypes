import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { Loader2, Bot } from 'lucide-react'
import useOllamaStream from '../hooks/useOllamaStream'

const fmtM = v => `$${(v / 1e6).toFixed(1)}M`

export default function ValuationTab() {
  const [regions, setRegions] = useState([])
  const [form, setForm] = useState({
    asking_price: 250_000_000, claimed_capacity_mw: 20, actual_utilization: 0.72,
    current_pue: 1.42, contract_quality: 'mixed', contract_term_years: 4.5,
    expansion_capacity_mw: 10, building_age_years: 6, land_owned: true,
    land_acres: 15, region: 'Northern Virginia (NOVA)',
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const { text: aiText, streaming, start: startAI } = useOllamaStream()

  useEffect(() => {
    fetch('/api/deployment/config').then(r => r.json()).then(c => setRegions(c.regions))
  }, [])

  const analyze = () => {
    setLoading(true)
    fetch('/api/valuation/analyze', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      .then(r => r.json()).then(setResult).finally(() => setLoading(false))
  }

  const set = (k, v) => setForm(p => ({ ...p, [k]: v }))

  // Waterfall data
  const waterfallData = result ? [
    { name: 'Base Value', value: result.base_value / 1e6, fill: '#1472CF' },
    ...result.adjustments.map(a => ({ name: a.factor, value: a.impact / 1e6, fill: a.impact >= 0 ? '#10B981' : '#EF4444' })),
    { name: 'Fair Value', value: result.adjusted_value / 1e6, fill: '#1472CF' },
    { name: 'Asking', value: result.asking_price / 1e6, fill: '#8B5CF6' },
  ] : []

  const statusColor = result?.valuation_status?.includes('under') ? 'text-green-600' : result?.valuation_status?.includes('over') ? 'text-red-600' : 'text-blue-600'

  return (
    <div className="space-y-6">
      {/* Form */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="font-semibold text-gray-900 mb-4">M&A Asset Valuation</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Asking Price ($M)</label>
            <input type="number" value={form.asking_price / 1e6} onChange={e => set('asking_price', +e.target.value * 1e6)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Capacity (MW)</label>
            <input type="number" min={1} value={form.claimed_capacity_mw} onChange={e => set('claimed_capacity_mw', +e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Utilization: {(form.actual_utilization*100).toFixed(0)}%</label>
            <input type="range" min={10} max={100} value={form.actual_utilization*100} onChange={e => set('actual_utilization', +e.target.value/100)} className="w-full accent-france-blue" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">PUE</label>
            <input type="number" step={0.01} min={1.0} value={form.current_pue} onChange={e => set('current_pue', +e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Region</label>
            <select value={form.region} onChange={e => set('region', e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm">
              {regions.map(r => <option key={r}>{r}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Contract Quality</label>
            <select value={form.contract_quality} onChange={e => set('contract_quality', e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm">
              <option value="hyperscale">Hyperscale</option><option value="enterprise">Enterprise</option>
              <option value="mixed">Mixed</option><option value="retail">Retail/SMB</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Contract Term (yr)</label>
            <input type="number" step={0.5} min={0.5} value={form.contract_term_years} onChange={e => set('contract_term_years', +e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Expansion (MW)</label>
            <input type="number" min={0} value={form.expansion_capacity_mw} onChange={e => set('expansion_capacity_mw', +e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Building Age (yr)</label>
            <input type="number" min={0} value={form.building_age_years} onChange={e => set('building_age_years', +e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Land (acres)</label>
            <input type="number" min={0} value={form.land_acres} onChange={e => set('land_acres', +e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <label className="flex items-center gap-2 text-sm text-gray-700 self-end pb-2">
            <input type="checkbox" checked={form.land_owned} onChange={e => set('land_owned', e.target.checked)} className="rounded accent-france-blue" />
            Land Owned
          </label>
          <div className="flex items-end">
            <button onClick={analyze} disabled={loading} className="w-full inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-france-blue hover:bg-france-blue-dark text-white font-medium text-sm disabled:opacity-50">
              {loading ? <Loader2 size={14} className="animate-spin" /> : null} Run Valuation
            </button>
          </div>
        </div>
      </div>

      {result && (
        <>
          {/* KPI Row */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <p className="text-xs font-medium text-gray-500">Base Value</p>
              <p className="text-lg font-bold text-gray-900">{fmtM(result.base_value)}</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <p className="text-xs font-medium text-gray-500">Fair Value</p>
              <p className="text-lg font-bold text-france-blue">{fmtM(result.adjusted_value)}</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <p className="text-xs font-medium text-gray-500">Valuation Gap</p>
              <p className={`text-lg font-bold ${statusColor}`}>{result.valuation_gap_percent > 0 ? '+' : ''}{result.valuation_gap_percent.toFixed(1)}%</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <p className="text-xs font-medium text-gray-500">Recommendation</p>
              <p className={`text-sm font-bold ${statusColor}`}>{result.recommendation}</p>
            </div>
          </div>

          {/* Waterfall chart */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-4">Valuation Waterfall</h3>
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={waterfallData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="name" tick={{ fontSize: 10 }} angle={-30} textAnchor="end" height={80} />
                <YAxis tickFormatter={v => `$${v}M`} />
                <Tooltip formatter={v => `$${v.toFixed(1)}M`} />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {waterfallData.map((d, i) => <Cell key={i} fill={d.fill} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Adjustments table */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Valuation Adjustments</h3></div>
            <table className="w-full text-sm">
              <thead><tr className="bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase"><th className="px-6 py-3">Factor</th><th className="px-6 py-3">Description</th><th className="px-6 py-3 text-right">Impact</th></tr></thead>
              <tbody className="divide-y divide-gray-100">
                {result.adjustments.map((a, i) => (
                  <tr key={i}>
                    <td className="px-6 py-3 font-medium">{a.factor}</td>
                    <td className="px-6 py-3 text-gray-500">{a.description}</td>
                    <td className={`px-6 py-3 text-right font-medium ${a.impact >= 0 ? 'text-green-600' : 'text-red-600'}`}>{a.impact >= 0 ? '+' : ''}{fmtM(a.impact)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Flags */}
          {result.flags.length > 0 && (
            <div className="space-y-2">
              {result.flags.map((f, i) => {
                const cls = f.type === 'warning' ? 'border-amber-400 bg-amber-50' : f.type === 'opportunity' ? 'border-green-400 bg-green-50' : 'border-red-400 bg-red-50'
                return <div key={i} className={`rounded-xl border-l-4 ${cls} p-4`}><strong>{f.title}</strong><p className="text-sm text-gray-600 mt-1">{f.description}</p></div>
              })}
            </div>
          )}
        </>
      )}
    </div>
  )
}
