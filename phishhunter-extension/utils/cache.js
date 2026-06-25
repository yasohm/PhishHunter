const CACHE_KEY = 'pg_url_cache';
const MAX_ENTRIES = 500;

export async function getFromCache(url) {
  const { [CACHE_KEY]: cache = {} } = await chrome.storage.local.get(CACHE_KEY);
  const entry = cache[url];
  if (!entry) return null;
  const { cacheMinutes = 30 } = await chrome.storage.local.get('cacheMinutes');
  if (Date.now() > entry.savedAt + cacheMinutes * 60_000) return null;
  return entry.result;
}

export async function saveToCache(url, result) {
  const { [CACHE_KEY]: cache = {} } = await chrome.storage.local.get(CACHE_KEY);
  const keys = Object.keys(cache);
  if (keys.length >= MAX_ENTRIES) {
    // Evict oldest 50 entries
    keys.sort((a, b) => cache[a].savedAt - cache[b].savedAt)
        .slice(0, 50)
        .forEach(k => delete cache[k]);
  }
  cache[url] = { result, savedAt: Date.now() };
  await chrome.storage.local.set({ [CACHE_KEY]: cache });
}

export async function clearCache() {
  await chrome.storage.local.remove(CACHE_KEY);
}

export async function getCacheStats() {
  const { [CACHE_KEY]: cache = {} } = await chrome.storage.local.get(CACHE_KEY);
  return { count: Object.keys(cache).length };
}

export async function getRecentScans(limit = 5) {
  const { [CACHE_KEY]: cache = {} } = await chrome.storage.local.get(CACHE_KEY);
  return Object.entries(cache)
    .map(([url, { result, savedAt }]) => ({ url, ...result, savedAt }))
    .sort((a, b) => b.savedAt - a.savedAt)
    .slice(0, limit);
}
