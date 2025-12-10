/* global localStorage, obtenerCorreoDelToken, verificarSesionActiva, cerrarSesion, fetchConToken, invalidarCacheClima */

function obtenerUsuarioCache (correo) {
  try {
    const correoToken = obtenerCorreoDelToken()
    if (!correoToken || correoToken !== correo) {
      invalidarCache()
      return null
    }

    const usuario = JSON.parse(localStorage.getItem('usuario') || 'null')
    if (!usuario || usuario.correo !== correo) {
      invalidarCache()
      return null
    }

    const ultimaActualizacion = parseInt(localStorage.getItem('ultimaActualizacion') || '0')
    const ahora = Date.now()
    const CACHE_EXPIRY = 5 * 60 * 1000 // 5 minutos

    if ((ahora - ultimaActualizacion) < CACHE_EXPIRY) {
      return usuario
    }

    return null // ✅ Solo expirado, no invalid
  } catch (error) {
    console.error('❌ Error leyendo cache:', error)
    invalidarCache()
    return null
  }
}

async function obtenerUsuario (correo) {
  // verificar sesión activa antes de todo
  if (!verificarSesionActiva()) {
    return null
  }

  const correoToken = obtenerCorreoDelToken()
  if (!correoToken) {
    cerrarSesion()
    return null
  }

  if (correoToken !== correo) {
    cerrarSesion()
    return null
  }
  // intentar cache primero
  let usuario = obtenerUsuarioCache(correo)

  if (usuario) {
    return usuario
  }

  // solo ir al backend si realmente es necesario
  try {
    const res = await fetchConToken(`/usuarios/${encodeURIComponent(correo)}`)

    if (!res || !res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`)
    }

    usuario = await res.json()

    // Actualizar cache
    localStorage.setItem('usuario', JSON.stringify(usuario))
    localStorage.setItem('ultimaActualizacion', Date.now())

    return usuario
  } catch (error) {
    console.error('❌ Error fetch backend:', error)

    // Si falla backend, intentar usar cache expirado como fallback -> estrategia de respaldo para mostrar los datos expirados como ultimo recurso -> preguntar al profe si es buena idea hacer esto
    const cacheExpirado = JSON.parse(localStorage.getItem('usuario') || 'null')
    if (cacheExpirado && cacheExpirado.correo === correo) {
      return cacheExpirado
    }

    // Si no hay nada, cerrar sesión
    invalidarCache()
    alert('Error de conexión. Redirigiendo al login...')
    cerrarSesion()
    return null
  }
}

async function obtenerNombresCultivos(correo) {
  if (!verificarSesionActiva()) return []

  try {
    const res = await fetchConToken(`/usuarios/${encodeURIComponent(correo)}/cultivos/nombres`)

    if (!res || !res.ok) {
      throw new Error('Error al obtener nombres de cultivos')
    }

    const nombres = await res.json()
    return Array.isArray(nombres) ? nombres : []

  } catch (error) {
    console.error('❌ Error obteniendo nombres de cultivos:', error)
    return []
  }
}

function actualizarCacheUsuario(nuevosdatos) {
  try {
    const usuarioActual = JSON.parse(localStorage.getItem('usuario') || '{}')
    const usuarioActualizado = { ...usuarioActual, ...nuevosdatos }

    localStorage.setItem('usuario', JSON.stringify(usuarioActualizado))
    localStorage.setItem('ultimaActualizacion', Date.now())

  } catch (error) {
    console.error('❌ Error actualizando cache:', error)
  }
}

function invalidarCache () {
  localStorage.removeItem('usuario')
  localStorage.removeItem('ultimaActualizacion')
}

// función auxiliar para debugging
function verEstadoCache (correo) {
  const correoToken = obtenerCorreoDelToken()
  const usuario = JSON.parse(localStorage.getItem('usuario') || 'null')
  const ultimaActualizacion = parseInt(localStorage.getItem('ultimaActualizacion') || '0')
  const ahora = Date.now()

}

// Invalidar cache de clima cuando cambien las coordenadas del usuario
function invalidarCacheClimaSiCambiaUbicacion (usuarioNuevo) {
  try {
    const usuarioAnterior = JSON.parse(localStorage.getItem('usuario') || '{}')

    const latAnterior = usuarioAnterior.ubicacion?.latitud || 0
    const lonAnterior = usuarioAnterior.ubicacion?.longitud || 0
    const latNueva = usuarioNuevo.ubicacion?.latitud || 0
    const lonNueva = usuarioNuevo.ubicacion?.longitud || 0

    // Si las coordenadas cambiaron, invalidar cache de clima
    if (latAnterior !== latNueva || lonAnterior !== lonNueva) {
      invalidarCacheClima()
    }
  } catch (error) {
    console.error('Error verificando cambio de coordenadas:', error)
  }
}
