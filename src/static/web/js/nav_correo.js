document.addEventListener('DOMContentLoaded', () => {
  // --- Resolver correo desde URL, window.name o (último recurso) del DOM del perfil ---
  function resolveCorreo() {
    // 1) URL ?correo=
    let c = new URLSearchParams(location.search).get('correo');
    if (c) return c;

    // 2) window.name (persistente por pestaña)
    try { c = JSON.parse(window.name || '{}')?.correo || null; } catch { c = null; }
    if (c) return c;

    // 3) Del DOM del perfil (si estás ahí y lo muestras en pantalla)
    const el = document.querySelector('.tarjeta-perfil .fila .valor');
    if (el) {
      const t = el.textContent.trim();
      if (t.includes('@')) return t;
    }
    return null;
  }

  function saveCorreo(c) {
    if (!c) return;
    try {
      const o = JSON.parse(window.name || '{}') || {};
      o.correo = c;
      window.name = JSON.stringify(o);
    } catch {
      window.name = JSON.stringify({ correo: c });
    }
  }

  function go(href, c) {
    if (!href) return;
    if (!c) { window.location.href = 'login.html'; return; }
    const u = new URL(href, location.origin);
    u.searchParams.set('correo', c);
    window.location.href = u.pathname + u.search + u.hash;
  }

  const correo = resolveCorreo();
  if (correo) saveCorreo(correo); // si lo trajiste por URL/DOM, déjalo guardado en la pestaña

  // --- Logo → Home con correo ---
  const btnLogo = document.getElementById('btn-logo') || document.querySelector('.logo a');
  if (btnLogo) {
    btnLogo.addEventListener('click', (e) => {
      e.preventDefault();
      const c = resolveCorreo() || correo;
      saveCorreo(c);
      go('home.html', c);
    });
  }

  // --- Usuario → Perfil con correo ---
  const btnUsuario = document.getElementById('btn-usuario');
  if (btnUsuario) {
    btnUsuario.addEventListener('click', (e) => {
      e.preventDefault();
      const c = resolveCorreo() || correo;
      saveCorreo(c);
      go('perfil.html', c);
    });
  }
});
