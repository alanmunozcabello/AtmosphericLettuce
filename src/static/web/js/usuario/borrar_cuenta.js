/* global localStorage, document, window, alert, encodeURIComponent */
document.addEventListener('DOMContentLoaded', () => {
  if(!verificarSesionActiva()) {
    return
  }
  const correoUsuario = obtenerCorreoDelToken() ||
                        localStorage.getItem('correoUsuario')
  
  if (!correoUsuario) {
    cerrarSesion()
    return
  }

  const btnDelete = document.getElementById('btn-delete')
  const alerta = document.getElementById('alerta-borrar')
  const btnCancelar = document.getElementById('btn-cancelar-borrar')
  const btnConfirmar = document.getElementById('btn-confirmar-borrar')

  // --- Abrir alerta ---
  if (btnDelete) {
    btnDelete.addEventListener('click', () => {
      // alerta.style.display = 'flex' // mostrar alerta
      alerta.classList.add('activo')
    })
  }

  // --- Cancelar ---
  btnCancelar.addEventListener('click', () => {
    // alerta.style.display = 'none'
    alerta.classList.remove('activo')
  })

  // --- Confirmar borrado ---
  btnConfirmar.addEventListener('click', async () => {
    try {
      /*const res = await fetch(`/usuarios/${encodeURIComponent(correoUsuario)}`, {
        method: 'DELETE'
      })*/
      const res = await fetchConToken(
        `/usuarios/${encodeURIComponent(correoUsuario)}`,
        { method: 'DELETE' }
      )

      if (res && res.ok) {
        alert('Cuenta eliminada exitosamente')
        cerrarSesion() // <-- limpia y cierra sesión
      } else {
        alert('No se pudo eliminar la cuenta.Intenta nuevamente.')
      }
    } catch (err) {
      console.error('Error en la petición DELETE', err)
      alert('Error al intentar eliminar la cuenta')
    }
  })

  // --- Cerrar si se hace clic fuera de la alerta ---
  window.addEventListener('click', (e) => {
    if (e.target === alerta) {
      // alerta.style.display = 'none'
      alerta.classList.remove('activo')
    }
  })

  // --- Cerrar con tecla ESC ---
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      alerta.style.display = 'none'
    }
  })
})
