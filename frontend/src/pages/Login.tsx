import { useState } from 'react'
import axios from 'axios'

export default function Login({ onLogin }:{ onLogin: (token:string)=>void }){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [mode, setMode] = useState<'login'|'register'>('login')
  const [error, setError] = useState('')

  async function submit(){
    setError('')
    try{
      if(mode==='register'){
        const r = await axios.post('/api/auth/register', { email, password, display_name: email.split('@')[0] })
        onLogin(r.data.access_token)
      } else {
        const r = await axios.post('/api/auth/login', { email, password })
        onLogin(r.data.access_token)
      }
    }catch(e:any){ setError(e?.response?.data?.error || 'Failed') }
  }

  return (
    <div className="max-w-sm mx-auto mt-10 p-6 border rounded bg-white">
      <h1 className="text-xl font-semibold mb-4">{mode==='login'?'Login':'Register'}</h1>
      <div className="space-y-3">
        <input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" className="border px-3 py-2 rounded w-full" />
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" className="border px-3 py-2 rounded w-full" />
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <button onClick={submit} className="w-full px-4 py-2 rounded bg-brand text-white">{mode==='login'?'Login':'Create account'}</button>
        <button onClick={()=>setMode(mode==='login'?'register':'login')} className="w-full text-sm text-gray-600">{mode==='login'?'No account? Register':'Have an account? Login'}</button>
      </div>
    </div>
  )
}