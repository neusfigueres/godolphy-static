// Country of the visitor, from Vercel's geolocation header (30/10/2026).
// Used by /precio/ to show plan prices in EUR, USD or MXN. No personal data is stored.
module.exports = (req, res) => {
  const country = String(req.headers['x-vercel-ip-country'] || '').toUpperCase().slice(0, 2);
  res.setHeader('Cache-Control', 'private, no-store');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify({ country: /^[A-Z]{2}$/.test(country) ? country : null }));
};
