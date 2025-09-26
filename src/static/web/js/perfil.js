// Espera a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
  const CORREO = window.CORREO_ACTUAL || new URLSearchParams(location.search).get('correo');
  if (!CORREO) { console.warn('Sin correo; omito llamadas a la API.'); return; }
  const LS_KEY = 'perfilAL'; // Clave para localStorage del perfil

  // Referencias a elementos de la vista (mostrar datos)
  const nombreV = document.querySelector('.nombre');
  const desdeV = document.querySelector('.desde');
  const filas = document.querySelectorAll('.tarjeta-perfil .fila');
  const correoV = filas[0]?.querySelector('.valor'); // 1ª fila = Correo
  const ubicV = filas[1]?.querySelector('.valor'); // 2ª fila = Ubicación
  const regionV = filas[2]?.querySelector('.valor'); // 3ª fila = Idioma
  const avatarV = document.querySelector('.avatar-fondo img');

  // Referencias al formulario de edición
  const form = document.getElementById('form-perfil');
  const inpNombre = document.getElementById('inp-nombre');
  const inpCorreo = document.getElementById('inp-correo');
  const inpUbic = document.getElementById('inp-ubicacion');
  const inpRegion = document.getElementById('inp-region');
  const inpAvatar = document.getElementById('inp-avatar');

  // Botones de la interfaz
  const btnEditar = document.getElementById('btn-editar');
  const btnGuardar = document.getElementById('btn-guardar');
  const btnCancelar = document.getElementById('btn-cancelar');

  // Función para leer el perfil desde localStorage
  const leer = () => JSON.parse(localStorage.getItem(LS_KEY) || 'null');
  // Función para guardar el perfil en localStorage
  const guardar = (obj) => localStorage.setItem(LS_KEY, JSON.stringify(obj));

  // Carga inicial de datos (si no hay datos, usa los del HTML)
  function cargar() {
    const data = leer() || {
      nombre: nombreV?.textContent?.trim() || 'Usuario',
      correo: correoV?.textContent?.trim() || '',
      ubic: ubicV?.textContent?.trim() || '',
      region: regionV?.textContent?.trim() || 'Maule',
      avatar: null // dataURL si el usuario sube uno
    };

    // Rellena la vista con los datos
    if (nombreV) nombreV.textContent = data.nombre;
    if (correoV) correoV.textContent = data.correo;
    if (ubicV) ubicV.textContent = data.ubic;
    if (regionV) regionV.textContent = data.region;
    if (avatarV && data.avatar) avatarV.src = data.avatar;

    // Rellena el formulario de edición con los datos
    inpNombre.value = data.nombre;
    inpCorreo.value = data.correo;
    inpUbic.value = data.ubic;
    inpRegion.value = data.region;
  }

  // Cambia entre modo edición y modo vista
  function modoEdicion(on) {
    form.style.display = on ? 'block' : 'none';
    btnGuardar.style.display = on ? 'inline-block' : 'none';
    btnCancelar.style.display = on ? 'inline-block' : 'none';
    btnEditar.style.display = on ? 'none' : 'inline-block';
  }

  // Evento para activar modo edición
  btnEditar.addEventListener('click', () => {
    cargar();     // Sincroniza datos por si cambiaron
    modoEdicion(true);
    inpNombre.focus();
  });

  // Evento para cancelar edición y volver a la vista normal
  btnCancelar.addEventListener('click', () => {
    modoEdicion(false);
  });

  // Evento para guardar los cambios del perfil
  btnGuardar.addEventListener('click', (e) => {
    e.preventDefault();

    let valido = true;

    // Quita estado de error previo
    inpNombre.classList.remove("invalid");
    inpCorreo.classList.remove("invalid");

    // Validar nombre (requerido)
    const nombre = inpNombre.value.trim();
    if (!nombre) {
      inpNombre.classList.add("invalid");
      valido = false;
    }

    // Validar correo (requerido y formato)
    const correo = inpCorreo.value.trim();
    if (!correo || !correo.includes("@") || !correo.includes(".")) {
      inpCorreo.classList.add("invalid");
      valido = false;
    }

    if (!valido) {
      return; // No sigue hasta que corrijan errores
    }

    // Estado de carga ON
    btnGuardar.textContent = "Guardando...";
    btnGuardar.classList.add("loading");

    // Simulación de guardado (1.5 segundos)
    setTimeout(() => {
      // Construye el objeto con los datos del formulario
      const data = {
        nombre,
        correo,
        ubic: inpUbic.value.trim(),
        region: inpRegion.value.trim() || "Español",
        avatar: avatarV?.src?.startsWith("data:") ? avatarV.src : (leer()?.avatar || null),
      };

      guardar(data);      // Guarda en localStorage
      cargar();           // Actualiza la vista
      modoEdicion(false); // Sale del modo edición

      // Estado de carga OFF
      btnGuardar.textContent = "Guardar";
      btnGuardar.classList.remove("loading");
    }, 1500);
  });

  // Evento para subir y previsualizar el avatar (imagen de perfil)
  inpAvatar?.addEventListener('change', () => {
    const file = inpAvatar.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      avatarV.src = reader.result; // dataURL
    };
    reader.readAsDataURL(file);
  });

  cargar(); // Carga los datos al iniciar la página
});
