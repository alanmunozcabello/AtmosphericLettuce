/* global localStorage, location, document, window, invalidarCache */
document.addEventListener('DOMContentLoaded', () => {
  if (!verificarSesionActiva()) {
    return
  }

  const correoDelToken = obtenerCorreoDelToken()
  const correoURL = new URLSearchParams(location.search).get('correo')

  if (correoURL && correoURL.toLowerCase() !== correoDelToken?.toLowerCase()) {
    console.error('❌ Intento de acceso no autorizado')
    cerrarSesion()
    return
  }
  // Obtener correo de localStorage o URL params
  const correoUsuario = correoDelToken ||
                        localStorage.getItem('correoUsuario')

  if (!correoUsuario) {
    cerrarSesion()
    return
  }

  // Guardar/actualizar en localStorage
  localStorage.setItem('correoUsuario', correoUsuario)

  // Mostrar correo en la UI
  const correoElement = document.getElementById('correo-usuario')
  if (correoElement) {
    correoElement.textContent = correoUsuario
  }

  // Manejar clic en logo
  const logo = document.querySelector('.logo img')
  if (logo) {
    logo.addEventListener('click', () => {
      window.location.href = `home.html?correo=${encodeURIComponent(correoUsuario)}`
    })
  }
})

// Función global para cerrar sesión
function logout () {
  cerrarSesion()
}
