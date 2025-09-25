document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const email = document.getElementById('email');
  const pass = document.getElementById('password');
  const btn = document.getElementById('btn-login');
  const toggle = document.getElementById('toggle-pass');

  // Toggle mostrar / ocultar contraseña (si tienes un botón con id="toggle-pass")
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

    // limpiar estilos previos
    email.classList.remove('invalid');
    pass.classList.remove('invalid');

    let ok = true;
    const validarEmail = email.value.trim();
    const validarContraseña = pass.value.trim();

    // Validaciones básicas
    if (!validarEmail || !validarEmail.includes('@') || !validarEmail.includes('.')) {
      email.classList.add('invalid');
      ok = false;
    }
    if (!validarContraseña) {
      pass.classList.add('invalid');
      ok = false;
    }
    if (validarContraseña.length < 6) {
      pass.classList.add('invalid');
      ok = false;
      alert('La contraseña debe contener al menos 6 dígitos.');
    }
    if (!ok) return;

    // estado de carga (guardamos texto original para restaurar)
    const originalText = btn.textContent;
    btn.textContent = 'Ingresando...';
    btn.classList.add('loading');
    btn.disabled = true;

    try {
      // Construir URL correctamente (ajusta host/puerto/prefix si hace falta)
      const emailEncoded = encodeURIComponent(validarEmail);
      const USER_URL = `http://127.0.0.1:8000/usuarios/${emailEncoded}`;-+
      
      console.log('Fetching ->', USER_URL);

      const resp = await fetch(USER_URL, {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      });

      console.log('resp.url', resp.url, 'status', resp.status, 'content-type:', resp.headers.get('content-type'));

      // Leer la respuesta de forma segura
      let body = null;
      const contentType = resp.headers.get('content-type') || '';
      if (contentType.includes('application/json')) {
        try {
          body = await resp.json();
        } catch (errJson) {
          console.warn('Falló parseo JSON aunque content-type indica JSON:', errJson);
          body = await resp.text().catch(() => null);
          console.log('Response text (fallback):', body);
          throw new Error('Respuesta del servidor no pudo ser parseada como JSON');
        }
      } else {
        body = await resp.text().catch(() => null);
        console.log('Response text:', body);
      }

      // Manejo según status y contenido
      if (resp.ok) {
        // Si el backend devuelve un objeto con detail/error aun cuando status 200, tratarlo como error lógico
        if (body && (body.detail || body.error)) {
          console.error('Backend devolvió detalle de error dentro de 200:', body);
          alert(body.detail || body.error || 'Error del servidor');
        } else {
          // Usuario encontrado -> guardar datos seguros y redirigir
          console.log('Usuario recibido:', body);

          // No guardar contraseñas en localStorage. Guardar sólo datos no sensibles.
          const usuarioSeguro = { ...body };
          delete usuarioSeguro.password;
          delete usuarioSeguro.contrasena;
          delete usuarioSeguro.clave;
          delete usuarioSeguro.pass;

          localStorage.setItem('usuario', JSON.stringify(usuarioSeguro));

          // Restaurar botón antes de redirigir
          btn.textContent = originalText;
          btn.classList.remove('loading');
          btn.disabled = false;

          // Redirigir a home
          window.location.href = 'home.html';
          return;
        }
      } else if (resp.status === 404) {
        alert('Usuario no encontrado (404)');
      } else if (resp.status === 401) {
        alert('Credenciales inválidas (401)');
      } else {
        console.error('Error HTTP', resp.status, body);
        alert(`Error del servidor: ${resp.status}`);
      }
    } catch (error) {
      console.error('Error en fetch/parse:', error);
      alert('No se pudo conectar con el servidor o la respuesta no es válida. Revisa la consola.');
    } finally {
      // restaurar botón siempre
      btn.textContent = originalText;
      btn.classList.remove('loading');
      btn.disabled = false;
    }
  });
});
