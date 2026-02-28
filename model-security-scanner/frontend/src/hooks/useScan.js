import { useState, useCallback } from 'react'

export default function useScan(onComplete) {
  const [scanning, setScanning] = useState(false)
  const [progress, setProgress] = useState({ model: '', testIndex: 0, totalTests: 10, testName: '', modelIndex: 0, totalModels: 1 })
  const [scanResults, setScanResults] = useState([])

  const startScan = useCallback((models, claudeApiKey) => {
    setScanning(true)
    setScanResults([])

    const currentResults = {}

    fetch('/api/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ models, claude_api_key: claudeApiKey || null }),
    }).then(response => {
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      function read() {
        reader.read().then(({ done, value }) => {
          if (done) {
            setScanning(false)
            onComplete?.()
            return
          }

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop()

          for (const line of lines) {
            if (!line.startsWith('data: ')) continue
            try {
              const event = JSON.parse(line.slice(6))

              if (event.type === 'model_start') {
                currentResults[event.model] = { model: event.model, total_score: 0, max_score: 0, results: [] }
                setProgress({
                  model: event.model,
                  testIndex: 0,
                  totalTests: event.total_models ? 10 : 10,
                  testName: 'Starting...',
                  modelIndex: event.model_index,
                  totalModels: event.total_models,
                })
              } else if (event.type === 'test_start') {
                setProgress(prev => ({
                  ...prev,
                  testIndex: event.test_index,
                  totalTests: event.total_tests,
                  testName: event.test_name,
                }))
              } else if (event.type === 'test_result') {
                currentResults[event.model].results.push(event.result)
              } else if (event.type === 'model_done') {
                currentResults[event.model].total_score = event.total_score
                currentResults[event.model].max_score = event.max_score
                setScanResults(Object.values({ ...currentResults }))
              } else if (event.type === 'scan_complete') {
                setScanning(false)
                onComplete?.()
              }
            } catch {
              // skip malformed lines
            }
          }
          read()
        })
      }
      read()
    })
  }, [onComplete])

  return { scanning, progress, scanResults, startScan }
}
