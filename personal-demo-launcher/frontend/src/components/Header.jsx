import { Zap, Play, Square, Loader2 } from 'lucide-react'

export default function Header({ startAll, stopAll, actionInProgress }) {
  const busy = actionInProgress === 'all'

  return (
    <header className="bg-gradient-to-r from-france-blue to-france-cyan sticky top-0 z-50 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-white/20 backdrop-blur flex items-center justify-center">
            <Zap size={20} className="text-white" />
          </div>
          <div className="text-white">
            <span className="font-bold text-lg tracking-tight">Personal Demos</span>
            <span className="hidden sm:inline text-white/70 text-xs ml-2">port 8501</span>
          </div>
        </div>

        {/* Global controls */}
        <div className="flex items-center gap-2">
          <button
            onClick={startAll}
            disabled={busy}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/20 hover:bg-white/30 text-white text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {busy ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
            Start All
          </button>
          <button
            onClick={stopAll}
            disabled={busy}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white/20 hover:bg-white/30 text-white text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {busy ? <Loader2 size={14} className="animate-spin" /> : <Square size={14} />}
            Stop All
          </button>
        </div>
      </div>

      {/* Sub-brand bar */}
      <div className="bg-black/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-8">
          <span className="text-white/80 text-xs font-medium">Chris France</span>
          <span className="text-white/60 text-xs">AI & Infrastructure Prototypes</span>
        </div>
      </div>
    </header>
  )
}
