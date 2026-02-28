import { Cpu, HardDrive, Zap, Thermometer, Wifi } from 'lucide-react'

function Card({ icon: Icon, label, value, growth }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
      <div className="flex items-center gap-2 mb-1">
        <Icon size={14} className="text-france-blue" />
        <span className="text-xs font-medium text-gray-500">{label}</span>
      </div>
      <p className="text-lg font-bold text-gray-900">{value}</p>
      {growth && <p className="text-xs text-france-cyan font-medium">+{growth}% growth</p>}
    </div>
  )
}

export default function MetricsRow({ summary }) {
  const cg = ((summary.compute_growth - 1) * 100).toFixed(0)
  const sg = ((summary.storage_growth - 1) * 100).toFixed(0)
  const pg = ((summary.power_growth - 1) * 100).toFixed(0)

  return (
    <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
      <Card icon={Cpu} label="Compute Cores" value={summary.projected_compute.toLocaleString(undefined, { maximumFractionDigits: 0 })} growth={cg} />
      <Card icon={HardDrive} label="Storage (TB)" value={summary.projected_storage.toLocaleString(undefined, { maximumFractionDigits: 0 })} growth={sg} />
      <Card icon={Zap} label="Power (MW)" value={summary.projected_power.toFixed(2)} growth={pg} />
      <Card icon={Thermometer} label="Cooling (Tons)" value={summary.projected_cooling.toLocaleString(undefined, { maximumFractionDigits: 0 })} growth={pg} />
      <Card icon={Wifi} label="Network (Gbps)" value={summary.projected_network.toFixed(1)} />
    </div>
  )
}
