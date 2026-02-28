import { useState, useCallback } from 'react'

export default function useOllamaStream() {
  const [text, setText] = useState('')
  const [streaming, setStreaming] = useState(false)

  const start = useCallback((url, body) => {
    setText('')
    setStreaming(true)

    fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).then(response => {
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      function read() {
        reader.read().then(({ done, value }) => {
          if (done) { setStreaming(false); return }
          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop()
          for (const line of lines) {
            if (!line.startsWith('data: ')) continue
            try {
              const event = JSON.parse(line.slice(6))
              if (event.token) setText(prev => prev + event.token)
              if (event.done) { setStreaming(false); return }
            } catch {}
          }
          read()
        })
      }
      read()
    }).catch(() => {
      setStreaming(false)
      setText(prev => prev + '\n\n[Connection error]')
    })
  }, [])

  return { text, streaming, start }
}
