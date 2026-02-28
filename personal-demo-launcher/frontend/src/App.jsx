import Header from './components/Header'
import AppGrid from './components/AppGrid'
import useApps from './hooks/useApps'

export default function App() {
  const { apps, loading, actionInProgress, startApp, stopApp, startAll, stopAll } = useApps()

  return (
    <div className="min-h-screen bg-gray-50">
      <Header
        startAll={startAll}
        stopAll={stopAll}
        actionInProgress={actionInProgress}
      />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-8 w-8 border-2 border-france-blue border-t-transparent" />
          </div>
        ) : (
          <AppGrid
            apps={apps}
            startApp={startApp}
            stopApp={stopApp}
            actionInProgress={actionInProgress}
          />
        )}
      </main>
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
        <p className="text-xs text-gray-400 text-center">
          Press Ctrl+C in terminal to stop launcher and all demos
        </p>
      </footer>
    </div>
  )
}
