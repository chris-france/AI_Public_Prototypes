import { useState } from 'react'
import { Shield, Target } from 'lucide-react'
import Header from './components/Header'
import ScanConfig from './components/ScanConfig'
import ScanProgress from './components/ScanProgress'
import SummaryStats from './components/SummaryStats'
import ResultsTable from './components/ResultsTable'
import DetailedResults from './components/DetailedResults'
import ComparisonChart from './components/ComparisonChart'
import HistoryTable from './components/HistoryTable'
import TestCategories from './components/TestCategories'
import useModels from './hooks/useModels'
import useScan from './hooks/useScan'
import useHistory from './hooks/useHistory'
import FeedbackBar from './components/FeedbackBar'

export default function App() {
  const { models, tests, loading: modelsLoading } = useModels()
  const { history, refreshHistory } = useHistory()
  const [selectedModels, setSelectedModels] = useState([])
  const [claudeApiKey, setClaudeApiKey] = useState('')

  const { scanning, progress, scanResults, startScan } = useScan(() => refreshHistory())

  const handleScan = () => {
    startScan(selectedModels, claudeApiKey)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Config + Tests side by side */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <ScanConfig
              models={models}
              loading={modelsLoading}
              selectedModels={selectedModels}
              setSelectedModels={setSelectedModels}
              claudeApiKey={claudeApiKey}
              setClaudeApiKey={setClaudeApiKey}
              onScan={handleScan}
              scanning={scanning}
            />
          </div>
          <div>
            <TestCategories tests={tests} />
          </div>
        </div>

        {scanning && <ScanProgress progress={progress} />}

        {scanResults.length > 0 && (
          <>
            <div className="flex items-center gap-2 pt-2">
              <Shield size={20} className="text-france-blue" />
              <h2 className="text-lg font-bold text-gray-900">Scan Results</h2>
            </div>
            <ResultsTable scanResults={scanResults} />
            <DetailedResults scanResults={scanResults} />
          </>
        )}

        {(scanResults.length > 0 || history.length > 0) && (
          <>
            <div className="border-t border-gray-200 pt-6 mt-2">
              <div className="flex items-center gap-2 mb-6">
                <Target size={20} className="text-france-blue" />
                <h2 className="text-lg font-bold text-gray-900">Model Comparison</h2>
              </div>
              <SummaryStats scanResults={scanResults} history={history} />
              <div className="mt-6"><ComparisonChart scanResults={scanResults} history={history} /></div>
            </div>
            <HistoryTable history={history} />
          </>
        )}
      </main>
      <FeedbackBar appName="model-security-scanner" />
    </div>
  )
}
