// ========== INICIALIZAR EVENTOS CRUD ==========
function inicializarEventosCRUD () {
  const form = document.getElementById('form-cultivo')
  const listaCultivos = document.getElementById('lista-cultivos')

  if (form) {
    form.removeEventListener('submit', agregarCultivo)
    form.addEventListener('submit', agregarCultivo)
  }

  if (listaCultivos) {
    listaCultivos.removeEventListener('click', manejarClickLista)
    listaCultivos.addEventListener('click', manejarClickLista)
  }

  console.log('✅ Eventos CRUD inicializados')
}

// ========== AGREGAR CULTIVO ==========
async function agregarCultivo (e) {
  e.preventDefault()

  const { correo, cultivosData } = window.cultivosState
  const inputCultivo = document.getElementById('input-cultivo')
  const inputHectareas = document.getElementById('input-hectareas')

  const nombre = inputCultivo.value.trim()
  const hectareas = parseFloat(inputHectareas.value)

  if (!nombre || hectareas <= 0) {
    alert('⚠️ Completa los campos correctamente')
    return
  }

  try {
    // ✅ Verificar si ya existe
    const cultivoExiste = cultivosData.hasOwnProperty(nombre)

    const accionTexto = cultivoExiste ? 'Modificando' : 'Agregando'
    console.log(`${accionTexto} cultivo:`, nombre)

    const response = await fetch(
      `/usuarios/${encodeURIComponent(correo)}/agregar_cultivo`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre_cultivo: nombre,
          hectareas: hectareas
        })
      }
    )

    const data = await response.json()

    if (data.error) {
      throw new Error(data.error)
    }

    if (!response.ok) {
      throw new Error(data.error || data.detail || 'Error en el servidor')
    }

    console.log('✅', data.mensaje || 'Cultivo guardado')

    if (window.invalidarCache) {
      window.invalidarCache()
    }

    await new Promise(resolve => setTimeout(resolve, 100))

    // ✅ Recargar cultivos
    if (window.recargarCultivos) {
      await window.recargarCultivos()
    }

    // Limpiar formulario
    inputCultivo.value = ''
    inputHectareas.value = ''
    inputCultivo.focus()

    const accion = cultivoExiste ? 'modificado' : 'agregado'
    alert(`✅ Cultivo ${accion} correctamente`)
  } catch (error) {
    console.error('❌ Error guardando cultivo:', error)
    alert(`⚠️ ${error.message}`)
  }
}

// ========== ELIMINAR CULTIVO ==========
async function eliminarCultivo (e) {
  const btn = e.target.closest('.btn-eliminar')
  if (!btn) return

  const { correo, cultivoSeleccionado } = window.cultivosState
  const nombre = btn.dataset.nombre

  if (!confirm(`¿Eliminar "${nombre}"?`)) return

  try {
    const response = await fetch(
      `/usuarios/${encodeURIComponent(correo)}/${encodeURIComponent(nombre)}/eliminar`,
      { method: 'DELETE' }
    )

    const data = await response.json()

    if (data.error) {
      throw new Error(data.error)
    }

    if (!response.ok) {
      throw new Error(data.error || data.detail || 'Error en el servidor')
    }

    console.log('✅', data.mensaje || 'Cultivo eliminado del servidor')

    // si estaba seleccionado se limpia al seleccion
    if (cultivoSeleccionado === nombre) {
      window.cultivosState.cultivoSeleccionado = null
      console.log('🔄 Cultivo seleccionado limpiado')

      // limpiar seleccion de la lista
      document.querySelectorAll('.item-cultivo').forEach(item => {
        item.classList.remove('seleccionado')
      })
    }

    // invalidar cache
    if (window.invalidarCache) {
      window.invalidarCache()
    }

    await new Promise(resolve => setTimeout(resolve, 100))

    // recargar cultivos
    if (window.recargarCultivos) {
      console.log('🔄 Recargando datos...')
      await window.recargarCultivos()
      console.log('🔍 Cultivos después:', Object.keys(window.cultivosState.cultivosData))
    }

    alert('✅ Cultivo eliminado correctamente')
  } catch (error) {
    console.error('❌ Error eliminando cultivo:', error)
    alert(`⚠️ ${error.message}`)
  }
}

// funcion modular para manejar lso clicks de la lista
function manejarClickLista (e) {
  // Eliminar
  if (e.target.classList.contains('btn-eliminar')) {
    eliminarCultivo(e)
    return
  }

  // Configurar
  if (e.target.classList.contains('btn-config')) {
    const nombre = e.target.dataset.nombre
    const { correo } = window.cultivosState
    window.location.href = `formulario_plantas.html?cultivo=${encodeURIComponent(nombre)}&correo=${encodeURIComponent(correo)}`
    return
  }

  // Seleccionar cultivo
  const item = e.target.closest('.item-cultivo')
  if (item && !e.target.classList.contains('btn-eliminar') && !e.target.classList.contains('btn-config')) {
    const nombre = item.dataset.nombre
    if (typeof seleccionarCultivoMapa === 'function') {
      seleccionarCultivoMapa(nombre)
    }
  }
}
