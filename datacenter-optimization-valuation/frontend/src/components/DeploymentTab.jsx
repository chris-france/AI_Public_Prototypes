import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'
import { Loader2, Bot } from 'lucide-react'
import useOllamaStream from '../hooks/useOllamaStream'

const COLORS = ['#1472CF', '#10B981', '#F59E0B']
const fmtM = v => `$${(v / 1e6).toFixed(1)}M`

export default function DeploymentTab() {
  const [config, setConfig] = useState(null)
  const [form, setForm] = useState({ total_power_mw: 20, rack_count: 500, timeline_urgency: 'standard', budget_constraint: 200, region: 'Northern Virginia (NOVA)', redundancy_level: 'N+1', cooling_type: 'air' })
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const { text: aiText, streaming, start: startAI } = useOllamaStream()

  useEffect(() => { fetch('/api/deployment/config').then(r => r.json()).then(setConfig) }, [])

  const analyze = () => {
    setLoading(true)
    fetch('/api/deployment/analyze', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) })
      .then(r => r.json()).then(setResults).finally(() => setLoading(false))
  }

  const set = (k, v) => setForm(p => ({ ...p, [k]: v }))

  if (!config) return <div className="flex justify-center py-10"><div className="animate-spin rounded-full h-8 w-8 border-2 border-france-blue border-t-transparent" /></div>

  const approaches = results ? Object.values(results) : []
  const chartData = approaches.map(a => ({ name: a.name, 'CapEx ($M)': +(a.capex / 1e6).toFixed(1), 'Timeline (mo)': a.timeline_months, 'ROI (%)': a.roi_percent }))

  return (
    <div className="space-y-6">
      {/* Form */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="font-semibold text-gray-900 mb-4">Deployment Requirements</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Power (MW)</label>
            <input type="number" min={1} step={1} value={form.total_power_mw} onChange={e => set('total_power_mw', +e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Rack Count</label>
            <input type="number" min={10} step={50} value={form.rack_count} onChange={e => set('rack_count', +e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Region</label>
            <select value={form.region} onChange={e => set('region', e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm">
              {config.regions.map(r => <option key={r}>{r}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Timeline</label>
            <select value={form.timeline_urgency} onChange={e => set('timeline_urgency', e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm">
              <option value="standard">Standard (24-30 mo)</option>
              <option value="accelerated">Accelerated (15-20 mo)</option>
              <option value="critical">Critical (&lt;12 mo)</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Budget ($M)</label>
            <input type="number" min={10} step={10} value={form.budget_constraint} onChange={e => set('budget_constraint', +e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Redundancy</label>
            <select value={form.redundancy_level} onChange={e => set('redundancy_level', e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm">
              {Object.keys(config.redundancy).map(k => <option key={k} value={k}>{k}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Cooling</label>
            <select value={form.cooling_type} onChange={e => set('cooling_type', e.target.value)} className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm">
              {Object.entries(config.cooling).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
            </select>
          </div>
          <div className="flex items-end">
            <button onClick={analyze} disabled={loading} className="w-full inline-flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-france-blue hover:bg-france-blue-dark text-white font-medium text-sm transition-colors disabled:opacity-50">
              {loading ? <Loader2 size={14} className="animate-spin" /> : null}
              Analyze
            </button>
          </div>
        </div>
      </div>

      {results && (
        <>
          {/* KPI cards */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {approaches.map((a, i) => (
              <div key={i} className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
                <h4 className="text-xs font-medium text-gray-500">{a.name}</h4>
                <p className="text-lg font-bold text-gray-900">{fmtM(a.total_10yr_cost)}</p>
                <p className="text-xs text-gray-400">{a.timeline_months}mo | ROI {a.roi_percent}%</p>
                <div className="mt-2 flex gap-1">
                  {a.meets_budget && <span className="text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded-full">Budget</span>}
                  {a.meets_timeline && <span className="text-xs bg-green-100 text-green-700 px-1.5 py-0.5 rounded-full">Timeline</span>}
                  {!a.meets_budget && <span className="text-xs bg-red-100 text-red-700 px-1.5 py-0.5 rounded-full">Over Budget</span>}
                </div>
              </div>
            ))}
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-semibold text-gray-900 mb-4">CapEx Comparison</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis tickFormatter={v => `$${v}M`} />
                  <Tooltip />
                  <Bar dataKey="CapEx ($M)" radius={[6, 6, 0, 0]}>
                    {chartData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-semibold text-gray-900 mb-4">ROI Comparison</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis tickFormatter={v => `${v}%`} />
                  <Tooltip />
                  <Bar dataKey="ROI (%)" radius={[6, 6, 0, 0]}>
                    {chartData.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Risk cards */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {approaches.map((a, i) => {
              const level = a.risk_score < 30 ? 'Low' : a.risk_score < 60 ? 'Medium' : 'High'
              const cls = a.risk_score < 30 ? 'border-green-400 bg-green-50' : a.risk_score < 60 ? 'border-amber-400 bg-amber-50' : 'border-red-400 bg-red-50'
              return (
                <div key={i} className={`rounded-xl border-l-4 ${cls} p-4`}>
                  <h4 className="font-semibold text-gray-900">{a.name} — {level} Risk ({a.risk_score}/100)</h4>
                  <ul className="mt-2 text-sm text-gray-600 list-disc list-inside">
                    {a.risk_factors.map((rf, j) => <li key={j}>{rf}</li>)}
                  </ul>
                </div>
              )
            })}
          </div>

          {/* AI recommendation */}
          {config.ollama_available && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center gap-3 mb-4">
                <Bot size={20} className="text-france-blue" />
                <h3 className="font-semibold text-gray-900">AI Strategy Recommendation</h3>
                <button onClick={() => startAI('/api/deployment/ai-recommendation', { prompt: `Analyze deployment: ${JSON.stringify(results)}`, model: config.ollama_models?.[0] || 'llama3.2' })} disabled={streaming}
                  className="ml-auto inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-france-blue text-white text-xs font-medium">
                  {streaming ? <Loader2 size={12} className="animate-spin" /> : <Bot size={12} />}
                  {streaming ? 'Generating...' : 'Generate'}
                </button>
              </div>
              {aiText && <div className="prose prose-sm max-w-none text-gray-700 whitespace-pre-wrap">{aiText}{streaming && <span className="inline-block w-2 h-4 bg-france-blue animate-pulse ml-0.5" />}</div>}
            </div>
          )}
        </>
      )}
    </div>
  )
}
