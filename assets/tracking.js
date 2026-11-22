/* Godolphy · consentimiento de cookies + GA4 + Meta Pixel + TikTok Pixel + evento de lead.
   GA4 y Meta solo guardan cookies si la persona acepta (Consent Mode v2). */
// Clic en «Prueba gratis» antes de que cargue /assets/signup-modal.js (móvil lento, Tailwind CDN bloqueando):
// se retiene el clic y el modal se abre en cuanto el script está listo (máx. 4 s; si no, va al enlace).
(function () {
  var SEL = 'a[href^="https://app.godolphy.com/auth/sign-up"],[data-gd-signup]';
  document.addEventListener('click', function (e) {
    if (window.gdOpenSignup) return;
    var el = e.target && e.target.closest && e.target.closest(SEL);
    if (!el || el.hasAttribute('data-gd-direct') || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    window.__gdQueuedSignup = el;
    setTimeout(function () {
      if (!window.gdOpenSignup && window.__gdQueuedSignup === el && el.href) location.href = el.href;
    }, 4000);
  }, true);
})();
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

  // ── Mismo visitante en godolphy.com y app.godolphy.com (PostHog, 20/11/2026) ──
  // Sin cookies aceptadas PostHog guarda el id solo en memoria: al ir a la app se pasa
  // por la URL (ph_did / ph_sid, y gd_c=1 si se aceptaron las cookies). La app los lee y los quita.
  function handOver(e) {
    var a = e.target && e.target.closest && e.target.closest('a[href*="app.godolphy.com"]');
    if (!a || !window.posthog || !posthog.get_distinct_id) return;
    try {
      var url = new URL(a.href);
      url.searchParams.set('ph_did', posthog.get_distinct_id());
      var sid = posthog.get_session_id && posthog.get_session_id();
      if (sid) url.searchParams.set('ph_sid', sid);
      if (getChoice() === 'granted') url.searchParams.set('gd_c', '1');
      a.href = url.toString();
    } catch (x) {}
  }
  document.addEventListener('click', handOver, true);
  document.addEventListener('auxclick', handOver, true);

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

  // ── Banner (guía AEPD: aceptar y rechazar al mismo nivel y tamaño, sin cookie wall) ──
  // No se guarda nada hasta que se pulsa un botón: si no elige, vuelve a salir en la página siguiente.
  function banner() {
    if (!document.getElementById('gd-cookies-css')) {
      var cs = document.createElement('style'); cs.id = 'gd-cookies-css';
      cs.textContent =
        '#gd-cookies{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:99999;width:calc(100% - 32px);max-width:560px;box-sizing:border-box;' +
        'background:#fff;color:#02021e;border-radius:20px;padding:16px 20px;box-shadow:0 18px 50px rgba(30,10,90,.28),0 2px 8px rgba(30,10,90,.12);' +
        'border:1px solid rgba(99,28,255,.14);font-family:Inter,system-ui,-apple-system,sans-serif;font-size:14px;line-height:1.5;text-align:left}' +
        '#gd-cookies .gc-t{display:block;font-family:Gabarito,Inter,system-ui,sans-serif;font-size:17px;font-weight:700;margin:0 0 4px;color:#02021e}' +
        '#gd-cookies p{margin:0;color:rgba(2,2,30,.78)}' +
        '#gd-cookies a{color:#631cff;font-weight:600;text-decoration:underline;text-underline-offset:2px}' +
        '#gd-cookies .gc-b{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}' +
        '#gd-cookies button{font:inherit;font-size:15px;font-weight:700;border-radius:12px;padding:10px 14px;cursor:pointer;min-height:44px;width:100%}' +
        '#gd-cookies.gc-side{left:auto;right:20px;transform:none;max-width:420px}' +
        '#gd-cookies button[data-c=granted]{background:#631cff;color:#fff;border:2px solid #631cff}' +
        '#gd-cookies button[data-c=denied]{background:#fff;color:#3a0fa8;border:2px solid #631cff}' +
        '#gd-cookies button:focus-visible{outline:3px solid #EEFE3A;outline-offset:2px}' +
        '@media(max-width:600px){#gd-cookies{bottom:8px;width:calc(100% - 16px);padding:10px 12px;border-radius:16px;font-size:12px;line-height:1.36}' +
        '#gd-cookies .gc-t{display:inline;font-size:13px;margin:0 4px 0 0}' +
        '#gd-cookies .gc-b{margin-top:8px;gap:8px}#gd-cookies button{font-size:14px;padding:8px 10px;min-height:38px;border-radius:10px}}';
      document.head.appendChild(cs);
    }
    var d = document.createElement('div');
    d.id = 'gd-cookies';
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-modal', 'false');
    d.setAttribute('aria-labelledby', 'gd-cookies-t');
    d.innerHTML = '<p><strong class="gc-t" id="gd-cookies-t">¿Nos ayudas a mejorar?</strong> ' +
      'Usamos cookies para medir qué contenido te resulta útil y mostrarte novedades para tu salón. Puedes aceptarlas o rechazarlas cuando quieras. ' +
      '<a href="/politica-de-cookies/">Más info</a></p>' +
      '<div class="gc-b"><button type="button" data-c="denied">Rechazar</button><button type="button" data-c="granted">Aceptar</button></div>';
    d.addEventListener('click', function (e) {
      var c = e.target && e.target.getAttribute && e.target.getAttribute('data-c');
      if (!c) return;
      setChoice(c);
      if (c === 'granted') grant();
      d.remove();
    });
    document.body.appendChild(d);
    // En escritorio, si la tarjeta tapa un botón de la primera pantalla, se coloca abajo a la derecha.
    try {
      if (window.innerWidth > 900) {
        var cr = d.getBoundingClientRect();
        var hit = [].some.call(document.querySelectorAll('a,button'), function (el) {
          if (d.contains(el) || !el.offsetParent) return false;
          var r = el.getBoundingClientRect();
          if (r.height < 34 || r.top < 70 || r.bottom > window.innerHeight) return false;
          var bg = getComputedStyle(el).backgroundColor;
          if (!bg || bg === 'transparent' || bg === 'rgba(0, 0, 0, 0)') return false;
          return r.left < cr.right && r.right > cr.left && r.top < cr.bottom && r.bottom > cr.top;
        });
        if (hit) d.classList.add('gc-side');
      }
    } catch (e) {}
  }

  var choice = getChoice();
  if (choice === 'granted') grant();
  else if (!choice) {
    if (document.body) banner(); else document.addEventListener('DOMContentLoaded', banner);
  }

  // Permite reabrir el banner desde la política de cookies: <a href="#" onclick="gdCookies()">
  window.gdCookies = function () { try { localStorage.removeItem(KEY); } catch (e) {} if (!document.getElementById('gd-cookies')) banner(); return false; };
})();
