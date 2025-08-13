import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Journal(){
  const [html, setHtml] = useState('')
  const [items, setItems] = useState<any[]>([])

  function load(){ axios.get('/api/journal').then(r=>setItems(r.data)) }
  useEffect(()=>{ load() },[])

  function add(){
    if(!html.trim()) return
    axios.post('/api/journal', { content_html: html }).then(()=>{ setHtml(''); load() })
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">New Entry</h2>
        <textarea value={html} onChange={e=>setHtml(e.target.value)} rows={6} className="w-full border rounded p-2" placeholder="What I learned / Mistakes..." />
        <div className="mt-2 text-right">
          <button onClick={add} className="px-4 rounded bg-brand text-white">Save</button>
        </div>
      </div>
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">Entries</h2>
        <ul className="space-y-3 text-sm">
          {items.map(it => (
            <li key={it.id} className="border rounded p-2">
              <div className="text-gray-500 text-xs">{it.date}</div>
              <div dangerouslySetInnerHTML={{__html: it.content_html}} />
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}