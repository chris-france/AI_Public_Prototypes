import { Play, Square, ExternalLink, Loader2 } from 'lucide-react'
import StatusBadge from './StatusBadge'
import TechTag from './TechTag'

export default function AppCard({ app, startApp, stopApp, actionInProgress }) {
  const { id, name, description, tech, port, status, placeholder } = app
  const isRunning = status === 'running'
  const busy = actionInProgress === id || actionInProgress === 'all'

  return (
    <div className="rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-md transition-shadow p-5 flex flex-col gap-3">
      {/* Header row */}
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-gray-900 text-sm leading-snug">{name}</h3>
        <StatusBadge status={status} />
      </div>

      {/* Port */}
      <span className="text-xs text-gray-400 font-mono -mt-1">port {port}</span>

      {/* Description */}
      <p className="text-xs text-gray-500 leading-relaxed flex-1">{description}</p>

      {/* Tech tags */}
      <div className="flex flex-wrap gap-1">
        {tech.map((t) => (
          <TechTag key={t} label={t} />
        ))}
      </div>

      {/* Action buttons */}
      <div className="flex gap-2 pt-1">
        {isRunning ? (
          <button
            onClick={() => stopApp(id)}
            disabled={busy}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-gray-200 text-gray-600 text-xs font-medium hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {busy ? <Loader2 size={12} className="animate-spin" /> : <Square size={12} />}
            Stop
          </button>
        ) : (
          <button
            onClick={() => startApp(id)}
            disabled={busy || placeholder}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-france-blue text-white text-xs font-medium hover:bg-france-blue-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {busy ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />}
            Start
          </button>
        )}

        {isRunning ? (
          <a
            href={`http://localhost:${port}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-france-blue/20 text-france-blue text-xs font-medium hover:bg-france-blue/5 transition-colors"
          >
            <ExternalLink size={12} />
            Open
          </a>
        ) : (
          <button
            disabled
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-gray-200 text-gray-300 text-xs font-medium cursor-not-allowed"
          >
            <ExternalLink size={12} />
            Open
          </button>
        )}
      </div>
    </div>
  )
}
