export async function registerServiceWorker() {
  if (!('serviceWorker' in navigator)) return null
  return navigator.serviceWorker.register('/service-worker.js')
}

async function urlBase64ToUint8Array(base64String: string) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4)
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/')
  const rawData = atob(base64)
  const outputArray = new Uint8Array(rawData.length)
  for (let i = 0; i < rawData.length; ++i) outputArray[i] = rawData.charCodeAt(i)
  return outputArray
}

export async function subscribePush() {
  const reg = await registerServiceWorker()
  if (!reg) throw new Error('SW not supported')

  const { data } = await fetch('/api/push/public-key').then(r => r.json())
  const vapidKey = (data && (data.publicKey || data)) || (await fetch('/api/push/public-key').then(r=>r.json())).publicKey
  const sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: await urlBase64ToUint8Array(vapidKey) })
  await fetch('/api/push/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(sub) })
  return sub
}

export async function unsubscribePush() {
  const reg = await navigator.serviceWorker.getRegistration()
  const sub = await reg?.pushManager.getSubscription()
  if (sub) {
    await fetch('/api/push/subscribe', { method: 'DELETE', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ endpoint: sub.endpoint }) })
    await sub.unsubscribe()
  }
}

export async function sendTestPush() {
  await fetch('/api/push/test', { method: 'POST' })
}