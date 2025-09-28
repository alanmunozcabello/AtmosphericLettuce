document.addEventListener('DOMContentLoaded', () => {
    const CORREO = new URLSearchParams(location.search).get('correo') 
               || localStorage.getItem('correoUsuario');

  if (!CORREO) {
    console.warn("⚠️ Usuario no identificado");
    // opcional → redirigir al login:
    window.location.href = "login.html";
  }

  // aseguramos que siempre esté en localStorage
  localStorage.setItem('correoUsuario', CORREO);
  
  const form   = document.getElementById('register-form');
  const nombre = document.getElementById('nombre');
  const email  = document.getElementById('email');
  const pass   = document.getElementById('password');
  const pass2  = document.getElementById('confirm-password');
  const btn    = document.getElementById('btn-register');

  [nombre, email, pass, pass2].forEach(inp => {
    inp.addEventListener('input', () => inp.classList.remove('invalid'));
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    [nombre, email, pass, pass2].forEach(i => i.classList.remove('invalid'));

    let ok = true;
    const vNombre = nombre.value.trim();
    const vEmail  = email.value.trim();
    const vPass   = pass.value.trim();
    const vPass2  = pass2.value.trim();

    if (!vNombre) { nombre.classList.add('invalid'); ok = false; }
    if (!vEmail || !vEmail.includes("@") || !vEmail.includes(".")) { email.classList.add("invalid"); ok = false; }
    if (!vPass || vPass.length < 6) { pass.classList.add('invalid'); ok = false; alert('La contraseña debe tener al menos 6 caracteres.'); }
    if (!vPass2 || vPass2 !== vPass) { pass2.classList.add('invalid'); ok = false; alert('Las contraseñas no coinciden.'); }
    if (!ok) return;

    const originalText = btn.textContent;
    btn.textContent = 'Creando cuenta...';
    btn.classList.add('loading');
    btn.disabled = true;

    try {
      const REGISTER_URL = 'http://127.0.0.1:8000/usuarios/registrar';

      const resp = await fetch(REGISTER_URL, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          correo: vEmail,
          nombre: vNombre,
          contrasena: vPass
        })
      });

      let body = null;
      const contentType = resp.headers.get('content-type') || '';
      if (contentType.includes('application/json')) {
        body = await resp.json();
      } else {
        body = await resp.text();
      }

      if (resp.ok) {
        if (body && (body.detail || body.error)) {
          alert(body.detail || body.error || 'Error del servidor');
        } else {
          console.log('Usuario registrado:', body);
          alert('Cuenta creada correctamente');
          window.location.href = 'index.html';
        }
      } else if (resp.status === 400) {
        alert('Error: datos inválidos o usuario ya existe');
      } else {
        alert(`Error del servidor: ${resp.status}`);
        console.error(body);
      }

    } catch (error) {
      console.error('Error al conectar con el servidor:', error);
      alert('No se pudo conectar con el servidor. Revisa la consola.');
    } finally {
      btn.textContent = originalText;
      btn.classList.remove('loading');
      btn.disabled = false;
    }
  });
});
