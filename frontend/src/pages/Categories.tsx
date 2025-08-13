import { useEffect, useState } from 'react'
import axios from 'axios'

type Category = { id:number; name:string; is_public:boolean }

export default function Categories(){
  const [items, setItems] = useState<Category[]>([])
  const [name, setName] = useState('')
  const [isPublic, setIsPublic] = useState(false)

  function load(){ axios.get('/api/categories').then(r=>setItems(r.data)) }
  useEffect(()=>{ load() },[])

  function add(){
    if(!name.trim()) return
    axios.post('/api/categories', { name, is_public: isPublic }).then(()=>{ setName(''); setIsPublic(false); load() })
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">Add Category</h2>
        <div className="space-y-2">
          <input value={name} onChange={e=>setName(e.target.value)} placeholder="Category name" className="border px-3 py-2 rounded w-full" />
          <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={isPublic} onChange={e=>setIsPublic(e.target.checked)} /> Make Public</label>
          <button onClick={add} className="px-4 rounded bg-brand text-white">Add</button>
        </div>
      </div>
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">Your Categories</h2>
        <ul className="space-y-2 text-sm">
          {items.map(it => <li key={it.id}>{it.name} <span className={`ml-2 ${it.is_public? 'text-green-600':'text-gray-400'}`}>{it.is_public? 'Public':'Private'}</span></li>)}
        </ul>
      </div>
    </div>
  )
}