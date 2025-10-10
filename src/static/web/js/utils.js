// const API_BASE = 'http://127.0.0.1:8000';

function obtenerUsuarioCache(correo) {
  try {
    const correoCache = localStorage.getItem('correoUsuario');
    if (!correoCache || correoCache !== correo) {
      console.log('🚫 Cache inválido: sesión no coincide');
      invalidarCache();
      window.location.href = 'index.html';
      return null;
    }

    const usuario = JSON.parse(localStorage.getItem('usuario') || 'null');
    if (!usuario || usuario.correo !== correo) {
      console.log('📦 Cache inválido: usuario no coincide');
      invalidarCache();
      return null;
    }

    const ultimaActualizacion = parseInt(localStorage.getItem('ultimaActualizacion') || '0');
    const ahora = Date.now();
    const CACHE_EXPIRY = 5 * 60 * 1000; // 5 minutos
    
    if ((ahora - ultimaActualizacion) < CACHE_EXPIRY) {
      console.log('📦 Cache válido y reciente');
      return usuario;
    }
    
    console.log('📦 Cache expirado por tiempo');
    return null; // ✅ Solo expirado, no invalid
  } catch (error) {
    console.error('❌ Error leyendo cache:', error);
    invalidarCache();
    return null;
  }
}

async function obtenerUsuario(correo) {
  // verificar sesión ANTES de intentar cache
  const correoCache = localStorage.getItem('correoUsuario');
  if (!correoCache) {
    console.log('🚫 No hay sesión - redirigiendo a login');
    window.location.href = 'index.html';
    return null;
  }

  // intentar cache primero
  let usuario = obtenerUsuarioCache(correo);
  
  if (usuario) {
    console.log('📦 Usando datos en cache - NO FETCH');
    return usuario;
  }
  
  // solo ir al backend si realmente es necesario
  try {
    console.log('🌐 Cache expirado/inexistente - cargando desde backend');
    const res = await fetch(`${API_BASE}/usuarios/${encodeURIComponent(correo)}`);
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    
    usuario = await res.json();
    
    // Actualizar cache
    localStorage.setItem('usuario', JSON.stringify(usuario));
    localStorage.setItem('ultimaActualizacion', Date.now());
    
    console.log('✅ Cache actualizado desde backend');
    return usuario;
  } catch (error) {
    console.error('❌ Error fetch backend:', error);
    
    // Si falla backend, intentar usar cache expirado como fallback -> estrategia de respaldo para mostrar los datos expirados como ultimo recurso -> preguntar al profe si es buena idea hacer esto
    const cacheExpirado = JSON.parse(localStorage.getItem('usuario') || 'null');
    if (cacheExpirado && cacheExpirado.correo === correo) {
      console.log('📦 Usando cache expirado como fallback');
      return cacheExpirado;
    }
    
    // Si no hay nada, ir al login
    invalidarCache();
    alert('Error de conexión. Redirigiendo al login...');
    window.location.href = 'index.html';
    return null;
  }
}

function actualizarCacheUsuario(nuevosdatos) {
  try {
    const usuarioActual = JSON.parse(localStorage.getItem('usuario') || '{}');
    const usuarioActualizado = { ...usuarioActual, ...nuevosdatos };
    
    localStorage.setItem('usuario', JSON.stringify(usuarioActualizado));
    localStorage.setItem('ultimaActualizacion', Date.now());
    
    console.log('✅ Cache actualizado:', usuarioActualizado);
  } catch (error) {
    console.error('❌ Error actualizando cache:', error);
  }
}

function invalidarCache() {
  localStorage.removeItem('usuario');
  localStorage.removeItem('ultimaActualizacion');
  console.log('🗑️ Cache invalidado');
}

// función auxiliar para debugging
function verEstadoCache(correo) {
  const correoCache = localStorage.getItem('correoUsuario');
  const usuario = JSON.parse(localStorage.getItem('usuario') || 'null');
  const ultimaActualizacion = parseInt(localStorage.getItem('ultimaActualizacion') || '0');
  const ahora = Date.now();
  
  console.log('🔍 Estado del cache:');
  console.log('   Correo solicitado:', correo);
  console.log('   Correo en cache:', correoCache);
  console.log('   Usuario en cache:', usuario?.correo);
  console.log('   Última actualización:', new Date(ultimaActualizacion).toLocaleString());
  console.log('   Expirado:', (ahora - ultimaActualizacion) > 5 * 60 * 1000);
}

// Invalidar cache de clima cuando cambien las coordenadas del usuario
function invalidarCacheClimaSiCambiaUbicacion(usuarioNuevo) {
  try {
    const usuarioAnterior = JSON.parse(localStorage.getItem('usuario') || '{}');
    
    const latAnterior = usuarioAnterior.ubicacion?.latitud || 0;
    const lonAnterior = usuarioAnterior.ubicacion?.longitud || 0;
    const latNueva = usuarioNuevo.ubicacion?.latitud || 0;
    const lonNueva = usuarioNuevo.ubicacion?.longitud || 0;
    
    // Si las coordenadas cambiaron, invalidar cache de clima
    if (latAnterior !== latNueva || lonAnterior !== lonNueva) {
      console.log('🌍 Coordenadas cambiaron, invalidando cache de clima');
      invalidarCacheClima();
    }
  } catch (error) {
    console.error('Error verificando cambio de coordenadas:', error);
  }
}