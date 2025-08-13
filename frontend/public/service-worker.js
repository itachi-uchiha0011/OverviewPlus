self.addEventListener('push', (event) => {
  let data = {}
  try { data = event.data ? event.data.json() : {} } catch(e) { data = { body: event.data && event.data.text() } }
  const title = data.title || 'Overview+'
  const body = data.body || (typeof data === 'string' ? data : 'You have a new notification')
  const options = {
    body,
    icon: '/favicon.ico',
    badge: '/favicon.ico',
    data: data.url ? { url: data.url } : {}
  }
  event.waitUntil(self.registration.showNotification(title, options))
})

self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  const url = event.notification.data && event.notification.data.url
  if (url) {
    event.waitUntil(clients.openWindow(url))
  }
})