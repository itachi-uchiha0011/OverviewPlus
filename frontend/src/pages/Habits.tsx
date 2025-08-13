import { useEffect, useState } from 'react'
import axios from 'axios'

type Habit = { id:number; name:string; frequency:string }

export default function Habits(){
  const [habits, setHabits] = useState<Habit[]>([])
  const [name, setName] = useState('')

  function load(){ axios.get('/api/habits').then(r=>setHabits(r.data)) }
  useEffect(()=>{ load() },[])

  function add(){
    if(!name.trim()) return
    axios.post('/api/habits', { name }).then(()=>{ setName(''); load() })
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">Add Habit</h2>
        <div className="flex gap-2">
          <input value={name} onChange={e=>setName(e.target.value)} placeholder="Habit name" className="border px-3 py-2 rounded w-full" />
          <button onClick={add} className="px-4 rounded bg-brand text-white">Add</button>
        </div>
      </div>
      <div className="p-4 border rounded bg-white">
        <h2 className="font-semibold mb-3">Your Habits</h2>
        <ul className="space-y-2">
          {habits.map(h => <li key={h.id} className="text-sm">{h.name} <span className="text-gray-400">({h.frequency})</span></li>)}
        </ul>
      </div>
    </div>
  )
}