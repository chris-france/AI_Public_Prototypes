import { useState } from 'react'
import Header from './components/Header'
import DeploymentTab from './components/DeploymentTab'
import ValuationTab from './components/ValuationTab'
import BenchmarksTab from './components/BenchmarksTab'
import FeedbackBar from './components/FeedbackBar'

const TABS = [
  { id: 'deployment', label: 'Deployment Analysis' },
  { id: 'valuation', label: 'M&A Valuation' },
  { id: 'benchmarks', label: 'Market Benchmarks' },
]

export default function App() {
  const [tab, setTab] = useState('deployment')

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Tabs */}
        <div className="flex gap-1 bg-gray-100 rounded-lg p-1">
          {TABS.map(t => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`flex-1 px-4 py-2.5 rounded-md text-sm font-medium transition-colors ${
                tab === t.id
                  ? 'bg-white text-france-blue shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === 'deployment' && <DeploymentTab />}
        {tab === 'valuation' && <ValuationTab />}
        {tab === 'benchmarks' && <BenchmarksTab />}
      </main>
      <FeedbackBar appName="datacenter-optimization-valuation" />
    </div>
  )
}
