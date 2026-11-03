// Lead magnets of godolphy.com (3/11/2026).
// Real serverless function (the old external rewrite returned 404 because of trailingSlash).
// Forwards the form to the dashboard endpoint, which saves the contact in ActiveCampaign
// and returns the download URL. The PDF URL never appears in this public repo.
const UPSTREAM = 'https://dashboard.godolphy.com/api/activecampaign-signup';

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  if (req.method !== 'POST') {
    res.statusCode = 405;
    res.end(JSON.stringify({ error: 'Method not allowed' }));
    return;
  }
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (_) { body = null; } }
  if (!body || typeof body !== 'object' || !body.email) {
    res.statusCode = 400;
    res.end(JSON.stringify({ error: 'Email is required' }));
    return;
  }
  try {
    const r = await fetch(UPSTREAM, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const text = await r.text();
    res.statusCode = r.status;
    res.end(text || '{}');
  } catch (err) {
    console.error('[api/lead] upstream error', err && err.message);
    res.statusCode = 502;
    res.end(JSON.stringify({ error: 'Upstream unavailable' }));
  }
};
