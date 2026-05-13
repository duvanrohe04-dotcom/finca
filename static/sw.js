// Service Worker simple para PWA (cache básico)
const CACHE_NAME = 'finca-admin-v3';
const PRECACHE_URLS = [
  '/',
  '/login',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/img/fondo.jpg',
  '/static/img/logo.jpg',
  '/static/img/icon-192.png',
  '/static/img/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE_URLS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Network-first para páginas; stale-while-revalidate para estáticos (para que cambios se vean rápido)
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Solo manejamos GET
  if (req.method !== 'GET') return;

  // HTML: network-first
  if (req.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then((cached) => cached || caches.match('/login')))
    );
    return;
  }

  // Státicos: stale-while-revalidate
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(req).then((cached) => {
        const fetchPromise = fetch(req)
          .then((res) => {
            const copy = res.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
            return res;
          })
          .catch(() => cached);

        // Si hay caché, lo devolvemos rápido y actualizamos en segundo plano.
        return cached || fetchPromise;
      })
    );
  }
});
