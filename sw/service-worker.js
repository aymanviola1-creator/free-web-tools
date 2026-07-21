// Service Worker for Free Web Tools — PWA offline support
const CACHE_NAME = 'free-web-tools-v1';
const urlsToCache = [
  '/free-web-tools/',
  '/free-web-tools/index.html',
  '/free-web-tools/robots.txt',
  '/free-web-tools/sitemap.xml'
];

// Install event — cache core assets
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// Activate event — clean old caches
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(name) {
          if (name !== CACHE_NAME) {
            return caches.delete(name);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch event — serve from cache, fallback to network
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      // Cache hit — return response
      if (response) {
        return response;
      }
      // Clone the request
      var fetchRequest = event.request.clone();
      return fetch(fetchRequest).then(function(response) {
        // Check if valid response
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }
        // Clone the response
        var responseToCache = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(event.request, responseToCache);
        });
        return response;
      });
    })
  );
});
