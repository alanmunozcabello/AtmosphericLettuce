// Espera a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
  // busca el correo en la url o en localStorage
  const CORREO = new URLSearchParams(location.search).get('correo')
    || localStorage.getItem('correoUsuario');

  if (!CORREO) {
    console.warn("⚠️ Usuario no identificado");
    window.location.href = "index.html"; 
  }

  
  localStorage.setItem('correoUsuario', CORREO);


  // --- Referencias al DOM ---
  const API_URL = 'http://127.0.0.1:8000/usuarios'; // Base del backend
  const form = document.getElementById('form-cultivo'); // formulario de agregar cultivo
  const input = document.getElementById('input-cultivo'); // input donde el usuario escribe el cultivo
  const inputHectareas = document.getElementById('input-hectareas'); // input de las hectareas
  const lista = document.getElementById('lista-cultivos'); // lista  donde se muestran los cultivos
  const submitBtn = form?.querySelector('button[type="submit"]'); // botón de enviar dentro del form

  // Si alguno de estos elementos no existe muestra error en consola 
  if (!form || !input || !inputHectareas || !lista) {
    console.error('⚠️ Faltan elementos: form-cultivo / input-cultivo / input-hectareas / lista-cultivos');
    return;
  }

  // Agregar o modificar un cultivo (PATCH)
  async function agregarOModificar(nombre, hectareasNum) {
    const res = await fetch(`${API_URL}/${encodeURIComponent(CORREO)}/${encodeURIComponent(nombre)}/${hectareasNum}/agregar_modificar`, {method: 'PATCH'}); // hace la petición HTTP
    const text = await res.text().catch(() => '');// intenta leer la respuesta como texto

    if (!res.ok) { //si algo salió mal muestra error por ahora -> cambiar a que mande una alerta                        
      console.error('❌', res.status, res.statusText, text);
      throw new Error(`HTTP ${res.status}: ${text || res.statusText}`); // lanza excepción
      //return;
    }

    try { 
      return JSON.parse(text); //parsea la respuesta
    } catch { 
      return null; 
    }

  }

  // Eliminar un cultivo
  async function eliminar(nombre) {
    const res = await fetch(`${API_URL}/${encodeURIComponent(CORREO)}/${encodeURIComponent(nombre)}/eliminar`, {method: 'DELETE'}); // hace la petición HTTP
    const text = await res.text().catch(() => '');// intenta leer la respuesta como texto

    if (!res.ok) { //si algo salió mal muestra error por ahora -> cambiar a que mande una alerta                        
      console.error('❌', res.status, res.statusText, text);
      throw new Error(`HTTP ${res.status}: ${text || res.statusText}`); // lanza excepción
      //return;
    }

    try { 
      return JSON.parse(text); //parsea la respuesta
    } catch { 
      return null; 
    }

  }


  // ---Función para mostrar los cultivos en la lista ---
  async function render() {
    lista.innerHTML = '<li>Cargando… ⏳</li>'; // mensaje temporal mientras se carga el cultvo 

    try {
      const usuario = await obtenerUsuario(CORREO); // obtener todo el usuario

      const cultivos = usuario.cultivos || {}; // quedarse solo con los cultivos del usuario
      const entries = Object.entries(cultivos); // convierte el objeto en lista de pares [nombre, valor]
      lista.innerHTML = ''; // limpia la lista anterior

      // Si no hay cultivos, muestra un mensaje vacío para que no se vea tan pela la zona 
      if (entries.length === 0) {
        lista.innerHTML = '<li>No tienes cultivos registrados 🌱</li>';
        return;
      }

      // Recorre cada cultivo y crea una  lista con su nombre y hectáreas
      for (const [nombre, hectareas] of entries) {
        const li = document.createElement('li');
        li.className = 'item-cultivo';
        li.innerHTML = `
          <span class="tick">✔</span>
          <span><strong>${nombre}</strong> — ${hectareas} ha</span>
          <button class="btn-eliminar" data-nombre="${nombre}" aria-label="Eliminar ${nombre}">✕</button>
        `;
        lista.appendChild(li); // añade el <li> a la lista
      }
    } catch (e) {
      console.error(e);
      lista.innerHTML = '<li>Error al cargar cultivos ❌</li>'; // muestra error si algo falla
    }
  }


  // ---Evento: agregar o modificar cultivo ---
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); // evita que se recargue la página

    const nombre = input.value.trim(); //obtener input texto
    const hectareas = parseInt(inputHectareas.value); //obtener input hectareas

    if(!nombre){ // si está vacío, no hace nada
      input.focus();
      alert("Ingrese un nombre valido");
      return;
    }
    if(!hectareas || hectareas < 1 || hectareas > 100000){ // si está vacío o está bajo 1 o sobre 100 mil hectareas no hace nada
      inputHectareas.focus();
      inputHectareas.value = '';
      alert("Ingrese una cantidad razonable de hectareas");
      return;
    }

    const prev = submitBtn?.textContent; // guarda el texto original del botón
    if (submitBtn) { 
      submitBtn.textContent = 'Guardando…'; // muestra mensaje visual
      submitBtn.disabled = true;            // desactiva el botón para evitar doble envío
    }

    try {
      const resp = await agregarOModificar(nombre, hectareas); // agrega con 1 ha por defecto
      if (resp && resp.error) {
        alert(`⚠️ ${resp.error}`);
      }else{

        const usuarioActual = JSON.parse(localStorage.getItem('usuario') || '{}');

        actualizarCacheUsuario({
          cultivos: {...usuarioActual.cultivos, //mantener los cultivos que se tenian
          [nombre]: hectareas //agregar o modificar otros
          }
        });
      }

      await render(); // vuelve a renderizar la lista actualizada

      input.value = ''; // limpia el campo
      inputHectareas.value = '';
      input.focus();    // vuelve a enfocar el input para seguir escribiendo
      inputHectareas.focus();

    } catch (err) {
      console.error(err);
      alert('⚠️ No se pudo agregar/modificar el cultivo. Revisa la consola.');
    } finally {
      // restaura el botón
      if (submitBtn) { 
        submitBtn.textContent = prev;
        submitBtn.disabled = false; 
      }
    }
  });


  // ---Evento: eliminar cultivo ---
  lista.addEventListener('click', async (e) => {
    // Busca si se hizo click en un botón con clase .btn-eliminar
    const btn = e.target.closest('.btn-eliminar');
    if (!btn) return; 

    const nombre = btn.dataset.nombre; // obtiene el nombre del cultivo desde data-nombre

    try {
      await eliminar(nombre); // llama al backend para eliminar

      //actualizar el local storage
      const usuarioActual = JSON.parse(localStorage.getItem('usuario') || '{}');
      const cultivosActualizados = { ...usuarioActual.cultivos };
      delete cultivosActualizados[nombre];
      
      actualizarCacheUsuario({
        cultivos: cultivosActualizados
      });

      await render(); // muestra lista actualizada

    } catch (err) {
      console.error(err);
      alert('⚠️ No se pudo eliminar el cultivo. Revisa la consola.');
    }
  });

  if (window.location.pathname.includes('home.html')) {
      // Solo cargar clima si estamos en home.html
      setTimeout(() => {
        if (typeof cargarClimaHome === 'function') {
          cargarClimaHome();
        }
      }, 1500); // mientras tanto será un tiempo fijo
    }

  // --- se cargan los cultivos y se muestran en la pagina ---
  render(); // carga y muestra los cultivos automáticamente
});
