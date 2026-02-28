import { useState, useEffect, useCallback, useRef } from 'react'

const POLL_INTERVAL = 3000

export default function useApps() {
  const [apps, setApps] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionInProgress, setActionInProgress] = useState(null)
  const intervalRef = useRef(null)

  const fetchApps = useCallback(async () => {
    try {
      const res = await fetch('/api/apps')
      if (res.ok) {
        setApps(await res.json())
      }
    } catch {
      // Backend not ready yet — ignore
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchApps()
    intervalRef.current = setInterval(fetchApps, POLL_INTERVAL)
    return () => clearInterval(intervalRef.current)
  }, [fetchApps])

  const startApp = useCallback(async (id) => {
    setActionInProgress(id)
    try {
      await fetch(`/api/apps/${id}/start`, { method: 'POST' })
      await fetchApps()
    } finally {
      setActionInProgress(null)
    }
  }, [fetchApps])

  const stopApp = useCallback(async (id) => {
    setActionInProgress(id)
    try {
      await fetch(`/api/apps/${id}/stop`, { method: 'POST' })
      await fetchApps()
    } finally {
      setActionInProgress(null)
    }
  }, [fetchApps])

  const startAll = useCallback(async () => {
    setActionInProgress('all')
    try {
      await fetch('/api/apps/start-all', { method: 'POST' })
      await fetchApps()
    } finally {
      setActionInProgress(null)
    }
  }, [fetchApps])

  const stopAll = useCallback(async () => {
    setActionInProgress('all')
    try {
      await fetch('/api/apps/stop-all', { method: 'POST' })
      await fetchApps()
    } finally {
      setActionInProgress(null)
    }
  }, [fetchApps])

  return { apps, loading, actionInProgress, startApp, stopApp, startAll, stopAll }
}
