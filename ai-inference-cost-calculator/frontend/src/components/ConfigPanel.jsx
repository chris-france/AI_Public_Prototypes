import { Settings } from 'lucide-react'

export default function ConfigPanel({ config, form, setField }) {
  const presetEntries = Object.entries(config.presets)
  const selectedGpu = config.gpus[form.gpu_type]

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center gap-2 mb-4">
        <Settings size={18} className="text-france-blue" />
        <h2 className="font-semibold text-gray-900">Configuration</h2>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {/* Preset */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Preset</label>
          <select
            value={form.preset}
            onChange={e => {
              const p = e.target.value
              const val = config.presets[p]
              setField('preset', p)
              if (val !== null) setField('queries_per_day', val)
            }}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue"
          >
            {presetEntries.map(([name]) => (
              <option key={name} value={name}>{name}</option>
            ))}
          </select>
        </div>

        {/* GPU Type */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">GPU Type</label>
          <select
            value={form.gpu_type}
            onChange={e => setField('gpu_type', e.target.value)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue"
          >
            {config.gpu_types.map(g => (
              <option key={g} value={g}>{g}</option>
            ))}
          </select>
        </div>

        {/* Queries per day */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Queries / Day</label>
          <input
            type="number"
            min={1}
            value={form.queries_per_day}
            onChange={e => setField('queries_per_day', parseInt(e.target.value) || 1)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue"
          />
        </div>

        {/* Model VRAM */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Model VRAM (GB)</label>
          <input
            type="number"
            min={1}
            value={form.model_vram}
            onChange={e => setField('model_vram', parseInt(e.target.value) || 1)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue"
          />
        </div>

        {/* Electricity rate */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Electricity ($/kWh)</label>
          <input
            type="number"
            min={0}
            step={0.01}
            value={form.electricity_rate}
            onChange={e => setField('electricity_rate', parseFloat(e.target.value) || 0)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue"
          />
        </div>

        {/* Seconds per inference */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Secs / Inference</label>
          <input
            type="number"
            min={0.1}
            step={0.1}
            value={form.secs_per_inference}
            onChange={e => setField('secs_per_inference', parseFloat(e.target.value) || 0.1)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue"
          />
        </div>
      </div>

      {/* Hardware cost override (only for Custom preset) */}
      {form.preset === 'Custom' && (
        <div className="mt-4 max-w-xs">
          <label className="block text-xs font-medium text-gray-500 mb-1">Hardware Cost ($)</label>
          <input
            type="number"
            min={0}
            step={100}
            value={form.hardware_cost ?? selectedGpu?.cost ?? 0}
            onChange={e => setField('hardware_cost', parseInt(e.target.value) || 0)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-france-blue/30 focus:border-france-blue"
          />
        </div>
      )}
    </div>
  )
}
