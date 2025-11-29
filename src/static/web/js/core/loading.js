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
  
  const loadingScreen = document.getElementById('loadingScreen')
  if (loadingScreen) {
    loadingScreen.classList.add('hide')
    setTimeout(() => {
      loadingScreen.remove()
    }, 300)
  }
}

// ========== VALIDAR SESIÓN ==========
async function validateAndShow() {
  const currentPage = window.location.pathname
  
  // Páginas públicas
  const publicPages = ['/index.html', '/registro.html', '/landing.html', '/login.html', '/']
  const isPublicPage = publicPages.some(page => 
    currentPage.endsWith(page) || currentPage === page
  )
  
  if (isPublicPage) {
    showContent()
    return
  }
  
  // Páginas privadas: validar token
  const token = localStorage.getItem('token')
  
  if (!token) {
    window.location.replace('/index.html')
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
      showContent()
    } else {
      localStorage.removeItem('token')
      window.location.replace('/index.html')
    }
  } catch (error) {
    console.error('Error validando token:', error)
    localStorage.removeItem('token')
    window.location.replace('/index.html')
  }
}

// ========== EJECUTAR AL CARGAR ==========
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', validateAndShow)
} else {
  validateAndShow()
}

// ========== FALLBACK ==========
setTimeout(() => {
  showContent()
}, 3000)