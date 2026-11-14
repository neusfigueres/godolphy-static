/* Godolphy · consentimiento de cookies + GA4 + Meta Pixel + TikTok Pixel + evento de lead.
   GA4 y Meta solo guardan cookies si la persona acepta (Consent Mode v2). */
(function () {
  var GA_ID = 'G-8JZDWMXKD9';
  var META_PIXEL_ID = '1468217345164128'; // Píxel 'Godolphy web' (Godolphy Software LLC)
  var META_PIXEL_ID_2 = '1116719227671218'; // Píxel 'Godolphy web 2' (portfolio 'Godolphy', cuenta publicitaria de campañas)
  var TIKTOK_PIXEL_ID = 'DB6B743C77UAU0U4EKF0'; // Píxel 'Godolphy web' (TikTok Ads)
  var KEY = 'gd_consent'; // 'granted' | 'denied'

  function getChoice() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function setChoice(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  // ── Google Analytics 4 con Consent Mode v2 (por defecto, denegado) ──
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  gtag('consent', 'default', {
    ad_storage: 'denied', analytics_storage: 'denied',
    ad_user_data: 'denied', ad_personalization: 'denied',
    wait_for_update: 500
  });
  var s = document.createElement('script');
  s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
  gtag('js', new Date());
  gtag('config', GA_ID);

  // ── Meta Pixel (solo con consentimiento) ──
  function loadMeta() {
    if (!META_PIXEL_ID || window.fbq) return;
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments) }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s) }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', META_PIXEL_ID);
    if (META_PIXEL_ID_2) fbq('init', META_PIXEL_ID_2);
    fbq('track', 'PageView');
  }

  // ── TikTok Pixel (solo con consentimiento) ──
  function loadTikTok() {
    if (!TIKTOK_PIXEL_ID || window.ttq) return;
    !function (w, d, t) { w.TiktokAnalyticsObject = t; var ttq = w[t] = w[t] || []; ttq.methods = ["page", "track", "identify", "instances", "debug", "on", "off", "once", "ready", "alias", "group", "enableCookie", "disableCookie", "holdConsent", "revokeConsent", "grantConsent"], ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))) } }; for (var i = 0; i < ttq.methods.length; i++)ttq.setAndDefer(ttq, ttq.methods[i]); ttq.instance = function (t) { for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++)ttq.setAndDefer(e, ttq.methods[n]); return e }, ttq.load = function (e, n) { var r = "https://analytics.tiktok.com/i18n/pixel/events.js", o = n && n.partner; ttq._i = ttq._i || {}, ttq._i[e] = [], ttq._i[e]._u = r, ttq._t = ttq._t || {}, ttq._t[e] = +new Date, ttq._o = ttq._o || {}, ttq._o[e] = n || {}; n = document.createElement("script"); n.type = "text/javascript", n.async = !0, n.src = r + "?sdkid=" + e + "&lib=" + t; e = document.getElementsByTagName("script")[0]; e.parentNode.insertBefore(n, e) };
      ttq.load(TIKTOK_PIXEL_ID); ttq.page(); }(window, document, 'ttq');
  }

  function grant() {
    gtag('consent', 'update', {
      ad_storage: 'granted', analytics_storage: 'granted',
      ad_user_data: 'granted', ad_personalization: 'granted'
    });
    if (window.posthog && posthog.set_config) posthog.set_config({ persistence: 'localStorage+cookie' });
    loadMeta();
    loadTikTok();
  }

  // ── UTMs: se guardan durante la visita (sessionStorage, sin cookies) para no perderlas al cambiar de página ──
  var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  window.gdGetUtm = function () {
    var saved = {}, p = new URLSearchParams(location.search), fromUrl = {};
    try { saved = JSON.parse(sessionStorage.getItem('gd_utm') || '{}'); } catch (e) {}
    UTM_KEYS.forEach(function (k) { if (p.get(k)) fromUrl[k] = p.get(k); });
    if (Object.keys(fromUrl).length) { saved = fromUrl; try { sessionStorage.setItem('gd_utm', JSON.stringify(saved)); } catch (e) {} }
    return saved;
  };
  window.gdGetUtm();

  // ── fbclid del clic en el anuncio de Meta: se guarda durante la visita (sessionStorage, sin cookies)
  //    para que la API de Conversiones pueda atribuir el lead al anuncio aunque no se acepten cookies ──
  window.gdGetFbc = function () {
    var p = new URLSearchParams(location.search), id = p.get('fbclid'), fbc = null;
    try { fbc = sessionStorage.getItem('gd_fbc'); } catch (e) {}
    if (id) { fbc = 'fb.1.' + Date.now() + '.' + id; try { sessionStorage.setItem('gd_fbc', fbc); } catch (e) {} }
    return fbc;
  };
  window.gdGetFbc();

  // Pasa las UTMs a los enlaces del dashboard (otro subdominio: allí no llega el sessionStorage)
  function decorateDashboardLinks() {
    var u = window.gdGetUtm();
    if (!Object.keys(u).length) return;
    var links = document.querySelectorAll('a[href*="dashboard.godolphy.com"], a[href*="app.godolphy.com/auth/sign-up"]');
    for (var i = 0; i < links.length; i++) {
      try {
        var url = new URL(links[i].href);
        UTM_KEYS.forEach(function (k) { if (u[k] && !url.searchParams.get(k)) url.searchParams.set(k, u[k]); });
        links[i].href = url.toString();
      } catch (e) {}
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', decorateDashboardLinks);
  else decorateDashboardLinks();

  // ── Lead: alta en la lista de espera ──
  window.gdTrackLead = function (extra) {
    var props = extra || {}, u = window.gdGetUtm();
    UTM_KEYS.forEach(function (k) { if (u[k]) props[k] = u[k]; });
    var email = props.email;
    if (!email) { var inp = document.querySelector('input[type=email]'); if (inp && inp.value) email = inp.value.trim(); }
    var phone = props.phone ? String(props.phone) : '';
    delete props.email; // el email y el teléfono nunca van en claro a GA, al píxel ni a PostHog desde aquí
    delete props.phone;
    var eventId = 'lead_' + Date.now() + '_' + Math.random().toString(36).slice(2, 10);
    try { gtag('event', 'generate_lead', props); } catch (e) {}
    try { if (window.fbq) fbq('track', 'Lead', props, { eventID: eventId }); } catch (e) {}
    // API de Conversiones de Meta (servidor): cuenta el lead aunque no se hayan aceptado cookies.
    // Solo se llama al enviar un formulario, donde ya se ha aceptado la política de privacidad.
    try {
      var fbp = (document.cookie.match(/(?:^|; )_fbp=([^;]+)/) || [])[1];
      var body = JSON.stringify(Object.assign({ event_name: 'Lead', event_id: eventId, email: email, phone: phone || undefined, fbc: window.gdGetFbc(), fbp: fbp, url: location.href }, props));
      if (navigator.sendBeacon) navigator.sendBeacon('/api/capi', new Blob([body], { type: 'application/json' }));
      else fetch('/api/capi', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: body, keepalive: true });
    } catch (e) {}
    try { if (window.ttq) ttq.track('SubmitForm', props); } catch (e) {}
    try { if (window.posthog) posthog.capture('waitlist_submitted', props); } catch (e) {}
  };

  // ── Banner ──
  function banner() {
    var d = document.createElement('div');
    d.id = 'gd-cookies';
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-label', 'Preferencias de cookies');
    d.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#02021e;color:#fff;padding:10px 14px;box-shadow:0 -6px 24px rgba(0,0,0,.18);font-family:system-ui,sans-serif;font-size:12.5px;line-height:1.4;display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;';
    // En móvil: una sola línea compacta (texto corto + botones), para no tapar el CTA
    if (!document.getElementById('gd-cookies-css')) {
      var cs = document.createElement('style'); cs.id = 'gd-cookies-css';
      cs.textContent = '#gd-cookies .gc-s{display:none}' +
        '@media(max-width:600px){#gd-cookies{flex-wrap:nowrap!important;gap:8px!important;padding:8px 10px!important;font-size:12px!important;justify-content:space-between!important}' +
        '#gd-cookies p{flex:1 1 auto!important;min-width:0}#gd-cookies .gc-l{display:none}#gd-cookies .gc-s{display:inline}' +
        '#gd-cookies button{padding:6px 10px!important;border-radius:8px!important}#gd-cookies>div{gap:6px!important}}';
      document.head.appendChild(cs);
    }
    d.innerHTML = '<p style="margin:0;color:rgba(255,255,255,.85);flex:1 1 220px;max-width:640px;"><span class="gc-l">Usamos cookies para analizar la web y mostrarte publicidad relevante.</span><span class="gc-s">Usamos cookies.</span> <a href="/politica-de-cookies/" style="color:#EEFE3A;">Más info</a></p>' +
      '<div style="display:flex;gap:8px;flex:0 0 auto;">' +
      '<button type="button" data-c="denied" style="background:transparent;color:#fff;border:1px solid rgba(255,255,255,.4);border-radius:10px;padding:7px 14px;font:inherit;font-weight:600;cursor:pointer;">Rechazar</button>' +
      '<button type="button" data-c="granted" style="background:#EEFE3A;color:#02021e;border:0;border-radius:10px;padding:7px 14px;font:inherit;font-weight:700;cursor:pointer;">Aceptar</button></div>';
    d.addEventListener('click', function (e) {
      var c = e.target && e.target.getAttribute && e.target.getAttribute('data-c');
      if (!c) return;
      setChoice(c);
      if (c === 'granted') grant();
      d.remove();
    });
    document.body.appendChild(d);
  }

  var choice = getChoice();
  if (choice === 'granted') grant();
  else if (!choice) {
    if (document.body) banner(); else document.addEventListener('DOMContentLoaded', banner);
  }

  // Permite reabrir el banner desde la política de cookies: <a href="#" onclick="gdCookies()">
  window.gdCookies = function () { try { localStorage.removeItem(KEY); } catch (e) {} if (!document.getElementById('gd-cookies')) banner(); return false; };
})();
