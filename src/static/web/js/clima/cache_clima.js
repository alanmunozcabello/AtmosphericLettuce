/* global localStorage, obtenerUsuario, fetchConToken */
// aquí gestionaré el clima en local storage
// problematica -> para obtener la temp actual min y max de hoy necesito hacer la llamada a clima hoy y clima semana
// solucion -> guardar en localstorage la informacion completa de el clima en el formato siguiente:

// climaHoy={
//     dia:"dia de la semana",
//     estado:"estado",
//     temp:"temp",
//     min:"min",
//     max:"max"
// }

// climaSemana={
//     "1":{
//         info:"info dia 1"
//     },
//     "2":{
//         info:"info dia 2"
//     },
//     "3":{
//         info:"info dia 3"
//     },
//     "4":{
//         info:"info dia 4"
//     },
//     "5":{
//         info:"info dia 5"
//     },
//     "6":{
//         info:"info dia 6"
//     },
//     "7":{
//         info:"info dia 7"
//     }
// }

// ✅ FUNCIONES DE CACHE
function obtenerClimaCacheDia() {
  try {
    const climaGuardado = localStorage.getItem('climaHoy')
    if (!climaGuardado) return null

    const clima = JSON.parse(climaGuardado)
    const ultimaActualizacion = parseInt(localStorage.getItem('climaHoyTimestamp') || '0')
    const ahora = Date.now()
    const CACHE_EXPIRY = 30 * 60 * 1000 // 30 minutos para clima

    // Si el cache está vigente, devolverlo
    if ((ahora - ultimaActualizacion) < CACHE_EXPIRY) {
      return clima
    }
    return null
  } catch (error) {
    console.error('❌ Error leyendo cache clima día:', error)
    return null
  }
}

function guardarClimaCacheDia(clima) {
  try {
    localStorage.setItem('climaHoy', JSON.stringify(clima))
    localStorage.setItem('climaHoyTimestamp', Date.now())
  } catch (error) {
    console.error('❌ Error guardando cache clima día:', error)
  }
}

function obtenerClimaCacheSemana() {
  try {
    const climaGuardado = localStorage.getItem('climaSemana')
    if (!climaGuardado) return null

    const clima = JSON.parse(climaGuardado)
    const ultimaActualizacion = parseInt(localStorage.getItem('climaSemanaTimestamp') || '0')
    const ahora = Date.now()
    const CACHE_EXPIRY = 60 * 60 * 1000 // 1 hora para clima semanal

    if ((ahora - ultimaActualizacion) < CACHE_EXPIRY) {
      return clima
    }
    return null
  } catch (error) {
    console.error('❌ Error leyendo cache clima semana:', error)
    return null
  }
}

function guardarClimaCacheSemana(clima) {
  try {
    localStorage.setItem('climaSemana', JSON.stringify(clima))
    localStorage.setItem('climaSemanaTimestamp', Date.now())
  } catch (error) {
    console.error('❌ Error guardando cache clima semana:', error)
  }
}

function invalidarCacheClima() {
  localStorage.removeItem('climaHoy')
  localStorage.removeItem('climaHoyTimestamp')
  localStorage.removeItem('climaSemana')
  localStorage.removeItem('climaSemanaTimestamp')
}

// ✅ FUNCIÓN PARA ACTUALIZAR COORDENADAS (usada al cambiar ubicación)
function actualizarCoordsClima(lat, lon) {
  localStorage.setItem('climaLat', lat)
  localStorage.setItem('climaLon', lon)
}

// ✅ FUNCIONES PRINCIPALES CON CACHE
async function obtenerClimaDiaFresco() {
  try {
    // ✅ OBTENER DATOS FRESCOS SIN CACHE (para cuando cambia ubicación)
    // 2. Obtener coordenadas del usuario
    let lat = localStorage.getItem('climaLat')
    let lon = localStorage.getItem('climaLon')

    // Si no hay coords guardadas, obtener del usuario
    if (!lat || !lon) {
      const CORREO = localStorage.getItem('correoUsuario')
      const usuario = await obtenerUsuario(CORREO)
      if (!usuario) {
        return null
      }

      lat = usuario.ubicacion?.latitud ?? usuario.ubicacion?.lat ?? -999
      lon = usuario.ubicacion?.longitud ?? usuario.ubicacion?.lon ?? -999
    }

    if (lat === -999 && lon === -999) {
      return null
    }

    // 3. Hacer fetch al backend SIN CACHE
    const url = `/clima/hoy/${lat}/${lon}`

    const respuesta = await fetchConToken(url, { method: 'GET' })
    if (!respuesta.ok) {
      return null
    }

    const resp = await respuesta.json()
    if (!resp.success) {
      return
    }

    const clima = resp.data

    // 4. Guardar en cache
    guardarClimaCacheDia(clima)

    return clima
  } catch (error) {
    return null
  }
}

