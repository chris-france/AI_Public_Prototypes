import AppCard from './AppCard'

export default function AppGrid({ apps, startApp, stopApp, actionInProgress }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      {apps.map((app) => (
        <AppCard
          key={app.id}
          app={app}
          startApp={startApp}
          stopApp={stopApp}
          actionInProgress={actionInProgress}
        />
      ))}
    </div>
  )
}
