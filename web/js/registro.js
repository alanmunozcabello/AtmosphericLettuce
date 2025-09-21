// Espera a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
  // Obtiene los elementos del formulario y campos de entrada
  const form   = document.getElementById('register-form');
  const nombre = document.getElementById('nombre');
  const email  = document.getElementById('email');
  const pass   = document.getElementById('password');
  const pass2  = document.getElementById('confirm-password');
  const btn    = document.getElementById('btn-register');

  // Limpia error visual al escribir en cualquier campo
  [nombre, email, pass, pass2].forEach(inp => {
    inp.addEventListener('input', () => inp.classList.remove('invalid'));
  });

  // Evento al enviar el formulario de registro
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Evita el envío tradicional del formulario

    // Quita clases de error previas
    [nombre, email, pass, pass2].forEach(i => i.classList.remove('invalid'));

    let ok = true; // Variable para validar el formulario

    // Obtiene los valores de los campos, eliminando espacios
    const vNombre = nombre.value.trim();
    const vEmail  = email.value.trim();
    const vPass   = pass.value.trim();
    const vPass2  = pass2.value.trim();

    // Validación de nombre: requerido
    if (!vNombre) {
      nombre.classList.add('invalid');
      ok = false;
    }

    // Validación de email: requerido y formato correcto
    if (!vEmail || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(vEmail)) {
      email.classList.add('invalid');
      ok = false;
    }

    // Validación de contraseña: requerida y mínimo 6 caracteres
    if (!vPass || vPass.length < 6) {
      pass.classList.add('invalid');
      ok = false;
      alert('⚠️ La contraseña debe tener al menos 6 caracteres.');
    }

    // Validación de confirmación de contraseña: requerida y debe coincidir
    if (!vPass2 || vPass2 !== vPass) {
      pass2.classList.add('invalid');
      ok = false;
      alert('⚠️ Las contraseñas no coinciden.');
    }

    if (!ok) return; // 🚫 Si hay errores, no seguimos

    // ✅ Estado de carga ON: cambia el texto y agrega clase visual
    btn.textContent = 'Creando cuenta...';
    btn.classList.add('loading');

    // Simula proceso de guardado (solo front, sin backend)
    setTimeout(() => {
      // Guarda usuario en localStorage (ejemplo sencillo)
      const user = { nombre: vNombre, email: vEmail, password: vPass };
      localStorage.setItem('usuarioRegistrado', JSON.stringify(user));

      // 🔄 Estado de carga OFF: restaura el botón
      btn.textContent = 'Registrarme';
      btn.classList.remove('loading');

      // Redirige a login
      window.location.href = 'index.html';
    }, 1200);
  });
});