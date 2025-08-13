import { useEffect, useRef, useState } from 'react'
import { io, Socket } from 'socket.io-client'

export default function Chat(){
  const [channelId, setChannelId] = useState<number>(1)
  const [messages, setMessages] = useState<{id:number; user_id:number; content:string}[]>([])
  const [text, setText] = useState('')
  const socketRef = useRef<Socket | null>(null)

  useEffect(()=>{
    const token = localStorage.getItem('access_token')
    const s = io('/', { extraHeaders: token? { Authorization: `Bearer ${token}` } : {} })
    socketRef.current = s
    s.on('connect', ()=>{
      s.emit('join_channel', { channel_id: channelId })
    })
    s.on('message', (msg)=>{
      setMessages(prev => [...prev, msg])
    })
    return ()=>{ s.disconnect() }
  },[channelId])

  function send(){
    if(!text.trim()) return
    socketRef.current?.emit('message', { channel_id: channelId, content: text })
    setText('')
  }

  return (
    <div className="p-4 border rounded bg-white">
      <h2 className="font-semibold mb-3">Chat (Channel {channelId})</h2>
      <div className="space-y-2">
        <input value={channelId} onChange={e=>setChannelId(Number(e.target.value))} className="border px-3 py-2 rounded w-full" />
        <div className="h-64 overflow-auto border rounded p-2 text-sm">
          {messages.map(m => <div key={m.id}><span className="text-gray-500">{m.user_id}:</span> {m.content}</div>)}
        </div>
        <div className="flex gap-2">
          <input value={text} onChange={e=>setText(e.target.value)} className="border px-3 py-2 rounded w-full" placeholder="Message" />
          <button onClick={send} className="px-4 rounded bg-brand text-white">Send</button>
        </div>
      </div>
    </div>
  )
}