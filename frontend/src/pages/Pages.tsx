import { useEffect, useState } from 'react'
import axios from 'axios'

type Page = { id:number; title:string; category_id:number|null }

enum LoadState { Idle, Loading, Done }

export default function Pages(){
  const [pages, setPages] = useState<Page[]>([])
  const [title, setTitle] = useState('')
  const [categoryId, setCategoryId] = useState<number | ''>('')
  const [state, setState] = useState<LoadState>(LoadState.Idle)

  function load(){ setState(LoadState.Loading); axios.get('/api/pages').then(r=>{setPages(r.data); setState(LoadState.Done)}) }
  useEffect(()=>{ load() },[])

  function add(){
    if(!title.trim()) return
    axios.post('/api/pages', { title, category_id: categoryId || null }).then(()=>{ setTitle(''); setCategoryId(''); load() })
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">Add Page</h2>
        <div className="space-y-2">
          <input value={title} onChange={e=>setTitle(e.target.value)} placeholder="Page title" className="border px-3 py-2 rounded w-full" />
          <input value={categoryId} onChange={e=>setCategoryId(e.target.value? Number(e.target.value): '')} placeholder="Category ID (optional)" className="border px-3 py-2 rounded w-full" />
          <button onClick={add} className="px-4 rounded bg-brand text-white">Add</button>
        </div>
      </div>
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">Your Pages</h2>
        {state===LoadState.Loading? <div className="text-gray-500">Loading...</div> : (
          <ul className="space-y-2 text-sm">
            {pages.map(p => <li key={p.id}>{p.title} <span className="text-gray-400">(cat: {p.category_id??'none'})</span></li>)}
          </ul>
        )}
      </div>
    </div>
  )
}