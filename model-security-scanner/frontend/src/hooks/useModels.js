import { useState, useEffect } from 'react'

export default function useModels() {
  const [models, setModels] = useState({ ollama: [], claude: [] })
  const [tests, setTests] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch('/api/models').then(r => r.json()),
      fetch('/api/tests').then(r => r.json()),
    ])
      .then(([m, t]) => {
        setModels(m)
        setTests(t)
      })
      .finally(() => setLoading(false))
  }, [])

  return { models, tests, loading }
}
