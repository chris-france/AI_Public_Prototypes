import { Calculator } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-france-blue to-france-cyan sticky top-0 z-50 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-white/20 backdrop-blur flex items-center justify-center">
            <Calculator size={20} className="text-white" />
          </div>
          <div className="text-white">
            <span className="font-bold text-lg tracking-tight">AI Inference Cost Calculator</span>
            <span className="hidden sm:inline text-white/70 text-xs ml-2">port 8601</span>
          </div>
        </div>
      </div>
      <div className="bg-black/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-8">
          <span className="text-white/80 text-xs font-medium">Chris France</span>
          <span className="text-white/60 text-xs">AI & Infrastructure Prototypes</span>
        </div>
      </div>
    </header>
  )
}
