/* global verificarSesionActiva, obtenerCorreoDelToken, cerrarSesion */

(function () {
    'use strict'

    function verificarYRedirigir() {
        if (!verificarSesionActiva()) {
            return false
        }

        const correoUsuario = obtenerCorreoDelToken()
        if (!correoUsuario) {
            cerrarSesion()
            return false
        }
        const urlParams = new URLSearchParams(window.location.search)
        const correoURL = urlParams.get('correo')

        if (correoURL && correoURL.toLowerCase() !== correoUsuario.toLowerCase()) {
            console.error('❌ Intento de acceso a otra cuenta')
            alert('Acceso denegado: no puedes acceder a información de otro usuario')
            cerrarSesion()
            return false
        }

        document.body.classList.add('sesion-validada')
        return true
    }

    if (!verificarSesionActiva()) {
        document.documentElement.style.display = 'none'
    } else {
        verificarYRedirigir()
    }

    document.addEventListener('DOMContentLoaded', () => {
        verificarYRedirigir()
    })

    window.addEventListener('pageshow', (event) => {
        if (event.persisted) {
            document.body.classList.remove('sesion-validada')
            verificarYRedirigir()
        }
    })

    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            verificarYRedirigir()
        }
    })

    setInterval(() => {
        if (!localStorage.getItem('token')) {
            cerrarSesion()
        }
    }, 10000)

    window.addEventListener('popstate', () => {
        if (!localStorage.getItem('token')) {
            document.documentElement.style.display = 'none'
            window.location.replace('login.html')
        }
    })
})()