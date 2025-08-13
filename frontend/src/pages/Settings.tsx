import { useEffect, useState } from 'react'
import axios from 'axios'
import { subscribePush, unsubscribePush, sendTestPush } from '../push'

export default function Settings(){
  const [me, setMe] = useState<any>(null)
  const [form, setForm] = useState<any>({})
  const [pushStatus, setPushStatus] = useState<string>('')

  useEffect(()=>{
    axios.get('/api/users/me').then(r=>{ setMe(r.data); setForm(r.data) }).catch(()=>{})
  },[])

  async function enablePush(){
    try { await subscribePush(); setPushStatus('Subscribed'); } catch { setPushStatus('Failed'); }
  }
  async function disablePush(){ await unsubscribePush(); setPushStatus('Unsubscribed') }
  async function testPush(){ await sendTestPush(); setPushStatus('Test sent') }

  function save(){ axios.put('/api/users/me', form).then(()=>alert('Saved')) }

  if(!me) return <div className="text-gray-500">Loading...</div>

  return (
    <div className="max-w-xl mx-auto p-4 border rounded bg-white space-y-3">
      <h2 className="font-semibold">Settings</h2>
      <label className="block text-sm">Display Name
        <input value={form.display_name||''} onChange={e=>setForm({...form, display_name: e.target.value})} className="border px-3 py-2 rounded w-full" />
      </label>
      <label className="block text-sm">Bio
        <textarea value={form.bio||''} onChange={e=>setForm({...form, bio: e.target.value})} rows={3} className="border px-3 py-2 rounded w-full" />
      </label>
      <label className="block text-sm">Public Profile
        <input type="checkbox" checked={!!form.is_public} onChange={e=>setForm({...form, is_public: e.target.checked})} className="ml-2" />
      </label>
      <div className="border-t pt-3">
        <div className="flex items-center gap-2">
          <button onClick={enablePush} className="px-3 py-1.5 rounded bg-brand text-white text-sm">Enable Push</button>
          <button onClick={disablePush} className="px-3 py-1.5 rounded border text-sm">Disable</button>
          <button onClick={testPush} className="px-3 py-1.5 rounded border text-sm">Test</button>
          <span className="text-xs text-gray-600">{pushStatus}</span>
        </div>
      </div>
      <div className="text-right">
        <button onClick={save} className="px-4 rounded bg-brand text-white">Save</button>
      </div>
    </div>
  )
}