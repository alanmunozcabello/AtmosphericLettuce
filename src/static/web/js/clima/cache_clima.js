/* global localStorage, obtenerUsuario */
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
function obtenerClimaCacheDia () {
  try {
    const climaGuardado = localStorage.getItem('climaHoy')
    if (!climaGuardado) return null

    const clima = JSON.parse(climaGuardado)
    const ultimaActualizacion = parseInt(localStorage.getItem('climaHoyTimestamp') || '0')
    const ahora = Date.now()
    const CACHE_EXPIRY = 30 * 60 * 1000 // 30 minutos para clima

    // Si el cache está vigente, devolverlo
    if ((ahora - ultimaActualizacion) < CACHE_EXPIRY) {
      console.log('📦 Usando clima del día desde cache')
      return clima
    }

    console.log('📦 Cache de clima del día expirado')
    return null
  } catch (error) {
    console.error('❌ Error leyendo cache clima día:', error)
    return null
  }
}

function guardarClimaCacheDia (clima) {
  try {
    localStorage.setItem('climaHoy', JSON.stringify(clima))
    localStorage.setItem('climaHoyTimestamp', Date.now())
    console.log('✅ Clima del día guardado en cache')
  } catch (error) {
    console.error('❌ Error guardando cache clima día:', error)
  }
}

function obtenerClimaCacheSemana () {
  try {
    const climaGuardado = localStorage.getItem('climaSemana')
    if (!climaGuardado) return null

    const clima = JSON.parse(climaGuardado)
    const ultimaActualizacion = parseInt(localStorage.getItem('climaSemanaTimestamp') || '0')
    const ahora = Date.now()
    const CACHE_EXPIRY = 60 * 60 * 1000 // 1 hora para clima semanal

    if ((ahora - ultimaActualizacion) < CACHE_EXPIRY) {
      console.log('📦 Usando clima semanal desde cache')
      return clima
    }

    console.log('📦 Cache de clima semanal expirado')
    return null
  } catch (error) {
    console.error('❌ Error leyendo cache clima semana:', error)
    return null
  }
}

function guardarClimaCacheSemana (clima) {
  try {
    localStorage.setItem('climaSemana', JSON.stringify(clima))
    localStorage.setItem('climaSemanaTimestamp', Date.now())
    console.log('✅ Clima semanal guardado en cache')
  } catch (error) {
    console.error('❌ Error guardando cache clima semana:', error)
  }
}

function invalidarCacheClima () {
  localStorage.removeItem('climaHoy')
  localStorage.removeItem('climaHoyTimestamp')
  localStorage.removeItem('climaSemana')
  localStorage.removeItem('climaSemanaTimestamp')
  console.log('🗑️ Cache de clima invalidado')
}

// ✅ FUNCIONES PRINCIPALES CON CACHE
async function obtenerClimaDia () {
  try {
    // 1. Intentar cache primero
    const climaCache = obtenerClimaCacheDia()
    if (climaCache) {
      return climaCache
    }

    // 2. Obtener coordenadas del usuario
    const CORREO = localStorage.getItem('correoUsuario')
    const usuario = await obtenerUsuario(CORREO)
    if (!usuario) {
      console.log('No se pudo obtener datos del usuario')
      return null
    }

    const lat = usuario.ubicacion?.latitud ?? usuario.ubicacion?.lat ?? -999
    const lon = usuario.ubicacion?.longitud ?? usuario.ubicacion?.lon ?? -999

    if (lat === -999 && lon === -999) {
      console.log('No se pudo obtener latitud y longitud')
      return null
    }

    // 3. Hacer fetch al backend
    const url = `/clima/hoy/${lat}/${lon}`
    console.log('🌐 Obteniendo clima del día desde backend')

    const respuesta = await fetch(url, { method: 'GET' })
    if (!respuesta.ok) {
      console.log(`Error ${respuesta.status}: ${respuesta.statusText}`)
      return null
    }

    const resp = await respuesta.json()
    if (!resp.success) {
      return
    }

    const clima = resp.data
    console.log('✅ Clima del día obtenido:', clima)

    // 4. Guardar en cache
    guardarClimaCacheDia(clima)

    return clima
  } catch (error) {
    console.log('Error obteniendo datos de clima día:', error)
    return null
  }
}

async function obtenerClimaSemana () {
  try {
    // 1. Intentar cache primero
    const climaCache = obtenerClimaCacheSemana()
    if (climaCache) {
      return climaCache
    }

    // 2. Obtener coordenadas del usuario
    const CORREO = localStorage.getItem('correoUsuario')
    const usuario = await obtenerUsuario(CORREO)
    if (!usuario) {
      console.log('No se pudo obtener datos del usuario')
      return null
    }

    const lat = usuario.ubicacion?.latitud ?? usuario.ubicacion?.lat ?? -999
    const lon = usuario.ubicacion?.longitud ?? usuario.ubicacion?.lon ?? -999

    if (lat === -999 && lon === -999) {
      console.log('No se pudo obtener latitud y longitud')
      return null
    }

    // 3. Hacer fetch al backend
    const url = `/clima/semana/${lat}/${lon}`
    console.log('🌐 Obteniendo clima semanal desde backend')

    const respuesta = await fetch(url, { method: 'GET' })
    if (!respuesta.ok) {
      console.log(`Error ${respuesta.status}: ${respuesta.statusText}`)
      return null
    }

    const resp = await respuesta.json()
    if (!resp.success) {
      return
    }

    const clima = resp.data
    console.log('✅ Clima semanal obtenido:', clima)

    // 4. Guardar en cache
    guardarClimaCacheSemana(clima)

    return clima
  } catch (error) {
    console.log('Error obteniendo datos de clima semana:', error)
    return null
  }
}

async function obtenerClimaHora () {
  try {
    // Para clima por horas no usamos cache porque cambia muy frecuentemente
    const CORREO = localStorage.getItem('correoUsuario')
    const usuario = await obtenerUsuario(CORREO)
    if (!usuario) {
      console.log('No se pudo obtener datos del usuario')
      return null
    }

    const lat = usuario.ubicacion?.latitud ?? usuario.ubicacion?.lat ?? -999
    const lon = usuario.ubicacion?.longitud ?? usuario.ubicacion?.lon ?? -999
    if (lat === -999 && lon === -999) {
      console.log('No se pudo obtener latitud y longitud')
      return null
    }

    const url = `/clima/hora/${lat}/${lon}`
    console.log('🌐 Obteniendo clima por horas desde backend')

    const respuesta = await fetch(url, { method: 'GET' })
    if (!respuesta.ok) {
      console.log(`Error ${respuesta.status}: ${respuesta.statusText}`)
      return null
    }

    const resp = await respuesta.json()
    if (!resp.success) {
      return
    }

    const clima = resp.data
    console.log('✅ Clima por horas obtenido:', clima)

    // de moemnto no se guarda porque no se usa

    return clima
  } catch (error) {
    console.log('Error obteniendo datos de clima hora:', error)
    return null
  }
}
