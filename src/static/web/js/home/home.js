/* global localStorage, location, document, window, verificarSesionActiva, obtenerCorreoDelToken, cerrarSesion, fetchConToken, obtenerUsuario */
function validarSesion() {
    if (!verificarSesionActiva()) {
        return false
    }

    const correoUsuario = obtenerCorreoDelToken()

    if (!correoUsuario) {
        console.error('❌ No se pudo obtener correo del token')
        cerrarSesion()
        return false
    }

    localStorage.setItem('correoUsuario', correoUsuario)
    // Marcar como listo
    window.usuarioCargado = true

    return true
}

window.addEventListener('pageshow', (event) => {
    if (event.persisted) {
        // ✅ NO hacer validarSesion() aquí para evitar flash
        // El DOM ya está intacto desde la caché
    }
})

document.addEventListener('DOMContentLoaded', () => {
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
        cerrarSesion()
    }
}, 30000)