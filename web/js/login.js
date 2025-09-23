// Espera a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
  // Obtiene los elementos del formulario y campos de entrada
  const form = document.getElementById('login-form');
  const email = document.getElementById('email');
  const pass = document.getElementById('password');
  const btn = document.getElementById('btn-login');
  const toggle = document.getElementById('toggle-pass');

  // Evento para mostrar/ocultar la contraseña al hacer clic en el icono (opcional)
  toggle?.addEventListener('click', () => {
    const isPwd = pass.type === 'password'; // Verifica si el tipo es password
    pass.type = isPwd ? 'text' : 'password'; // Cambia el tipo de input
    toggle.textContent = isPwd ? '🙈' : '👁️'; 
    pass.focus(); // Enfoca el campo de contraseña
  });

  // Evento al enviar el formulario de login
  form.addEventListener('submit', (e) => {
    e.preventDefault(); // Evita el envío tradicional del formulario

    // Quita clases de error previas
    email.classList.remove('invalid');
    pass.classList.remove('invalid');

    let ok = true; // Variable para validar el formulario

    const valEmail = email.value.trim(); // Valor del email sin espacios
    const valPass = pass.value.trim();  // Valor de la contraseña sin espacios

    // Validación de email: requerido y formato correcto
    if (!valEmail || !valEmail.includes("@") || !valEmail.includes(".")) {
      email.classList.add("invalid"); // Marca el campo como inválido
      ok = false;
    }

    // Validación de contraseña: requerida
    if (!valPass) {
      pass.classList.add('invalid'); // Marca el campo como inválido
      ok = false;
    }

     if (valPass.length < 6) {
      pass.classList.add('invalid');
      ok = false;
      alert('La contraseña debe contener al menos 6 dígitos.');

    }

    if (!ok) return; // Si hay errores, no continúa

    // Estado de carga: cambia el texto y agrega clase visual
    btn.textContent = 'Ingresando...';
    btn.classList.add('loading');

    // Simula proceso de login (aquí iría la llamada real al servidor en nuestro caso cuando conectemos con backend)
    setTimeout(() => {
      // Estado de carga OFF: restaura el botón
      btn.textContent = 'Iniciar Sesión';
      btn.classList.remove('loading');

      // Redirección si todo está correcto
      window.location.href = 'home.html';
    }, 1200);
  });
});