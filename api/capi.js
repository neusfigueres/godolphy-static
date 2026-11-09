// Meta Conversions API (9/11/2026).
// The browser calls this only when someone submits a form (lead magnet, waitlist…),
// where they have already accepted the privacy policy. The event goes to Meta from
// the server, so it is counted even if the person rejected cookies and the pixel never loaded.
// The email is hashed (SHA-256) before leaving here; Meta never receives it in clear text.
// Required env var in Vercel: META_CAPI_TOKEN (Events Manager › pixel › Settings › Conversions API).
// Optional: META_PIXEL_ID (defaults to 'Godolphy web 2', the pixel of the ad account),
//           META_TEST_EVENT_CODE (to see the events in Events Manager › Test events).
const crypto = require('crypto');

const PIXEL_ID = process.env.META_PIXEL_ID || '1116719227671218';
const ALLOWED_EVENTS = ['Lead', 'CompleteRegistration', 'SubmitApplication', 'Contact'];

function sha256(v) {
  return crypto.createHash('sha256').update(String(v).trim().toLowerCase()).digest('hex');
}

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  if (req.method !== 'POST') { res.statusCode = 405; res.end('{"error":"Method not allowed"}'); return; }

  const token = process.env.META_CAPI_TOKEN;
  if (!token) { res.statusCode = 200; res.end('{"sent":false,"reason":"no token"}'); return; }

  let b = req.body;
  if (typeof b === 'string') { try { b = JSON.parse(b); } catch (_) { b = null; } }
  if (!b || typeof b !== 'object') { res.statusCode = 400; res.end('{"error":"Bad body"}'); return; }

  const eventName = ALLOWED_EVENTS.includes(b.event_name) ? b.event_name : 'Lead';
  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || undefined;
  const ua = req.headers['user-agent'] || undefined;

  const userData = { client_ip_address: ip, client_user_agent: ua };
  const email = b.email ? String(b.email).trim() : '';
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) userData.em = [sha256(email)];
  if (b.fbc && /^fb\.1\.\d+\./.test(b.fbc)) userData.fbc = String(b.fbc).slice(0, 500);
  if (b.fbp && /^fb\.1\.\d+\./.test(b.fbp)) userData.fbp = String(b.fbp).slice(0, 200);

  const custom = {};
  ['form', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach((k) => {
    if (b[k]) custom[k] = String(b[k]).slice(0, 200);
  });

  const payload = {
    data: [{
      event_name: eventName,
      event_time: Math.floor(Date.now() / 1000),
      event_id: b.event_id ? String(b.event_id).slice(0, 100) : undefined,
      action_source: 'website',
      event_source_url: b.url ? String(b.url).slice(0, 1000) : undefined,
      user_data: userData,
      custom_data: custom,
    }],
  };
  if (process.env.META_TEST_EVENT_CODE) payload.test_event_code = process.env.META_TEST_EVENT_CODE;

  try {
    const r = await fetch(`https://graph.facebook.com/v21.0/${PIXEL_ID}/events?access_token=${encodeURIComponent(token)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) console.error('[api/capi] meta error', r.status, j && j.error && j.error.message);
    res.statusCode = 200;
    res.end(JSON.stringify({ sent: r.ok, received: j.events_received || 0 }));
  } catch (err) {
    console.error('[api/capi] fetch error', err && err.message);
    res.statusCode = 200;
    res.end('{"sent":false}');
  }
};
