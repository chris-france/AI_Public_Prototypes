import { useState, useEffect, useRef, useCallback } from 'react'

const DEFAULTS = {
  industry: 'Technology',
  employees: 5000,
  growth_rate: 0.15,
  workloads: ['General Compute', 'Database Operations', 'AI/ML Inference'],
  compliance: ['SOC 2 Type II'],
  horizon_years: 5,
  ai_intensity: 0.5,
}

export default function useSimulation() {
  const [config, setConfig] = useState(null)
  const [form, setForm] = useState(DEFAULTS)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const debounce = useRef(null)

  useEffect(() => {
    fetch('/api/config').then(r => r.json()).then(setConfig)
  }, [])

  const simulate = useCallback(() => {
    setLoading(true)
    fetch('/api/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
      .then(r => r.json())
      .then(setResults)
      .finally(() => setLoading(false))
  }, [form])

  useEffect(() => {
    if (!config) return
    clearTimeout(debounce.current)
    debounce.current = setTimeout(simulate, 300)
    return () => clearTimeout(debounce.current)
  }, [form, config, simulate])

  const setField = (key, value) => {
    setForm(prev => ({ ...prev, [key]: value }))
  }

  return { config, form, setField, results, loading }
}