async function obtenerClimaDia() {
  try {
    // 1. Intentar cache primero
    const climaCache = obtenerClimaCacheDia()
    if (climaCache) {
      return climaCache
    }

    // 2. Obtener coordenadas del usuario
    let lat = localStorage.getItem('climaLat')
    let lon = localStorage.getItem('climaLon')

    // Si no hay coords guardadas, obtener del usuario
    if (!lat || !lon) {
      const CORREO = localStorage.getItem('correoUsuario')
      const usuario = await obtenerUsuario(CORREO)
      if (!usuario) {
        return null
      }

      lat = usuario.ubicacion?.latitud ?? usuario.ubicacion?.lat ?? -999
      lon = usuario.ubicacion?.longitud ?? usuario.ubicacion?.lon ?? -999
    }

    if (lat === -999 && lon === -999) {
      return null
    }

    // 3. Hacer fetch al backend
    const url = `/clima/hoy/${lat}/${lon}`

    const respuesta = await fetchConToken(url, { method: 'GET' })
    if (!respuesta.ok) {
      return null
    }

    const resp = await respuesta.json()
    if (!resp.success) {
      return
    }

    const clima = resp.data

    // 4. Guardar en cache
    guardarClimaCacheDia(clima)

    return clima
  } catch (error) {
    return null
  }
}

async function obtenerClimaSemana() {
  try {
    // 1. Intentar cache primero
    const climaCache = obtenerClimaCacheSemana()
    if (climaCache) {
      return climaCache
    }

    // 2. Obtener coordenadas del usuario
    let lat = localStorage.getItem('climaLat')
    let lon = localStorage.getItem('climaLon')

    // Si no hay coords guardadas, obtener del usuario
    if (!lat || !lon) {
      const CORREO = localStorage.getItem('correoUsuario')
      const usuario = await obtenerUsuario(CORREO)
      if (!usuario) {
        return null
      }

      lat = usuario.ubicacion?.latitud ?? usuario.ubicacion?.lat ?? -999
      lon = usuario.ubicacion?.longitud ?? usuario.ubicacion?.lon ?? -999
    }

    if (lat === -999 && lon === -999) {
      return null
    }

    // 3. Hacer fetch al backend
    const url = `/clima/semana/${lat}/${lon}`

    const respuesta = await fetchConToken(url, { method: 'GET' })
    if (!respuesta.ok) {
      return null
    }

    const resp = await respuesta.json()
    if (!resp.success) {
      return
    }

    const clima = resp.data

    // 4. Guardar en cache
    guardarClimaCacheSemana(clima)

    return clima
  } catch (error) {
    return null
  }
}

async function obtenerClimaHora() {
  try {
    // Para clima por horas no usamos cache porque cambia muy frecuentemente
    const CORREO = localStorage.getItem('correoUsuario')
    const usuario = await obtenerUsuario(CORREO)
    if (!usuario) {
      return null
    }

    const lat = usuario.ubicacion?.latitud ?? usuario.ubicacion?.lat ?? -999
    const lon = usuario.ubicacion?.longitud ?? usuario.ubicacion?.lon ?? -999
    if (lat === -999 && lon === -999) {
      return null
    }

    const token = localStorage.getItem('token')
    const url = `/clima/hora/${lat}/${lon}`

    const respuesta = await fetchConToken(url, { method: 'GET' })
    if (!respuesta.ok) {
      return null
    }

    const resp = await respuesta.json()
    if (!resp.success) {
      return
    }

    const clima = resp.data

    // de moemnto no se guarda porque no se usa

    return clima
  } catch (error) {
    console.log('Error obteniendo datos de clima hora:', error)
    return null
  }
}
