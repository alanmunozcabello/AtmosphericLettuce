/* global window, document, localStorage */

// ========== DESHABILITAR BFCACHE ==========
// Forzar recarga cuando la página viene del cache
window.addEventListener('pageshow', (event) => {
  if (event.persisted) {
    // La página viene del bfcache: recargar
    window.location.reload()
  }
})

// ========== MOSTRAR CONTENIDO ==========
function showContent() {
  document.body.classList.add('content-visible')
  // ✅ Permitir scroll cuando se oculta el loading
  document.body.classList.remove('loading-active')

  const loadingScreen = document.getElementById('loadingScreen')
  if (loadingScreen) {
    loadingScreen.classList.add('hide')
    setTimeout(() => {
      loadingScreen.remove()
    }, 300)
  }
}

// ========== VALIDAR SESIÓN Y ESPERAR DATOS ==========
async function validateAndShow() {
  const currentPage = window.location.pathname

  // Páginas públicas
  const publicPages = ['/login.html', '/registro.html', '/landing.html', '/']
  const isPublicPage = publicPages.some(page =>
    currentPage.endsWith(page) || currentPage === page
  )

  if (isPublicPage) {
    // Mostrar HTML inmediatamente en páginas públicas
    document.documentElement.style.display = 'block'
    showContent()
    return
  }

  // Páginas privadas: validar token
  const token = localStorage.getItem('token')

  if (!token) {
    window.location.replace('/login.html')
    return
  }

  try {
    const response = await fetch('/api/validar-token', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    })

    if (response.ok) {
      // ESPERAR a que los datos críticos estén listos
      await esperarDatosCriticos()
      showContent()
    } else {
      localStorage.removeItem('token')
      window.location.replace('/login.html')
    }
  } catch (error) {
    console.error('Error validando token:', error)
    localStorage.removeItem('token')
    window.location.replace('/login.html')
  }
}

// ========== Esperar datos según la página ==========
async function esperarDatosCriticos() {
  const currentPage = window.location.pathname

  console.log('⏳ Esperando datos críticos para:', currentPage)

  if (currentPage.includes('home.html')) {
    // Esperar clima + usuario (máximo 8 segundos total)
    await Promise.all([
      waitFor(() => window.climaCargado, 'Clima', 4000),  // 4s
      waitFor(() => window.usuarioCargado, 'Usuario', 4000)  // 4s
    ])
  } else if (currentPage.includes('dias.html')) {
    await waitFor(() => window.climaSemanaCargado, 'Clima semanal', 5000)
  } else if (currentPage.includes('perfil.html')) {
    await waitFor(() => window.perfilCargado, 'Perfil', 5000)
  } else if (currentPage.includes('gestor_cultivos.html')) {
    await waitFor(() => window.cultivosCargados, 'Cultivos', 6000)  // Más tiempo para scroll infinito
  } else if (currentPage.includes('formulario_plantas.html')) {
    await waitFor(() => window.formularioCargado, 'Formulario', 2000)
  } else {
    console.log('ℹ️ Página sin datos específicos')
  }

  console.log('✅ Todos los datos críticos están listos')
}

// ========== Helper: Esperar hasta que una condición sea true ==========
function waitFor(condition, nombre = 'Dato', timeout = 5000) {
  return new Promise((resolve) => {
    const startTime = Date.now()

    const interval = setInterval(() => {
      if (condition()) {
        clearInterval(interval)
        console.log(`✅ ${nombre} cargado`)
        resolve()
      } else if (Date.now() - startTime > timeout) {
        console.warn(`⚠️ Timeout esperando: ${nombre}`)
        clearInterval(interval)
        resolve() // Continuar de todos modos para no bloquear
      }
    }, 100)
  })
}

// ========== EJECUTAR AL CARGAR ==========
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', validateAndShow)
} else {
  validateAndShow()
}

// ========== FALLBACK ==========
setTimeout(() => {
  console.warn('⚠️ Timeout general del loading screen (10s)')
  showContent()
}, 10000) // 10 segundos máximo