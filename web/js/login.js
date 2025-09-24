// login.js (versión corregida para usar GET /usuarios/{correo})
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('login-form');
  const email = document.getElementById('email');
  const pass = document.getElementById('password');
  const btn = document.getElementById('btn-login');
  const toggle = document.getElementById('toggle-pass');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // limpiar estilos previos
    email.classList.remove('invalid');
    pass.classList.remove('invalid');

    let ok = true;
    const validarEmail = email.value.trim();
    const validarContraseña = pass.value.trim();

    if (!validarEmail || !validarEmail.includes("@") || !validarEmail.includes(".")) {
      email.classList.add("invalid");
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

    // estado de carga
    const originalText = btn.textContent;
    btn.textContent = 'Ingresando...';
    btn.classList.add('loading');
    btn.disabled = true;

    try {
      // URL usando la ruta GET que ya tienes: /usuarios/{correo}
      // Si tu backend tiene prefix (/api) o corre en otro puerto, ajusta aquí:
      // const USER_URL = `http://localhost:8000/api/usuarios/${encodeURIComponent(validarEmail)}`;
      const USER_URL = `/usuarios/${encodeURIComponent(validarEmail)}`;

      // IMPORTANTE: GET no lleva body. Solo enviamos headers básicos.
      const resp = await fetch("http://127.0.0.1:8000/usuarios/{correo}", {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      });

      // DEBUG: ver cabeceras y status en consola
      console.log('Request to', USER_URL, 'status:', resp.status);

      if (resp.ok) {
        const user = await resp.json().catch(() => null);
        console.log('Respuesta user:', user);

        if (!user) {
          alert('Respuesta inválida del servidor (no JSON). Revisa la consola.');
          return;
        }

        // Intentamos localizar la contraseña devuelta por el backend.
        // Ajusta los nombres de campo según lo que tu API retorne.
        const serverPassword =
          user.password ?? user.contrasena ?? user.clave ?? user.pass ?? null;

        if (!serverPassword) {
          // El backend no devuelve contraseña en el JSON; no es posible autenticar en cliente.
          alert('El servidor no devuelve la contraseña. No se puede autenticar desde el frontend.');
          console.error('Objeto user recibido sin campo de contraseña:', user);
          return;
        }

        // Si el backend devuelve la contraseña en texto plano (poco seguro), la comparamos.
        if (validarContraseña === serverPassword) {
          // Login OK: guardar datos mínimos y redirigir
          // No guardar contraseña en localStorage
          const userToSave = Object.assign({}, user);
          delete userToSave.password;
          delete userToSave.contrasena;
          delete userToSave.clave;
          delete userToSave.pass;

          localStorage.setItem('user', JSON.stringify(userToSave));
          window.location.href = 'home.html';
          return;
        } else {
          alert('Credenciales inválidas');
          return;
        }
      }

      // Manejo de errores HTTP
      if (resp.status === 404) {
        alert('Usuario no encontrado');
      } else if (resp.status === 401) {
        alert('Credenciales inválidas');
      } else {
        const text = await resp.text().catch(() => '');
        console.error('Error del servidor:', resp.status, text);
        alert('Error con el servidor. Revisa la consola para más detalles.');
      }
    } catch (err) {
      console.error('No se pudo conectar al backend:', err);
      alert('No se pudo conectar al servidor. ¿Está corriendo el backend y permitido el CORS?');
    } finally {
      // restaurar botón
      btn.textContent = originalText;
      btn.classList.remove('loading');
      btn.disabled = false;
    }
  });
});
