import { useEffect, useState } from 'react'
import axios from 'axios'
import { Bar } from 'react-chartjs-2'
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend)

type DashboardData = {
  today: string
  habits: { id: number; name: string; completed: boolean }[]
  todos: { id: number; title: string }[]
  not_todos: { id: number; title: string }[]
  journal_entries_today: number
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)

  useEffect(() => {
    axios.get('/api/dashboard').then(r => setData(r.data)).catch(()=>{})
  }, [])

  if (!data) return <div className="text-gray-500">Loading...</div>

  const completed = data.habits.filter(h=>h.completed).length
  const pending = data.habits.length - completed
  const chartData = {
    labels: ['Completed', 'Pending'],
    datasets: [
      { label: 'Habits', data: [completed, pending], backgroundColor: ['#16a34a', '#9ca3af'] }
    ]
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <section className="p-4 rounded border bg-white">
        <h2 className="font-semibold mb-3">Today's Habits</h2>
        <ul className="space-y-2">
          {data.habits.slice(0,6).map(h => (
            <li key={h.id} className="flex items-center justify-between text-sm">
              <span>{h.name}</span>
              <span className={h.completed? 'text-green-600':'text-gray-400'}>{h.completed? 'Done':'Pending'}</span>
            </li>
          ))}
        </ul>
      </section>
      <section className="p-4 rounded border bg-white">
        <h2 className="font-semibold mb-3">Top 4 To-Do</h2>
        <ul className="list-disc ml-5 text-sm">
          {data.todos.map(t => <li key={t.id}>{t.title}</li>)}
        </ul>
      </section>
      <section className="p-4 rounded border bg-white">
        <h2 className="font-semibold mb-3">Top 4 Not To-Do</h2>
        <ul className="list-disc ml-5 text-sm">
          {data.not_todos.map(t => <li key={t.id}>{t.title}</li>)}
        </ul>
      </section>
      <section className="p-4 rounded border bg-white lg:col-span-2">
        <h2 className="font-semibold mb-3">Journal Today</h2>
        <p className="text-sm text-gray-600">Entries: {data.journal_entries_today}</p>
      </section>
      <section className="p-4 rounded border bg-white">
        <h2 className="font-semibold mb-3">Habits Chart</h2>
        <Bar data={chartData} options={{ responsive: true, plugins: { legend: { display: false }}}} />
      </section>
    </div>
  )
}