export async function callAPI(url) {
  const { apiUrl = 'http://localhost:8000' } = await chrome.storage.local.get('apiUrl');
  const response = await fetch(`${apiUrl}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  if (!response.ok) throw new Error(`API error ${response.status}`);
  return response.json();
}
