
document.addEventListener('DOMContentLoaded', () => {
  const CORREO = new URLSearchParams(location.search).get('correo') 
              || localStorage.getItem('correoUsuario');

  if (!CORREO) {
    console.warn("⚠️ Usuario no identificado");
    window.location.href = "login.html";
  }

  localStorage.setItem('correoUsuario', CORREO);

  const form   = document.getElementById('login-form');
  const email  = document.getElementById('email');
  const pass   = document.getElementById('password');
  const btn    = document.getElementById('btn-login');
  const toggle = document.getElementById('toggle-pass');

  if (toggle) {
    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      if (pass.type === 'password') {
        pass.type = 'text';
        toggle.textContent = 'Ocultar';
      } else {
        pass.type = 'password';
        toggle.textContent = 'Mostrar';
      }
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    email.classList.remove('invalid');
    pass.classList.remove('invalid');

    const vEmail = email.value.trim();
    const vPass  = pass.value.trim();

    let ok = true;
    if (!vEmail || !vEmail.includes('@') || !vEmail.includes('.')) { email.classList.add('invalid'); ok = false; }
    if (!vPass) { pass.classList.add('invalid'); ok = false; }
    if (vPass.length < 6) { pass.classList.add('invalid'); ok = false; alert('La contraseña debe contener al menos 6 dígitos.'); }
    if (!ok) return;

    const originalText = btn.textContent;
    btn.textContent = 'Ingresando...';
    btn.classList.add('loading');
    btn.disabled = true;

    try {
      const emailEnc = encodeURIComponent(vEmail);
      const passEnc  = encodeURIComponent(vPass);
      const LOGIN_URL = `http://127.0.0.1:8000/usuarios/iniciar_sesion/${emailEnc}/${passEnc}`;

      const resp = await fetch(LOGIN_URL, { method: 'GET', headers: { 'Accept': 'application/json' } });

      // Leer siempre como texto y luego intentar JSON
      const raw  = await resp.text();
      let body   = null;
      try { body = JSON.parse(raw); } catch { body = raw; }

      console.log('status', resp.status, 'body:', body);

      if (!resp.ok) {
        if (resp.status === 404) { alert('Usuario no encontrado'); }
        else if (resp.status === 401) { alert('Correo o contraseña incorrectos'); }
        else { alert(`Error del servidor: ${resp.status}`); }
        return;
      }

      let success = false;
      if (body === true) success = true;
      if (!success && body && typeof body === 'object' && body.success === true) success = true;
      if (!success && body && typeof body === 'object' && typeof body.usuario === 'object') success = true;
      if (!success && body && typeof body === 'object') {
        const keys = Object.keys(body).map(k => k.toLowerCase());
        if (keys.includes('correo') || keys.includes('email') || keys.includes('nombre')) {
          success = true;
        }
      }

      if (!success) {
        alert('Correo o contraseña incorrectos');
        return;
      }
      localStorage.setItem('correoUsuario', vEmail);
      try {
        const wn = JSON.parse(window.name || '{}');
        wn.correo = vEmail;
        window.name = JSON.stringify(wn);
      } catch {
        window.name = JSON.stringify({ correo: vEmail });
      }

      btn.textContent = originalText;
      btn.classList.remove('loading');
      btn.disabled = false;

      window.location.href = `home.html?correo=${encodeURIComponent(vEmail)}`;
    } catch (err) {
      console.error('Error de conexión:', err);
      alert('No se pudo conectar con el servidor. Intenta nuevamente.');
    } finally {
      btn.textContent = originalText;
      btn.classList.remove('loading');
      btn.disabled = false;
    }
  });
});

