import { useState } from 'react'
import { MessageSquarePlus, Send, X } from 'lucide-react'

export default function FeedbackBar({ appName }) {
  const [open, setOpen] = useState(false)
  const [comment, setComment] = useState('')
  const [status, setStatus] = useState(null) // 'saving' | 'saved' | 'error'

  const submit = async () => {
    if (!comment.trim()) return
    setStatus('saving')
    try {
      const res = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ page: window.location.pathname, comment }),
      })
      if (!res.ok) throw new Error()
      setStatus('saved')
      setComment('')
      setTimeout(() => { setOpen(false); setStatus(null) }, 1200)
    } catch {
      setStatus('error')
      setTimeout(() => setStatus(null), 2000)
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit() }
  }

  if (!open) {
    return (
      <button
        onClick={() => setOpen(true)}
        className="fixed bottom-5 right-5 z-50 flex items-center gap-2 bg-amber-500 hover:bg-amber-600 text-white pl-3 pr-4 py-2.5 rounded-full shadow-lg transition-colors text-sm font-medium"
      >
        <MessageSquarePlus size={18} />
        Feedback
      </button>
    )
  }

  return (
    <div className="fixed bottom-5 right-5 z-50 w-80 bg-white border border-amber-300 rounded-xl shadow-xl">
      <div className="flex items-center justify-between px-4 py-2.5 bg-amber-50 rounded-t-xl border-b border-amber-200">
        <span className="text-sm font-semibold text-amber-800">Send Feedback</span>
        <button onClick={() => { setOpen(false); setStatus(null) }} className="text-amber-600 hover:text-amber-800">
          <X size={16} />
        </button>
      </div>
      <div className="p-3">
        <textarea
          autoFocus
          rows={3}
          value={comment}
          onChange={e => setComment(e.target.value)}
          onKeyDown={handleKey}
          placeholder="Bug, idea, or comment..."
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-400 resize-none"
        />
        <div className="flex items-center justify-between mt-2">
          <span className="text-xs text-gray-400">
            {status === 'saved' && 'Saved!'}
            {status === 'error' && 'Failed — try again'}
            {status === 'saving' && 'Saving...'}
            {!status && 'Enter to send'}
          </span>
          <button
            onClick={submit}
            disabled={!comment.trim() || status === 'saving'}
            className="flex items-center gap-1.5 bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-white px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
          >
            <Send size={14} /> Send
          </button>
        </div>
      </div>
    </div>
  )
}
