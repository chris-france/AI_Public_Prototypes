import { useState, useEffect, useCallback } from 'react'

export default function useHistory() {
  const [history, setHistory] = useState([])

  const refreshHistory = useCallback(() => {
    fetch('/api/history').then(r => r.json()).then(setHistory)
  }, [])

  useEffect(() => {
    refreshHistory()
  }, [refreshHistory])

  return { history, refreshHistory }
}
