/**
 * Utilidades de autenticación JWT
 */

/**
 * Verifica que el usuario tenga sesión activa
 * @returns {boolean} true si hay token válido, false si no
 */
function verificarSesionActiva() {
  const token = localStorage.getItem('token')
  
  if (!token) {
    console.warn('⚠️ No hay token, redirigiendo a login...')
    window.location.replace('index.html')
    return false
  }

  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    const ahora = Math.floor(Date.now() / 1000)
    
    if (payload.exp < ahora) {
      console.warn('⚠️ Token expirado, redirigiendo a login...')
      localStorage.clear()
      window.location.replace('index.html')
      return false
    }
  } catch (e) {
    console.error('❌ Token inválido:', e)
    localStorage.clear()
    window.location.replace('index.html')
    return false
  }

  return true
}

/**
 * Realiza peticiones HTTP autenticadas con JWT
 * @param {string} url - Endpoint (ej: '/usuarios/correo@mail.com')
 * @param {Object} options - Opciones de fetch
 * @returns {Promise<Response>}
 */
async function fetchConToken(url, options = {}) {
  const token = localStorage.getItem('token')
  
  if (!token) {
    window.location.replace('index.html')
    return
  }

  const headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }

  try {
    const response = await fetch(url, { ...options, headers })

    if (response.status === 401) {
      localStorage.clear()
      alert('Tu sesión ha expirado. Inicia sesión nuevamente.')
      window.location.replace('index.html')
      return
    }

    return response
  } catch (error) {
    console.error('Error en petición autenticada:', error)
    throw error
  }
}

/**
 * Cierra sesión de forma segura
 */
function cerrarSesion() {
  console.log('👋 Cerrando sesión...')
  localStorage.clear()
  sessionStorage.clear()
  window.location.replace('index.html')
  window.history.pushState(null, '', 'index.html')
}

/**
 * Obtiene el correo del usuario desde el token
 * @returns {string|null} Correo del usuario o null
 */
function obtenerCorreoDelToken() {
  const token = localStorage.getItem('token')
  if (!token) return null
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.sub
  } catch (e) {
    return null
  }
}

// Prevenir navegación hacia atrás después de logout
window.addEventListener('popstate', function(event) {
  const token = localStorage.getItem('token')
  if (!token) {
    console.warn('⚠️ Intento de volver atrás sin token')
    window.history.pushState(null, '', 'index.html')
    window.location.replace('index.html')
  }
})