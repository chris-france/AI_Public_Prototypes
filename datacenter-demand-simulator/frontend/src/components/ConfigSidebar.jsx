import { Settings } from 'lucide-react'

export default function ConfigSidebar({ config, form, setField }) {
  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div className="flex items-center gap-2 mb-3">
          <Settings size={16} className="text-france-blue" />
          <h3 className="font-semibold text-sm text-gray-900">Business Parameters</h3>
        </div>

        <div className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Industry</label>
            <select value={form.industry} onChange={e => setField('industry', e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue">
              {config.industries.map(i => <option key={i}>{i}</option>)}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Employees</label>
            <input type="number" min={100} step={100} value={form.employees}
              onChange={e => setField('employees', parseInt(e.target.value) || 100)}
              className="w-full rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue" />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Growth Rate: {(form.growth_rate * 100).toFixed(0)}%</label>
            <input type="range" min={0} max={50} value={form.growth_rate * 100}
              onChange={e => setField('growth_rate', parseInt(e.target.value) / 100)}
              className="w-full accent-france-blue" />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">Horizon: {form.horizon_years} years</label>
            <input type="range" min={3} max={10} value={form.horizon_years}
              onChange={e => setField('horizon_years', parseInt(e.target.value))}
              className="w-full accent-france-blue" />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-500 mb-1">AI Intensity: {(form.ai_intensity * 100).toFixed(0)}%</label>
            <input type="range" min={0} max={100} value={form.ai_intensity * 100}
              onChange={e => setField('ai_intensity', parseInt(e.target.value) / 100)}
              className="w-full accent-france-blue" />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <h3 className="font-semibold text-sm text-gray-900 mb-2">Workloads</h3>
        <div className="space-y-1">
          {config.workloads.map(w => (
            <label key={w} className="flex items-center gap-2 text-xs text-gray-700 cursor-pointer">
              <input type="checkbox" checked={form.workloads.includes(w)}
                onChange={e => {
                  const next = e.target.checked ? [...form.workloads, w] : form.workloads.filter(x => x !== w)
                  setField('workloads', next)
                }}
                className="rounded accent-france-blue" />
              {w}
            </label>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <h3 className="font-semibold text-sm text-gray-900 mb-2">Compliance</h3>
        <div className="space-y-1">
          {Object.keys(config.compliance).map(c => (
            <label key={c} className="flex items-center gap-2 text-xs text-gray-700 cursor-pointer">
              <input type="checkbox" checked={form.compliance.includes(c)}
                onChange={e => {
                  const next = e.target.checked ? [...form.compliance, c] : form.compliance.filter(x => x !== c)
                  setField('compliance', next)
                }}
                className="rounded accent-france-blue" />
              {c}
            </label>
          ))}
        </div>
      </div>
    </div>
  )
}
