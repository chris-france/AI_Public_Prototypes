import { ShieldAlert } from 'lucide-react'

export default function TestCategories({ tests }) {
  if (!tests || tests.length === 0) return null

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 h-full">
      <div className="flex items-center gap-2 mb-3">
        <ShieldAlert size={16} className="text-france-blue" />
        <h3 className="text-sm font-semibold text-gray-900">10 Attack Categories</h3>
      </div>
      <div className="space-y-1.5">
        {tests.map((t, i) => (
          <div key={t.id} className="flex items-start gap-2">
            <span className="text-[10px] font-bold text-france-blue bg-france-blue/8 rounded px-1.5 py-0.5 mt-0.5 shrink-0">
              {i + 1}
            </span>
            <div>
              <div className="text-xs font-medium text-gray-800 leading-tight">{t.name}</div>
              <div className="text-[10px] text-gray-400 leading-tight">{t.description}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
