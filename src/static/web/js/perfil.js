// perfil.js (con persistencia en backend de nombre/correo)
document.addEventListener('DOMContentLoaded', () => {
  const API_BASE = 'http://localhost:8000'; // ajusta host/puerto
  const LS_KEY = 'perfilAL';

  // --- utilidades ---
  const replaceCorreoInURL = (nuevoCorreo) => {
    try {
      const url = new URL(location.href);
      url.searchParams.set('correo', nuevoCorreo);
      history.replaceState(null, '', url.toString());
    } catch { /* noop */ }
  };

  // Sustituye tu putUsuario por esta versión que envía usuarioMOD como query param
  const putUsuario = async (correoActual, body) => {
    const url = new URL(`${API_BASE}/usuarios/${encodeURIComponent(correoActual)}/modificar`);
    url.searchParams.set('usuarioMOD', JSON.stringify(body)); // <-- clave: va en la query

    const res = await fetch(url.toString(), { method: 'PUT' }); // sin body
    let text = '';
    try { text = await res.text(); } catch { }
    if (!res.ok) throw new Error(`PUT fallo: ${res.status} ${res.statusText} ${text}`);
    try { return JSON.parse(text || '{}'); } catch { return {}; }
  };


  // --- resolver correo actual ---
  const CORREO =
    new URLSearchParams(location.search).get('correo') ||
    localStorage.getItem('correoUsuario') ||
    '';

  if (!CORREO) {
    console.warn('⚠️ Usuario no identificado');
    window.location.href = 'index.html';
    return;
  }
  localStorage.setItem('correoUsuario', CORREO);

  // --- refs vista/form ---
  const nombreV = document.querySelector('.nombre');
  const filas = document.querySelectorAll('.tarjeta-perfil .fila');
  const correoV = filas[0]?.querySelector('.valor');
  const ubicV = filas[1]?.querySelector('.valor');
  const regionV = filas[2]?.querySelector('.valor');
  const avatarV = document.querySelector('.avatar-fondo img');

  const form = document.getElementById('form-perfil');
  const inpNombre = document.getElementById('inp-nombre');
  const inpCorreo = document.getElementById('inp-correo');
  const inpUbic = document.getElementById('inp-ubicacion');
  const inpRegion = document.getElementById('inp-region');
  const inpAvatar = document.getElementById('inp-avatar');

  const btnEditar = document.getElementById('btn-editar');
  const btnGuardar = document.getElementById('btn-guardar');
  const btnCancelar = document.getElementById('btn-cancelar');

  // --- LS helpers ---
  const leerLS = () => {
    try { return JSON.parse(localStorage.getItem(LS_KEY) || 'null'); }
    catch { return null; }
  };
  const guardarLS = (obj) => localStorage.setItem(LS_KEY, JSON.stringify(obj));

  // --- pintar ---
  function pintar(data) {
    if (nombreV) nombreV.textContent = data.nombre ?? 'Usuario';
    if (correoV) correoV.textContent = data.correo ?? '';
    if (ubicV) ubicV.textContent = data.ubic ?? 'No especificada';
    if (regionV) regionV.textContent = data.region ?? 'No especificada';
    if (avatarV && data.avatar) avatarV.src = data.avatar;

    if (inpNombre) inpNombre.value = data.nombre ?? 'Usuario';
    if (inpCorreo) inpCorreo.value = data.correo ?? CORREO;
    if (inpUbic) inpUbic.value = data.ubic ?? '';
    if (inpRegion) inpRegion.value = data.region ?? '';
  }

  function cargarInicial() {
    const cached = leerLS();
    const base = cached || {
      nombre: (nombreV?.textContent || 'Usuario').trim(),
      correo: (correoV?.textContent?.trim()) || CORREO,
      ubic: (ubicV?.textContent || '').trim(),
      region: (regionV?.textContent || '').trim(),
      avatar: null,
    };
    guardarLS(base);
    pintar(base);
  }

  async function syncConBackend() {
    try {
      const res = await fetch(`${API_BASE}/usuarios/${encodeURIComponent(CORREO)}`);
      if (!res.ok) return;

      const usuario = await res.json();
      const previo = leerLS() || {};

      // Si el backend manda un "nombre" que es un email, lo tratamos como no-nombre
      const nombreSrv = (usuario?.nombre ?? '').trim();
      const esEmail = nombreSrv.includes('@');
      const displayName = esEmail
        ? (previo.nombre && !previo.nombre.includes('@') ? previo.nombre : (CORREO.split('@')[0] || 'Usuario'))
        : (nombreSrv || previo.nombre || 'Usuario');

      const fusionado = {
        ...previo,
        nombre: displayName,
        correo: usuario?.correo ?? CORREO,
        // Obtener ciudad y región del backend
        ubic: usuario?.ubicacion?.ciudad ?? previo.ubic ?? '',
        region: usuario?.ubicacion?.region ?? previo.region ?? '',
        avatar: previo.avatar ?? null,
      };

      guardarLS(fusionado);
      pintar(fusionado);
    } catch (e) {
      console.warn('No se pudo sincronizar perfil:', e);
    }
  }

  function modoEdicion(on) {
    if (form) form.style.display = on ? 'block' : 'none';
    if (btnGuardar) btnGuardar.style.display = on ? 'inline-block' : 'none';
    if (btnCancelar) btnCancelar.style.display = on ? 'inline-block' : 'none';
    if (btnEditar) btnEditar.style.display = on ? 'none' : 'inline-block';
  }

  btnEditar?.addEventListener('click', () => {
    const data = leerLS() || {};
    pintar(data);
    modoEdicion(true);
    inpNombre?.focus();
  });

  btnCancelar?.addEventListener('click', () => {
    modoEdicion(false);
    const data = leerLS() || {};
    pintar(data);
  });

  // --- GUARDAR: también persiste en backend nombre/correo ---
  btnGuardar?.addEventListener('click', async (e) => {
    e.preventDefault();
    if (!inpNombre || !inpCorreo) return;
  
    // limpiar estados
    inpNombre.classList.remove('invalid');
    inpCorreo.classList.remove('invalid');
  
    const nombreNuevo = inpNombre.value.trim();
    const correoNuevo = (inpCorreo.value.trim() || CORREO).trim();
    const ciudadNueva = inpUbic.value.trim();
    const regionNueva = inpRegion.value.trim();
  
    let valido = true;
    if (!nombreNuevo) { inpNombre.classList.add('invalid'); valido = false; }
    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correoNuevo);
    if (!correoNuevo || !emailOk) { inpCorreo.classList.add('invalid'); valido = false; }
    if (!valido) return;
  
    // loading ON
    btnGuardar.textContent = 'Guardando...';
    btnGuardar.classList.add('loading');
    btnGuardar.disabled = true;
  
    const previo = leerLS() || {};
    const body = {
      nombre: nombreNuevo,
      correo: correoNuevo,
    };
  
    try {
      // 1. PUT para actualizar nombre/correo
      await putUsuario(previo.correo || CORREO, body);
    
      // 2. PATCH para actualizar ciudad y región si ambos tienen valor
      if (ciudadNueva && regionNueva) {
        const url = `${API_BASE}/usuarios/${encodeURIComponent(correoNuevo)}/ubicacion/region/${encodeURIComponent(regionNueva)}/${encodeURIComponent(ciudadNueva)}/modificar`;
        const respPatch = await fetch(url, { method: 'PATCH' });
        if (!respPatch.ok) {
          const txtPatch = await respPatch.text();
          throw new Error(`Error actualizando ciudad/región: ${respPatch.status} ${txtPatch}`);
        }
      }
    
      // 3. Actualizar estado local y repintar
      const fusionado = {
        ...previo,
        nombre: nombreNuevo,
        correo: correoNuevo,
        ubic: ciudadNueva || previo.ubic || '',
        region: regionNueva || previo.region || '',
        avatar: (avatarV?.src?.startsWith('data:') ? avatarV.src : (previo.avatar || null)) || null,
      };
    
      guardarLS(fusionado);
      localStorage.setItem('correoUsuario', correoNuevo);
      replaceCorreoInURL(correoNuevo);
      pintar(fusionado);
      modoEdicion(false);
    
      console.log('✅ Perfil actualizado correctamente');
    } catch (err) {
      console.error('❌ No se pudo guardar en backend:', err);
      alert('No se pudo actualizar tus datos en el servidor. Intenta nuevamente.');
    } finally {
      // loading OFF
      btnGuardar.textContent = 'Guardar';
      btnGuardar.classList.remove('loading');
      btnGuardar.disabled = false;
    }
  });

  // avatar preview
  inpAvatar?.addEventListener('change', () => {
    const file = inpAvatar.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => { if (avatarV) avatarV.src = reader.result; };
    reader.readAsDataURL(file);
  });

  // init
  cargarInicial();
  modoEdicion(false);
  syncConBackend();
});