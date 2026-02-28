import Header from './components/Header'
import ConfigPanel from './components/ConfigPanel'
import MetricsRow from './components/MetricsRow'
import CumulativeCostChart from './components/CumulativeCostChart'
import CostPerInferenceChart from './components/CostPerInferenceChart'
import ComparisonTable from './components/ComparisonTable'
import HardwareTable from './components/HardwareTable'
import useCalculator from './hooks/useCalculator'

export default function App() {
  const { config, form, setField, results, loading } = useCalculator()

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {config ? (
          <>
            <ConfigPanel config={config} form={form} setField={setField} />
            {results && (
              <>
                <MetricsRow results={results} gpuType={form.gpu_type} />
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <CumulativeCostChart data={results.cumulative} gpuType={form.gpu_type} />
                  <CostPerInferenceChart results={results} gpuType={form.gpu_type} />
                </div>
                <ComparisonTable results={results} gpuType={form.gpu_type} />
                <HardwareTable gpus={config.gpus} selected={form.gpu_type} />
              </>
            )}
          </>
        ) : (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-8 w-8 border-2 border-france-blue border-t-transparent" />
          </div>
        )}
      </main>
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
        <p className="text-xs text-gray-400 text-center">
          Compare TCO for local GPU builds vs cloud providers over 36 months
        </p>
      </footer>
    </div>
  )
}
