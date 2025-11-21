/* global localStorage, location, document, window, verificarSesionActiva, obtenerCorreoDelToken, cerrarSesion, fetchConToken, obtenerUsuario */
function validarSesion() {
    if (!verificarSesionActiva()) {
        console.log('❌ No hay sesión activa, redirigiendo...')
        return false
    }

    const correoUsuario = obtenerCorreoDelToken()
    
    if (!correoUsuario) {
        console.error('❌ No se pudo obtener correo del token')
        cerrarSesion()
        return false
    }
    
    const correoURL = new URLSearchParams(location.search).get('correo')

    if (correoURL && correoURL.toLowerCase() !== correoUsuario.toLowerCase()) {
        console.error('❌ Intento de acceso no autorizado')
        alert('Acceso denegado: no puedes ver el perfil de otro usuario')
        cerrarSesion()
        return false
    }

    localStorage.setItem('correoUsuario', correoUsuario)
    console.log('✅ Usuario autenticado en home:', correoUsuario)
    return true
}

window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        console.log('⚠️ Página restaurada desde caché (botón Atrás)')
        validarSesion()
    }
})

document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 Carga inicial de home.html')
    validarSesion()
})

window.addEventListener('beforeunload', () => {
    sessionStorage.setItem('navegandoFuera', 'true')
})

window.addEventListener('load', () => {
    if (sessionStorage.getItem('navegandoFuera') === 'true') {
        sessionStorage.removeItem('navegandoFuera')
        validarSesion()
    }
})

setInterval(() => {
  if (!localStorage.getItem('token')) {
    console.warn('⚠️ Token eliminado durante la sesión')
    cerrarSesion()
  }
}, 30000)