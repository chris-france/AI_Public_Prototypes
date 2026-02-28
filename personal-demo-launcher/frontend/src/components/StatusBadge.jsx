const statusConfig = {
  running: {
    label: 'Running',
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    dot: 'bg-emerald-500',
    pulse: true,
  },
  stopped: {
    label: 'Stopped',
    bg: 'bg-gray-100',
    text: 'text-gray-500',
    dot: 'bg-gray-400',
    pulse: false,
  },
  coming_soon: {
    label: 'Coming Soon',
    bg: 'bg-amber-50',
    text: 'text-amber-700',
    dot: 'bg-amber-400',
    pulse: false,
  },
}

export default function StatusBadge({ status }) {
  const config = statusConfig[status] || statusConfig.stopped

  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${config.bg} ${config.text}`}>
      <span className="relative flex h-2 w-2">
        {config.pulse && (
          <span className={`animate-ping absolute inline-flex h-full w-full rounded-full ${config.dot} opacity-75`} />
        )}
        <span className={`relative inline-flex rounded-full h-2 w-2 ${config.dot}`} />
      </span>
      {config.label}
    </span>
  )
}
