import { useState, useEffect, useRef, useCallback } from 'react'

const DEFAULTS = {
  preset: 'Custom',
  gpu_type: 'RTX 4090',
  queries_per_day: 1000,
  model_vram: 16,
  electricity_rate: 0.12,
  secs_per_inference: 2.0,
  hardware_cost: null,
}

export default function useCalculator() {
  const [config, setConfig] = useState(null)
  const [form, setForm] = useState(DEFAULTS)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const debounce = useRef(null)

  // Load config on mount
  useEffect(() => {
    fetch('/api/config').then(r => r.json()).then(setConfig)
  }, [])

  // Calculate whenever form changes (debounced)
  const calculate = useCallback(() => {
    setLoading(true)
    fetch('/api/calculate', {
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
    debounce.current = setTimeout(calculate, 200)
    return () => clearTimeout(debounce.current)
  }, [form, config, calculate])

  const setField = (key, value) => {
    setForm(prev => ({ ...prev, [key]: value }))
  }

  return { config, form, setField, results, loading }
}
