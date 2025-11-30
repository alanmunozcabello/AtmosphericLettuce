/* global localStorage, location, document, window, invalidarCache */
document.addEventListener('DOMContentLoaded', () => {
  if (!verificarSesionActiva()) {
    return
  }

  const correoDelToken = obtenerCorreoDelToken()

  // Obtener correo de localStorage o URL params
  const correoUsuario = correoDelToken

  if (!correoUsuario) {
    console.error('❌ No se pudo obtener correo del token')
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
      window.location.href = 'home.html'
    })
  }
})

// Función global para cerrar sesión
function logout () {
  cerrarSesion()
}
