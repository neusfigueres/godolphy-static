/* Godolphy · consentimiento de cookies + GA4 + Meta Pixel + evento de lead.
   GA4 y Meta solo guardan cookies si la persona acepta (Consent Mode v2). */
(function () {
  var GA_ID = 'G-QP43GQ9V08';
  var META_PIXEL_ID = ''; // pendiente: ID del Pixel de Meta
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
    fbq('track', 'PageView');
  }

  function grant() {
    gtag('consent', 'update', {
      ad_storage: 'granted', analytics_storage: 'granted',
      ad_user_data: 'granted', ad_personalization: 'granted'
    });
    if (window.posthog && posthog.set_config) posthog.set_config({ persistence: 'localStorage+cookie' });
    loadMeta();
  }

  // ── Lead: alta en la lista de espera ──
  window.gdTrackLead = function (extra) {
    var p = new URLSearchParams(location.search), props = extra || {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) { if (p.get(k)) props[k] = p.get(k); });
    try { gtag('event', 'generate_lead', props); } catch (e) {}
    try { if (window.fbq) fbq('track', 'Lead', props); } catch (e) {}
    try { if (window.posthog) posthog.capture('waitlist_submitted', props); } catch (e) {}
  };

  // ── Banner ──
  function banner() {
    var d = document.createElement('div');
    d.id = 'gd-cookies';
    d.setAttribute('role', 'dialog');
    d.setAttribute('aria-label', 'Preferencias de cookies');
    d.style.cssText = 'position:fixed;left:16px;right:16px;bottom:16px;z-index:99999;max-width:560px;margin:0 auto;background:#02021e;color:#fff;border-radius:16px;padding:18px 20px;box-shadow:0 12px 40px rgba(0,0,0,.25);font-family:Poppins,system-ui,sans-serif;font-size:14px;line-height:1.5;';
    d.innerHTML = '<p style="margin:0 0 14px;color:rgba(255,255,255,.85);">Usamos cookies propias y de terceros para analizar el uso de la web y mostrarte publicidad relevante. Puedes aceptarlas o rechazarlas. <a href="/politica-de-cookies/" style="color:#EEFE3A;">Más información</a></p>' +
      '<div style="display:flex;gap:10px;justify-content:flex-end;flex-wrap:wrap;">' +
      '<button type="button" data-c="denied" style="background:transparent;color:#fff;border:1.5px solid rgba(255,255,255,.4);border-radius:12px;padding:9px 18px;font:inherit;font-weight:600;cursor:pointer;">Rechazar</button>' +
      '<button type="button" data-c="granted" style="background:#EEFE3A;color:#02021e;border:0;border-radius:12px;padding:9px 18px;font:inherit;font-weight:700;cursor:pointer;">Aceptar</button></div>';
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
