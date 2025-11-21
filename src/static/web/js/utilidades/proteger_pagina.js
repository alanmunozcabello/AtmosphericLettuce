/* global verificarSesionActiva, obtenerCorreoDelToken, cerrarSesion */

(function() {
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

        return true
    }

    document.addEventListener('DOMContentLoaded', () => {
        console.log('🔒 Verificando sesión (DOMContentLoaded)...')
        verificarYRedirigir()
    })

    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            console.log('👁️ Página visible de nuevo (visibilitychange)')
            verificarYRedirigir()
        }
    })

    setInterval(() => {
        if (!localStorage.getItem('token')) {
            console.warn('⚠️ Token eliminado durante la sesión')
            cerrarSesion()
        }
    }, 10000)

    window.addEventListener('popstate', () => {
    if (!localStorage.getItem('token')) {
      console.warn('⚠️ Navegación atrás sin token')
      window.location.replace('index.html')
    }
  })
})()