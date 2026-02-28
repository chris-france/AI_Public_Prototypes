import { Loader2 } from 'lucide-react'

export default function ScanProgress({ progress }) {
  const { model, testIndex, totalTests, testName, modelIndex, totalModels } = progress

  const pct = totalTests > 0 ? ((testIndex + 1) / totalTests) * 100 : 0

  return (
    <div className="bg-gradient-to-r from-france-blue/5 to-france-cyan/5 rounded-xl border border-france-blue/20 p-6">
      <div className="flex items-center gap-3 mb-3">
        <Loader2 size={20} className="animate-spin text-france-blue" />
        <div>
          <h3 className="font-semibold text-gray-900">
            Scanning: <span className="text-france-blue">{model}</span>
          </h3>
          <p className="text-xs text-gray-500">
            Model {modelIndex + 1} of {totalModels} &middot; Test {testIndex + 1}/{totalTests}: {testName}
          </p>
        </div>
      </div>
      <div className="w-full bg-white/60 rounded-full h-3 shadow-inner">
        <div
          className="bg-gradient-to-r from-france-blue to-france-cyan h-3 rounded-full transition-all duration-300 shadow-sm"
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-right text-xs text-gray-400 mt-1">{pct.toFixed(0)}%</p>
    </div>
  )
}
