import { DollarSign, TrendingDown, Clock, CheckCircle, AlertTriangle, XCircle } from 'lucide-react'

function MetricCard({ label, value, icon: Icon, accent }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <div className="flex items-center gap-2 mb-1">
        <Icon size={14} className={accent || 'text-gray-400'} />
        <span className="text-xs font-medium text-gray-500">{label}</span>
      </div>
      <p className="text-lg font-bold text-gray-900">{value}</p>
    </div>
  )
}

const fmt = v => v.toLocaleString('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 })

export default function MetricsRow({ results, gpuType }) {
  const { local, cloud, breakeven, gpus_needed } = results
  const providers = Object.keys(cloud)

  const breakEvenText = breakeven.month !== null
    ? `Month ${breakeven.month} vs ${breakeven.vs_provider}`
    : 'Does not break even'
  const breakEvenIcon = breakeven.month !== null && breakeven.month <= 36
    ? CheckCircle
    : breakeven.month !== null
      ? AlertTriangle
      : XCircle
  const breakEvenAccent = breakeven.month !== null && breakeven.month <= 36
    ? 'text-green-500'
    : breakeven.month !== null
      ? 'text-amber-500'
      : 'text-red-500'

  return (
    <div>
      {gpus_needed > 1 && (
        <div className="mb-4 px-4 py-2 bg-france-blue/10 text-france-blue text-sm rounded-lg font-medium">
          Model requires {gpus_needed}x {gpuType} GPUs
        </div>
      )}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <MetricCard label={`Local (monthly)`} value={fmt(local.monthly)} icon={DollarSign} accent="text-france-blue" />
        <MetricCard label="Local (3-yr TCO)" value={fmt(local.three_year_tco)} icon={DollarSign} accent="text-france-blue" />
        {providers.map(p => (
          <MetricCard key={p} label={`${p} (monthly)`} value={fmt(cloud[p].monthly)} icon={DollarSign} />
        ))}
      </div>
      <div className="mt-4">
        <MetricCard label="Break-Even Point" value={breakEvenText} icon={breakEvenIcon} accent={breakEvenAccent} />
      </div>
    </div>
  )
}
