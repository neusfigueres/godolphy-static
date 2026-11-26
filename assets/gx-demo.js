/* Godolphy · «Ver demo» (vídeo en ventana) y «Pide una demo con Neus» (formulario → /api/lead, fuente demo-neus).
   Botones: [data-gd-demo="video"] y [data-gd-demo="neus"]. data-sector en el botón = tipo de negocio. */
(function () {
  var d = document, VIDEO = '/videos/godolphy-tour-720.mp4', POSTER = '/videos/godolphy-tour-poster.jpg';
  function track(ev, p) {
    try { if (window.posthog && posthog.capture) posthog.capture(ev, p || {}); } catch (e) {}
    try { if (window.gtag) gtag('event', ev, p || {}); } catch (e) {}
  }
  var css = '.gdm{position:fixed;inset:0;z-index:9999;background:rgba(10,4,30,.78);display:flex;align-items:flex-start;justify-content:center;padding:56px 16px 24px;overflow-y:auto;opacity:0;transition:opacity .25s;}' +
    '.gdm.on{opacity:1;}.gdm-box{position:relative;width:100%;max-width:980px;margin:auto;}' +
    '.gdm-x{position:absolute;top:-44px;right:0;background:none;border:0;color:#fff;font-size:30px;line-height:1;cursor:pointer;padding:4px 8px;}' +
    '.gdm video{display:block;width:100%;border-radius:18px;background:#000;box-shadow:0 30px 80px rgba(0,0,0,.45);}' +
    '.gdm-form{max-width:460px;background:#fff;border-radius:24px;padding:30px 28px;color:#02021e;font-family:inherit;}' +
    '.gdm-form .gdm-x{top:10px;right:10px;color:rgba(2,2,30,.5);}' +
    '.gdm-form h3{font-family:Gabarito,sans-serif;font-size:27px;line-height:1.15;margin:0 0 8px;}' +
    '.gdm-form p{margin:0 0 18px;font-size:15px;line-height:1.55;color:rgba(2,2,30,.65);}' +
    '.gdm-form label{display:block;font-size:13px;font-weight:600;margin:12px 0 5px;}' +
    '.gdm-form input[type=text],.gdm-form input[type=email],.gdm-form input[type=tel]{width:100%;box-sizing:border-box;border:1px solid #ddd6f5;border-radius:12px;padding:12px 14px;font-size:15px;font-family:inherit;}' +
    '.gdm-form input:focus{outline:2px solid #631cff;border-color:transparent;}' +
    '.gdm-ck{display:flex;gap:9px;align-items:flex-start;font-size:12.5px!important;font-weight:400!important;color:rgba(2,2,30,.7);line-height:1.45;}' +
    '.gdm-ck input{margin-top:2px;flex:0 0 auto;}.gdm-ck a{color:#631cff;}' +
    '.gdm-form button[type=submit]{width:100%;margin-top:18px;background:#631cff;color:#fff;border:0;border-radius:999px;padding:14px;font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;}' +
    '.gdm-form button[disabled]{opacity:.6;cursor:wait;}.gdm-err{color:#c62828;font-size:13px;margin-top:10px;min-height:1em;}' +
    '.gdm-ok{text-align:center;padding:10px 0;}.gdm-ok b{display:block;font-family:Gabarito,sans-serif;font-size:24px;margin-bottom:8px;}';
  var st = d.createElement('style'); st.textContent = css; d.head.appendChild(st);

  var modal = null, lastFocus = null;
  function close() {
    if (!modal) return;
    var v = modal.querySelector('video'); if (v) v.pause();
    modal.classList.remove('on');
    var m = modal; modal = null;
    setTimeout(function () { m.remove(); }, 250);
    d.removeEventListener('keydown', onKey);
    d.body.style.overflow = '';
    if (lastFocus) try { lastFocus.focus(); } catch (e) {}
  }
  function onKey(e) { if (e.key === 'Escape') close(); }
  function open(inner, label) {
    close();
    lastFocus = d.activeElement;
    modal = d.createElement('div');
    modal.className = 'gdm'; modal.setAttribute('role', 'dialog'); modal.setAttribute('aria-modal', 'true'); modal.setAttribute('aria-label', label);
    modal.innerHTML = inner;
    modal.addEventListener('click', function (e) { if (e.target === modal || e.target.closest('.gdm-x')) close(); });
    d.body.appendChild(modal); d.body.style.overflow = 'hidden';
    requestAnimationFrame(function () { modal.classList.add('on'); });
    d.addEventListener('keydown', onKey);
    return modal;
  }

  function openVideo(btn) {
    var m = open('<div class="gdm-box"><button class="gdm-x" aria-label="Cerrar">×</button>' +
      '<video src="' + VIDEO + '" poster="' + POSTER + '" controls autoplay playsinline preload="auto"></video></div>', 'Demo de Godolphy en vídeo');
    var v = m.querySelector('video'), sent = {};
    v.addEventListener('play', function () { if (!sent.p) { sent.p = 1; track('lp_demo_video_play', { sector: btn.getAttribute('data-sector') || '' }); } });
    v.addEventListener('ended', function () { track('lp_demo_video_complete', { sector: btn.getAttribute('data-sector') || '' }); });
    track('lp_demo_video_open', { sector: btn.getAttribute('data-sector') || '' });
  }

  function openForm(btn) {
    var sector = btn.getAttribute('data-sector') || '';
    var m = open('<form class="gdm-box gdm-form" novalidate><button type="button" class="gdm-x" aria-label="Cerrar">×</button>' +
      '<h3>Te enseño Godolphy en directo</h3>' +
      '<p>Soy Neus, la fundadora. Te escribo para buscar un día y te lo enseño con tus servicios: por videollamada o, si estás en Barcelona o alrededores, en tu negocio.</p>' +
      '<label for="gdm-n">Nombre</label><input id="gdm-n" type="text" name="nombre" autocomplete="name" required>' +
      '<label for="gdm-e">Email</label><input id="gdm-e" type="email" name="email" autocomplete="email" required>' +
      '<label for="gdm-t">Teléfono</label><input id="gdm-t" type="tel" name="telefono" autocomplete="tel" required>' +
      '<label for="gdm-b">Nombre de tu negocio</label><input id="gdm-b" type="text" name="nombre_negocio" autocomplete="organization">' +
      '<label class="gdm-ck"><input type="checkbox" name="privacy" required> <span>He leído y acepto la <a href="/politica-de-privacidad/" target="_blank" rel="noopener">política de privacidad</a>.</span></label>' +
      '<label class="gdm-ck"><input type="checkbox" name="mkt"> <span>Quiero recibir novedades y consejos de Godolphy por email (opcional).</span></label>' +
      '<button type="submit">Pedir mi demo</button><div class="gdm-err" aria-live="polite"></div></form>', 'Pide una demo con Neus');
    var f = m.querySelector('form'), err = f.querySelector('.gdm-err'), b = f.querySelector('button[type=submit]');
    setTimeout(function () { f.nombre.focus(); }, 50);
    track('lp_demo_form_open', { sector: sector });
    f.addEventListener('submit', function (e) {
      e.preventDefault(); err.textContent = '';
      var nombre = f.nombre.value.trim(), email = f.email.value.trim(), tel = f.telefono.value.trim();
      if (!nombre) { err.textContent = 'Escribe tu nombre.'; return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { err.textContent = 'Revisa el email.'; return; }
      if (tel.replace(/\D/g, '').length < 9) { err.textContent = 'Revisa el teléfono.'; return; }
      if (!f.privacy.checked) { err.textContent = 'Tienes que aceptar la política de privacidad.'; return; }
      b.disabled = true; b.textContent = 'Enviando…';
      fetch('/api/lead', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source: 'demo-neus', nombre: nombre, email: email, telefono: tel, nombre_negocio: f.nombre_negocio.value.trim(),
          tipo_negocio: sector, privacy_accepted: true, marketing_consent: f.mkt.checked }) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (x) {
          if (!x.ok || !x.j || x.j.saved === false) throw new Error('save');
          track('lp_demo_requested', { sector: sector });
          try { if (window.fbq) fbq('track', 'Lead', { content_name: 'demo-neus' }); } catch (e2) {}
          f.innerHTML = '<button type="button" class="gdm-x" aria-label="Cerrar">×</button><div class="gdm-ok"><b>¡Hecho, ' + nombre.replace(/[<>&"]/g, '') + '!</b><p>Te escribiré para buscar un día. Mientras tanto, puedes probar Godolphy gratis 30 días.</p>' +
            '<a href="https://app.godolphy.com/auth/sign-up" style="display:inline-block;background:#631cff;color:#fff;font-weight:700;border-radius:999px;padding:13px 24px;text-decoration:none;">Prueba gratis 30 días</a></div>';
        })
        .catch(function () {
          b.disabled = false; b.textContent = 'Pedir mi demo';
          err.innerHTML = 'No se ha podido enviar. Escríbeme a <a href="mailto:neus@godolphy.com">neus@godolphy.com</a> y lo vemos.';
          track('lp_demo_request_failed', { sector: sector });
        });
    });
  }

  d.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('[data-gd-demo]');
    if (!btn) return;
    e.preventDefault();
    if (btn.getAttribute('data-gd-demo') === 'video') openVideo(btn); else openForm(btn);
  });
})();
