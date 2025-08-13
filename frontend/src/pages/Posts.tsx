import { useEffect, useState } from 'react'
import axios from 'axios'

type Post = { id:number; title:string; content_html:string; is_public:boolean; likes:number; comments:number }

export default function Posts(){
  const [items, setItems] = useState<Post[]>([])
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [isPublic, setIsPublic] = useState(false)

  function load(){ axios.get('/api/posts').then(r=>setItems(r.data)) }
  useEffect(()=>{ load() },[])

  function add(){
    if(!title.trim()) return
    axios.post('/api/posts', { title, content_html: content, is_public: isPublic }).then(()=>{ setTitle(''); setContent(''); setIsPublic(false); load() })
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">New Post</h2>
        <div className="space-y-2">
          <input value={title} onChange={e=>setTitle(e.target.value)} placeholder="Title" className="border px-3 py-2 rounded w-full" />
          <textarea value={content} onChange={e=>setContent(e.target.value)} rows={6} className="w-full border rounded p-2" placeholder="Content HTML" />
          <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={isPublic} onChange={e=>setIsPublic(e.target.checked)} /> Publish</label>
          <button onClick={add} className="px-4 rounded bg-brand text-white">Save</button>
        </div>
      </div>
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">Your Posts</h2>
        <ul className="space-y-2 text-sm">
          {items.map(it => (
            <li key={it.id} className="border rounded p-2">
              <div className="font-medium">{it.title}</div>
              <div className="text-xs text-gray-500">{it.is_public? 'Public':'Private'} · {it.likes} likes · {it.comments} comments</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}