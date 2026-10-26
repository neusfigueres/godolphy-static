/* Godolphy · modal de alta rápida para la prueba gratuita (30 días, sin tarjeta).
   Uso: cualquier elemento con el atributo data-gd-signup abre el modal, o window.gdOpenSignup().
   Endpoint: POST https://api.godolphy.com/public/signup-trial (CORS solo www.godolphy.com / godolphy.com). */
(function () {
  if (window.gdOpenSignup) return;
  var ENDPOINT = 'https://api.godolphy.com/public/signup-trial';
  var LOGIN = 'https://app.godolphy.com/auth/sign-in';

  var TZ_COUNTRY = {
    'Europe/Madrid': 'ES', 'Atlantic/Canary': 'ES', 'Africa/Ceuta': 'ES', 'Europe/Andorra': 'AD', 'Europe/Lisbon': 'PT',
    'America/Mexico_City': 'MX', 'America/Monterrey': 'MX', 'America/Cancun': 'MX', 'America/Merida': 'MX', 'America/Tijuana': 'MX',
    'America/Chihuahua': 'MX', 'America/Hermosillo': 'MX', 'America/Mazatlan': 'MX', 'America/Matamoros': 'MX', 'America/Bahia_Banderas': 'MX',
    'America/Bogota': 'CO', 'America/Lima': 'PE', 'America/Santiago': 'CL', 'America/Caracas': 'VE', 'America/Montevideo': 'UY',
    'America/Asuncion': 'PY', 'America/La_Paz': 'BO', 'America/Guayaquil': 'EC', 'America/Panama': 'PA', 'America/Costa_Rica': 'CR',
    'America/Santo_Domingo': 'DO', 'America/Havana': 'CU', 'America/Guatemala': 'GT', 'America/Tegucigalpa': 'HN',
    'America/El_Salvador': 'SV', 'America/Managua': 'NI', 'America/Puerto_Rico': 'PR'
  };

  function tz() { try { return Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) { return ''; } }
  function country(z) { if (!z) return ''; if (z.indexOf('America/Argentina/') === 0) return 'AR'; return TZ_COUNTRY[z] || ''; }
  function utm() { try { return window.gdGetUtm ? window.gdGetUtm() : {}; } catch (e) { return {}; } }

  var css = '' +
    '#gd-su{position:fixed;inset:0;z-index:100000;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(2,2,30,.62);font-family:Poppins,system-ui,sans-serif}' +
    '#gd-su[hidden]{display:none!important}' +
    '#gd-su .b{position:relative;width:100%;max-width:440px;max-height:calc(100% - 32px);overflow:auto;background:#fff;color:#02021e;border-radius:20px;padding:30px 26px 24px;box-shadow:0 24px 60px rgba(0,0,0,.3)}' +
    '#gd-su h2{margin:0 0 6px;padding-right:34px;font-family:Gabarito,Poppins,sans-serif;font-size:27px;line-height:1.1;font-weight:800;letter-spacing:-.01em}' +
    '#gd-su .s{margin:0 0 18px;font-size:14.5px;line-height:1.5;color:#45455e}' +
    '#gd-su label.e{display:block;font-size:13px;font-weight:600;margin:0 0 6px}' +
    '#gd-su input[type=email]{width:100%;box-sizing:border-box;font:inherit;font-size:16px;padding:13px 14px;border:1.5px solid #cfcfe0;border-radius:12px;outline:none;color:#02021e;background:#fff}' +
    '#gd-su input[type=email]:focus{border-color:#631cff;box-shadow:0 0 0 3px rgba(99,28,255,.18)}' +
    '#gd-su .ck{display:flex;gap:10px;align-items:flex-start;margin:12px 0 0;font-size:13px;line-height:1.45;color:#45455e;cursor:pointer}' +
    '#gd-su .ck input{margin:2px 0 0;width:17px;height:17px;flex:none;accent-color:#631cff}' +
    '#gd-su .ck a{color:#631cff}' +
    '#gd-su .er{min-height:18px;margin:8px 0 0;font-size:13px;color:#c0233b}' +
    '#gd-su .er a{color:#631cff;font-weight:600}' +
    '#gd-su button.go{width:100%;margin:10px 0 0;font:inherit;font-size:16px;font-weight:700;padding:14px;border:0;border-radius:12px;background:#631cff;color:#fff;cursor:pointer}' +
    '#gd-su button.go:disabled{opacity:.6;cursor:wait}' +
    '#gd-su button.go:focus-visible,#gd-su .x:focus-visible{outline:3px solid #EEFE3A;outline-offset:2px}' +
    '#gd-su .x{position:absolute;top:12px;right:12px;width:36px;height:36px;border:0;border-radius:50%;background:#f1f0f7;color:#02021e;font-size:20px;line-height:1;cursor:pointer}' +
    '#gd-su .ft{margin:12px 0 0;font-size:12.5px;color:#6b6b80;text-align:center}' +
    '#gd-su .ft a{color:#631cff;font-weight:600}' +
    '#gd-su .hp{position:absolute!important;left:-10000px!important;top:auto!important;width:1px!important;height:1px!important;overflow:hidden!important}' +
    '#gd-su .ok{text-align:center;padding:8px 0 4px}#gd-su .ok h2{padding-right:0}' +
    '#gd-su .ok .ic{width:56px;height:56px;margin:0 auto 14px;border-radius:50%;background:#EEFE3A;display:flex;align-items:center;justify-content:center;font-size:28px}';

  var html = '' +
    '<div class="b" role="dialog" aria-modal="true" aria-labelledby="gd-su-t">' +
      '<button type="button" class="x" aria-label="Cerrar">&times;</button>' +
      '<div class="f">' +
        '<h2 id="gd-su-t">Prueba Godolphy 30 días gratis</h2>' +
        '<p class="s">Sin tarjeta. Con todas las funciones del plan Pro. Solo necesitamos tu email para crear tu cuenta.</p>' +
        '<form novalidate>' +
          '<label class="e" for="gd-su-email">Tu email</label>' +
          '<input id="gd-su-email" name="email" type="email" autocomplete="email" inputmode="email" placeholder="tu@salon.com" required>' +
          '<div class="hp" aria-hidden="true"><label for="gd-su-website">Web</label><input id="gd-su-website" name="website" type="text" autocomplete="off" tabindex="-1"></div>' +
          '<label class="ck"><input id="gd-su-terms" type="checkbox"> <span>Acepto los <a href="/terminos-y-condiciones/" target="_blank" rel="noopener">términos y condiciones</a> y la <a href="/politica-de-privacidad/" target="_blank" rel="noopener">política de privacidad</a>.</span></label>' +
          '<label class="ck"><input id="gd-su-mkt" type="checkbox"> <span>Quiero recibir consejos y novedades de Godolphy por email (opcional).</span></label>' +
          '<p class="er" role="alert" aria-live="polite"></p>' +
          '<button type="submit" class="go">Crear mi cuenta gratis</button>' +
        '</form>' +
        '<p class="ft">¿Ya tienes cuenta? <a href="' + LOGIN + '">Entra aquí</a></p>' +
      '</div>' +
      '<div class="ok" hidden>' +
        '<div class="ic" aria-hidden="true">✉</div>' +
        '<h2>Revisa tu correo</h2>' +
        '<p class="s">Te hemos enviado un enlace para crear tu contraseña. Caduca en 24 horas. Si no lo ves, mira en la carpeta de spam o promociones.</p>' +
      '</div>' +
    '</div>';

  var root, form, emailIn, termsIn, mktIn, hpIn, err, btn, lastFocus;

  function build() {
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    root = document.createElement('div'); root.id = 'gd-su'; root.hidden = true; root.innerHTML = html;
    document.body.appendChild(root);
    form = root.querySelector('form'); emailIn = root.querySelector('#gd-su-email');
    termsIn = root.querySelector('#gd-su-terms'); mktIn = root.querySelector('#gd-su-mkt');
    hpIn = root.querySelector('#gd-su-website'); err = root.querySelector('.er'); btn = root.querySelector('.go');
    root.querySelector('.x').addEventListener('click', close);
    root.addEventListener('click', function (e) { if (e.target === root) close(); });
    document.addEventListener('keydown', function (e) {
      if (root.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'Tab') trap(e);
    });
    form.addEventListener('submit', submit);
  }

  function trap(e) {
    var f = [].slice.call(root.querySelectorAll('a[href],button,input:not([tabindex="-1"])')).filter(function (n) { return n.offsetParent !== null; });
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  function open(e) {
    if (e && e.preventDefault) e.preventDefault();
    if (!root) build();
    lastFocus = document.activeElement;
    root.querySelector('.f').hidden = false; root.querySelector('.ok').hidden = true;
    err.innerHTML = ''; btn.disabled = false; btn.textContent = 'Crear mi cuenta gratis';
    root.hidden = false; document.documentElement.style.overflow = 'hidden';
    setTimeout(function () { emailIn.focus(); }, 30);
    try { if (window.gtag) gtag('event', 'signup_modal_open'); } catch (x) {}
  }

  function close() {
    root.hidden = true; document.documentElement.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function showErr(t) { err.innerHTML = t; }

  function success() {
    root.querySelector('.f').hidden = true; root.querySelector('.ok').hidden = false;
    var props = {}, u = utm();
    Object.keys(u).forEach(function (k) { props[k] = u[k]; });
    try { if (window.gtag) gtag('event', 'sign_up', Object.assign({ method: 'email' }, props)); } catch (x) {}
    try { if (window.fbq) fbq('track', 'CompleteRegistration', props); } catch (x) {}
    try { if (window.ttq) ttq.track('CompleteRegistration', props); } catch (x) {}
    try { if (window.posthog) posthog.capture('trial_signup', props); } catch (x) {}
    root.querySelector('.x').focus();
  }

  function submit(e) {
    e.preventDefault();
    var email = (emailIn.value || '').trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { showErr('Revisa el email: parece que no es correcto.'); emailIn.focus(); return; }
    if (!termsIn.checked) { showErr('Para crear la cuenta tienes que aceptar los términos y la política de privacidad.'); termsIn.focus(); return; }
    showErr(''); btn.disabled = true; btn.textContent = 'Creando tu cuenta…';
    var z = tz(), c = country(z), u = utm();
    var body = {
      email: email, timezone: z, accept_terms: true, marketing_consent: !!mktIn.checked,
      utm_source: u.utm_source || '', utm_medium: u.utm_medium || '', utm_campaign: u.utm_campaign || '', utm_content: u.utm_content || '',
      referrer: document.referrer || '', website: hpIn.value || ''
    };
    if (c) body.country = c;
    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { s: r.status, d: d || {} }; }); })
      .then(function (res) {
        var code = res.d.code;
        if (res.s === 201) return success();
        if (res.s === 409 || code === 'exists') showErr('Ya tienes cuenta con este email. <a href="' + LOGIN + '">Entra aquí</a>');
        else if (code === 'invalid_email') { showErr('Revisa el email: parece que no es correcto.'); emailIn.focus(); }
        else if (code === 'terms_required') showErr('Para crear la cuenta tienes que aceptar los términos y la política de privacidad.');
        else if (res.s === 429 || code === 'rate_limited') showErr('Demasiados intentos. Inténtalo más tarde.');
        else showErr('No hemos podido crear la cuenta. Inténtalo de nuevo en unos minutos.');
        btn.disabled = false; btn.textContent = 'Crear mi cuenta gratis';
      })
      .catch(function () {
        showErr('No hemos podido conectar. Revisa tu conexión e inténtalo de nuevo.');
        btn.disabled = false; btn.textContent = 'Crear mi cuenta gratis';
      });
  }

  window.gdOpenSignup = open;
  // Enlace directo: cualquier página con ?alta=1 abre el modal al cargar (las UTM de la URL se conservan)
  try {
    if (new URLSearchParams(location.search).get('alta') === '1') {
      if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { open(); });
      else open();
    }
  } catch (e) {}
  document.addEventListener('click', function (e) {
    var t = e.target && e.target.closest && e.target.closest('[data-gd-signup]');
    if (t) return open(e);
    // Links to the long sign-up page open the quick modal instead (email only).
    // Ctrl/Cmd/middle click keep the link (new tab); without JS the link still works.
    var a = e.target && e.target.closest && e.target.closest('a[href^="https://app.godolphy.com/auth/sign-up"]');
    if (a && !e.defaultPrevented && e.button === 0 && !e.metaKey && !e.ctrlKey && !e.shiftKey && !e.altKey) {
      e.preventDefault();
      open(e);
    }
  });
})();
