document.addEventListener('DOMContentLoaded', () => {
  const CORREO = new URLSearchParams(location.search).get('correo')
    || localStorage.getItem('correoUsuario');

  if (!CORREO) {
    console.warn("⚠️ Usuario no identificado");
    window.location.href = "index.html";
  }
  //commit prueba post actualización
  localStorage.setItem('correoUsuario', CORREO);

  // Referencias a elementos del formulario de login
  const form = document.getElementById('login-form');  // <form> principal
  const email = document.getElementById('email');  // input de correo
  const pass = document.getElementById('password');  // input de contraseña
  const btn = document.getElementById('btn-login'); // botón Ingresar
  const toggle = document.getElementById('toggle-pass');// botón/anchor Mostrar/Ocultar


  // Función helper: quita la clase 'invalid' de un input
  const clearInvalid = (el) => el.classList.remove('invalid');
  // Al escribir en los inputs, limpia el estado de error
  email.addEventListener('input', () => clearInvalid(email));
  pass.addEventListener('input', () => clearInvalid(pass));

  // Manejador del submit del formulario (login)
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); 

    // Limpia cualquier estado de error previo
    email.classList.remove('invalid');
    pass.classList.remove('invalid');

    // Lee valores actuales de los inputs, sin espacios en blanco al inicio y al final 
    const vEmail = email.value.trim();
    const vPass = pass.value.trim();

    // Validaciones front-end 
    let ok = true;
    // Email no vacío y con formato mínimo (contenga @ y .)
    if (!vEmail || !vEmail.includes('@') || !vEmail.includes('.')) { email.classList.add('invalid'); ok = false; }
    // contraseña no vacía
    if (!vPass) { pass.classList.add('invalid'); ok = false; }
    // contraseña con largo mínimo 
    if (vPass.length < 6) { pass.classList.add('invalid'); ok = false; }
    // Si algo falla, no continúa con la petición al backend
    if (!ok) return;

    // Guarda el texto original del botón y setea estado "cargando"
    const originalText = btn.textContent;
    btn.textContent = 'Ingresando...';
    btn.classList.add('loading');
    btn.disabled = true;

    try {
      // Codifica email y pass para usarlos en la URL
      const emailEnc = encodeURIComponent(vEmail);
      const passEnc = encodeURIComponent(vPass);
      // Endpoint de login (método GET con credenciales en la ruta)
      const LOGIN_URL = `/usuarios/iniciar_sesion/${emailEnc}/${passEnc}`;

      // Realiza la petición al backend; pide JSON en la respuesta
      const resp = await fetch(LOGIN_URL, { method: 'GET', headers: { 'Accept': 'application/json' } });
      
      // Si la respuesta HTTP no es OK, maneja distintos códigos
      if (!resp.ok) {
        if (resp.status === 404) { alert('Usuario no encontrado'); }
        else if (resp.status === 401) { alert('Correo o contraseña incorrectos'); }
        else { alert(`Error del servidor: ${resp.status}`); }
        return; // corta aquí si no fue exitoso
      }

      // Lee como texto y luego intenta convertir a formato JSON
      const raw = await resp.text();
      let body = null;
      try { 
        body = JSON.parse(raw); 
      } catch { 
        body = raw; 
      }

      //VER QUE ONDA CON ESTA SECCIÓN MAS TARDE CON CONSOLE.LOG() PARA VER A QUE If ENTRA -> SE HIZO PENSANDO EN 5 RESPUESTAS DISTINTAS DEL BACKEND (SOLO HAY 2!!!!)
      // metodos  para considerar "éxito" según distintos formatos de respuesta
      let success = false;
      if (body === true) success = true; // backend que devuelve booleano
      if (!success && body && typeof body === 'object' && body.success === true) success = true; // { success: true }
      if (!success && body && typeof body === 'object' && typeof body.usuario === 'object') success = true; // { usuario: {...} }
      if (!success && body && typeof body === 'object') {
        // Si tiene claves típicas de un usuario, lo consideramos éxito
        const keys = Object.keys(body).map(k => k.toLowerCase());
        if (keys.includes('correo') || keys.includes('email') || keys.includes('nombre')) {
          success = true;
        }
      }

      // Si ninguna de las condiciones anteriores marcó éxito las credenciales inválidas
      if (!success) {
        alert('Correo o contraseña incorrectos');
        return;
      }

      // En éxito: guarda el correo en localStorage (sesión) y todo el usuario para evitar hacer llamadas innecesarias al backend
      if(success){
        // Guardar datos completos del usuario
        const usuarioCompleto = {
          correo: vEmail,
          nombre: body.nombre || 'Usuario',
          ubicacion: body.ubicacion || {},
          cultivos: body.cultivos || {},
          foto_perfil: body.foto_perfil || ''
        };
        console.log(usuarioCompleto.cultivos);

        localStorage.setItem('correoUsuario', vEmail);
        localStorage.setItem('usuario', JSON.stringify(usuarioCompleto)); // ✅ CACHE COMPLETO
        localStorage.setItem('ultimaActualizacion', Date.now()); // ✅ TIMESTAMP

        window.location.href = `home.html?correo=${encodeURIComponent(vEmail)}`;
      }
      // Limpia los campos del formulario
      email.value = "";
      pass.value = "";

      // Guarda también el correo en window.name (canal simple entre páginas)
      try {
        const wn = JSON.parse(window.name || '{}');
        wn.correo = vEmail;
        window.name = JSON.stringify(wn);
      } catch {
        window.name = JSON.stringify({ correo: vEmail });
      }

      // Restaura visual del botón antes de redirigir
      btn.textContent = originalText;
      btn.classList.remove('loading');
      btn.disabled = false;

      // Redirige a home con el correo en la URL para continuidad
      window.location.href = `home.html?correo=${encodeURIComponent(vEmail)}`;
    } catch (err) {
      // Errores de red/conexión o excepciones no controladas
      console.error('Error de conexión:', err);
      alert('No se pudo conectar con el servidor. Intenta nuevamente.');
    } finally {
      // Siempre restaura el botón a su estado original
      btn.textContent = originalText;
      btn.classList.remove('loading');
      btn.disabled = false;
    }
  });
});
