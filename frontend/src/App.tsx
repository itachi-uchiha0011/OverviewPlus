import { useEffect, useState } from 'react'
import { Link, Route, Routes, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Dashboard from './pages/Dashboard'
import Habits from './pages/Habits'
import Journal from './pages/Journal'
import Categories from './pages/Categories'
import Pages from './pages/Pages'
import Posts from './pages/Posts'
import Chat from './pages/Chat'
import Settings from './pages/Settings'
import Login from './pages/Login'
import { registerServiceWorker } from './push'

function useAuth() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'))
  useEffect(() => {
    axios.defaults.headers.common['Authorization'] = token ? `Bearer ${token}` : ''
    if (token) {
      axios.get('/api/auth/csrf-token').then(r => {
        const t = (r.data && (r.data.csrf_token || r.data.token)) || r.data
        if (t) axios.defaults.headers.common['X-CSRF-Token'] = t
      }).catch(()=>{})
    } else {
      delete axios.defaults.headers.common['X-CSRF-Token']
    }
  }, [token])
  return { token, setToken }
}

export default function App() {
  const { token, setToken } = useAuth()
  const navigate = useNavigate()

  useEffect(() => { registerServiceWorker() }, [])

  function logout() {
    localStorage.removeItem('access_token')
    setToken(null)
    navigate('/login')
  }

  return (
    <div className="min-h-full">
      <header className="border-b bg-white/80 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center gap-4">
          <Link to="/" className="text-xl font-bold text-brand">Overview+</Link>
          {token && (
            <nav className="hidden md:flex gap-4 text-sm">
              <Link to="/" className="hover:text-brand">Dashboard</Link>
              <Link to="/habits" className="hover:text-brand">Habits</Link>
              <Link to="/journal" className="hover:text-brand">Journal</Link>
              <Link to="/categories" className="hover:text-brand">Categories</Link>
              <Link to="/pages" className="hover:text-brand">Pages</Link>
              <Link to="/posts" className="hover:text-brand">Posts</Link>
              <Link to="/chat" className="hover:text-brand">Chat</Link>
              <Link to="/settings" className="hover:text-brand">Settings</Link>
            </nav>
          )}
          <div className="ml-auto">
            {token ? (
              <button onClick={logout} className="text-sm px-3 py-1.5 rounded bg-brand text-white">Logout</button>
            ) : (
              <Link to="/login" className="text-sm px-3 py-1.5 rounded bg-brand text-white">Login</Link>
            )}
          </div>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-6">
        <Routes>
          <Route path="/login" element={<Login onLogin={(t)=>{localStorage.setItem('access_token', t); setToken(t); navigate('/')}} />} />
          <Route path="/" element={<Dashboard />} />
          <Route path="/habits" element={<Habits />} />
          <Route path="/journal" element={<Journal />} />
          <Route path="/categories" element={<Categories />} />
          <Route path="/pages" element={<Pages />} />
          <Route path="/posts" element={<Posts />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  )
}