document.addEventListener('DOMContentLoaded', () => {
  //  Correo desde la URL (home.html?correo=...).
  const params = new URLSearchParams(window.location.search);
  const CORREO = params.get('correo');
  if (!CORREO) {
    alert('⚠️ No se recibió el correo del usuario. Volviendo al login.');
    location.href = 'login.html';
    return;
  }

  // DOM
  const API_URL = 'http://127.0.0.1:8000/usuarios';
  const form = document.getElementById('form-cultivo');
  const input = document.getElementById('input-cultivo');
  const lista = document.getElementById('lista-cultivos');
  const submitBtn = form?.querySelector('button[type="submit"]');

  if (!form || !input || !lista) {
    console.error('⚠️ Faltan elementos: form-cultivo / input-cultivo / lista-cultivos');
    return;
  }

  // Helper fetch con logs
  async function safeFetch(url, options) {
    const res = await fetch(url, options);
    const text = await res.text().catch(() => '');
    if (!res.ok) {
      console.error('❌', res.status, res.statusText, text);
      throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
    }
    try { return JSON.parse(text); } catch { return null; }
  }

  // rutas exactas
  async function leer() {
    const url = `${API_URL}/${encodeURIComponent(CORREO)}/cultivos`;
    return await safeFetch(url, { method: 'GET' }); // { "tomate": 1, ... }
  }
  async function agregarOModificar(nombre, hectareasNum) {
    const url = `${API_URL}/${encodeURIComponent(CORREO)}/${encodeURIComponent(nombre)}/${hectareasNum}/agregar_modificar`;
    return await safeFetch(url, { method: 'PATCH' });
  }
  async function eliminar(nombre) {
    const url = `${API_URL}/${encodeURIComponent(CORREO)}/${encodeURIComponent(nombre)}/eliminar`;
    await safeFetch(url, { method: 'DELETE' });
  }

  // 5) Render
  async function render() {
    lista.innerHTML = '<li>Cargando… ⏳</li>';
    try {
      const cultivos = await leer();
      const entries = Object.entries(cultivos || {});
      lista.innerHTML = '';
      if (entries.length === 0) {
        lista.innerHTML = '<li>No tienes cultivos registrados 🌱</li>';
        return;
      }
      for (const [nombre, hectareas] of entries) {
        const li = document.createElement('li');
        li.className = 'item-cultivo';
        li.innerHTML = `
          <span class="tick">✔</span>
          <span><strong>${nombre}</strong> — ${hectareas} ha</span>
          <button class="btn-eliminar" data-nombre="${nombre}" aria-label="Eliminar ${nombre}">✕</button>
        `;
        lista.appendChild(li);
      }
    } catch (e) {
      console.error(e);
      lista.innerHTML = '<li>Error al cargar cultivos ❌</li>';
    }
  }

  // 6) Agregar (1 ha(hectarea) por defecto)
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); 
    const nombre = input.value.trim();
    if (!nombre) return;

    const prev = submitBtn?.textContent;
    if (submitBtn) { submitBtn.textContent = 'Guardando…'; submitBtn.disabled = true; }

    try {
      await agregarOModificar(nombre, 1); // 1 ha por defecto mas adelante cambiar 
      await render();
      input.value = '';
      input.focus();
    } catch (err) {
      console.error(err);
      alert('⚠️ No se pudo agregar/modificar el cultivo. Revisa la consola.');
    } finally {
      if (submitBtn) { submitBtn.textContent = prev; submitBtn.disabled = false; }
    }
  });

  //  Eliminar
  lista.addEventListener('click', async (e) => {
    const btn = e.target.closest('.btn-eliminar');
    if (!btn) return;
    const nombre = btn.dataset.nombre;
    try {
      await eliminar(nombre);
      await render();
    } catch (err) {
      console.error(err);
      alert('⚠️ No se pudo eliminar el cultivo. Revisa la consola.');
    }
  });

  //  Carga inicial
  render();
});
