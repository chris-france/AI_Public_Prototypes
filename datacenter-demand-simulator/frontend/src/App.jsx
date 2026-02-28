import { useState } from 'react'
import Header from './components/Header'
import ConfigSidebar from './components/ConfigSidebar'
import MetricsRow from './components/MetricsRow'
import CapacityCharts from './components/CapacityCharts'
import ScenarioComparison from './components/ScenarioComparison'
import DecisionTimeline from './components/DecisionTimeline'
import AIAnalysisPanel from './components/AIAnalysisPanel'
import useSimulation from './hooks/useSimulation'

const TABS = [
  { id: 'capacity', label: 'Capacity Projections' },
  { id: 'scenarios', label: 'Risk Scenarios' },
  { id: 'decisions', label: 'Decision Timeline' },
  { id: 'ai', label: 'AI Analysis' },
]

export default function App() {
  const [tab, setTab] = useState('capacity')
  const { config, form, setField, results, loading } = useSimulation()

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex gap-8">
          {/* Sidebar */}
          <div className="w-72 shrink-0">
            {config && <ConfigSidebar config={config} form={form} setField={setField} />}
          </div>

          {/* Main content */}
          <div className="flex-1 min-w-0 space-y-6">
            {results && (
              <>
                <MetricsRow summary={results.summary} />

                {/* Tabs */}
                <div className="flex gap-1 bg-gray-100 rounded-lg p-1">
                  {TABS.map(t => (
                    <button
                      key={t.id}
                      onClick={() => setTab(t.id)}
                      className={`flex-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        tab === t.id
                          ? 'bg-white text-france-blue shadow-sm'
                          : 'text-gray-600 hover:text-gray-900'
                      }`}
                    >
                      {t.label}
                    </button>
                  ))}
                </div>

                {tab === 'capacity' && <CapacityCharts scenarios={results.scenarios} />}
                {tab === 'scenarios' && <ScenarioComparison scenarios={results.scenarios} comparison={results.comparison} />}
                {tab === 'decisions' && <DecisionTimeline points={results.decision_points} />}
                {tab === 'ai' && <AIAnalysisPanel summary={results.summary} ollamaAvailable={config?.ollama_available} ollamaModels={config?.ollama_models} />}
              </>
            )}
            {!results && (
              <div className="flex items-center justify-center py-20">
                <div className="animate-spin rounded-full h-8 w-8 border-2 border-france-blue border-t-transparent" />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
