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
  const lista = document.getElementById('lista-cultivos'); // lista  donde se muestran los cultivos
  const submitBtn = form?.querySelector('button[type="submit"]'); // botón de enviar dentro del form

  // Si alguno de estos elementos no existe muestra error en consola 
  if (!form || !input || !lista) {
    console.error('⚠️ Faltan elementos: form-cultivo / input-cultivo / lista-cultivos');
    return;
  }


  // ---Helper general para peticiones al backend ---
  async function safeFetch(url, options) {
    const res = await fetch(url, options); // hace la petición HTTP
    const text = await res.text().catch(() => '');// intenta leer la respuesta como texto
    if (!res.ok) {                               
      console.error('❌', res.status, res.statusText, text); // muestra error en consola
      throw new Error(`HTTP ${res.status}: ${text || res.statusText}`); // lanza excepción
    }
    try { return JSON.parse(text); } catch { return null; }  // intenta parsear el texto a JSON
  }


  // ---Funciones específicas para cada ruta del backend de los cultvios  ---
  // Obtener los cultivos del usuario
  async function leer() {
    const url = `${API_URL}/${encodeURIComponent(CORREO)}/cultivos`;
    return await safeFetch(url, { method: 'GET' }); // Ejemplo de respuesta: { "tomate": 1, "trigo": 2 }
  }

  // Agregar o modificar un cultivo (PATCH)
  async function agregarOModificar(nombre, hectareasNum) {
    const url = `${API_URL}/${encodeURIComponent(CORREO)}/${encodeURIComponent(nombre)}/${hectareasNum}/agregar_modificar`;
    return await safeFetch(url, { method: 'PATCH' });
  }

  // Eliminar un cultivo
  async function eliminar(nombre) {
    const url = `${API_URL}/${encodeURIComponent(CORREO)}/${encodeURIComponent(nombre)}/eliminar`;
    await safeFetch(url, { method: 'DELETE' });
  }


  // ---Función para mostrar los cultivos en la lista ---
  async function render() {
    lista.innerHTML = '<li>Cargando… ⏳</li>'; // mensaje temporal mientras se carga el cultvo 

    try {
      const cultivos = await leer(); // obtiene los cultivos desde el backend
      const entries = Object.entries(cultivos || {}); // convierte el objeto en lista de pares [nombre, valor]
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

    const nombre = input.value.trim(); // obtiene el texto del input
    if (!nombre) return;               // si está vacío, no hace nada

    const prev = submitBtn?.textContent; // guarda el texto original del botón
    if (submitBtn) { 
      submitBtn.textContent = 'Guardando…'; // muestra mensaje visual
      submitBtn.disabled = true;            // desactiva el botón para evitar doble envío
    }

    try {
      const resp = await agregarOModificar(nombre, 1); // agrega con 1 ha por defecto
      await render(); // vuelve a renderizar la lista actualizada
      if (resp && resp.error) {
        alert(`⚠️ ${resp.error}`);
      }

      input.value = ''; // limpia el campo
      input.focus();    // vuelve a enfocar el input para seguir escribiendo
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
    // Busca si se hizo clic en un botón con clase .btn-eliminar
    const btn = e.target.closest('.btn-eliminar');
    if (!btn) return; 

    const nombre = btn.dataset.nombre; // obtiene el nombre del cultivo desde data-nombre

    try {
      await eliminar(nombre); // llama al backend para eliminar
      await render(); // muestra lista actualizada
    } catch (err) {
      console.error(err);
      alert('⚠️ No se pudo eliminar el cultivo. Revisa la consola.');
    }
  });


  // --- se cargan los cultivos y se muestran en la pagina ---
  render(); // carga y muestra los cultivos automáticamente
});
