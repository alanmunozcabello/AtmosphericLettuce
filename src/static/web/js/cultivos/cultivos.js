/* global verificarSesionActiva, obtenerCorreoDelToken, cerrarSesion, obtenerUsuario, location, localStorage */

window.recargarCultivos = async function () {
  console.log('⚠️ recargarCultivos llamado antes de inicializar')
  return Promise.resolve()
}

document.addEventListener('DOMContentLoaded', () => {
  if (!verificarSesionActiva()) {
    return
  }

  // ========== VERIFICAR SESIÓN ==========
  const CORREO = obtenerCorreoDelToken()

  if (!CORREO) {
    console.error('❌ No se pudo obtener correo del token')
    cerrarSesion()
    return
  }

  const correoURL = new URLSearchParams(location.search).get('correo')
  
  if (correoURL && correoURL.toLowerCase() !== CORREO.toLowerCase()) {
    console.error('❌ Intento de acceso no autorizado')
    alert('Acceso denegado: no puedes ver cultivos de otro usuario')
    cerrarSesion()
    return
  }

  localStorage.setItem('correoUsuario', CORREO)

  // ========== ESTADO GLOBAL COMPARTIDO ==========
  window.cultivosState = {
    correo: CORREO,
    usuarioData: null, // ✅ Guardar datos completos del usuario
    cultivosData: {}, // ✅ Formato: { nombre: cultivoObj }
    cultivoSeleccionado: null,
    usuarioLatitud: -33.446,
    usuarioLongitud: -70.681,
    colores: [
      '#ef4444', '#f59e0b', '#10b981', '#3b82f6',
      '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'
    ]
  }

  // ========== INICIALIZACIÓN ==========
  async function inicializar () {
    console.log('🌾 Inicializando gestor de cultivos...')

    try {
      // 1. Obtener datos del usuario
      const usuario = await obtenerUsuario(CORREO)

      if (!usuario) {
        console.warn('⚠️ No se pudo obtener datos del usuario')
        cerrarSesion()
        return
      }
        // ✅ Guardar datos completos
      window.cultivosState.usuarioData = usuario

        // ✅ Actualizar ubicación con nuevo formato
      if (usuario.ubicacion) {
        window.cultivosState.usuarioLatitud = usuario.ubicacion.latitud || -33.446
        window.cultivosState.usuarioLongitud = usuario.ubicacion.longitud || -70.681
        console.log('📍 Ubicación:',
          window.cultivosState.usuarioLatitud,
          window.cultivosState.usuarioLongitud
        )
      }

        // ✅ Convertir array de cultivos a objeto { nombre: cultivoObj }
      if (Array.isArray(usuario.cultivos)) {
        window.cultivosState.cultivosData = {}
        usuario.cultivos.forEach(cultivo => {
          window.cultivosState.cultivosData[cultivo.nombre] = cultivo
        })
        console.log('✅ Cultivos cargados:', Object.keys(window.cultivosState.cultivosData).length)
      }

      // 2. Inicializar mapa principal
      if (typeof inicializarMapaPrincipal === 'function') {
        inicializarMapaPrincipal()
      }

      // 3. Renderizar UI
      if (typeof renderizarLista === 'function') {
        renderizarLista()
      }

      if (typeof renderizarMapaPrincipal === 'function') {
        renderizarMapaPrincipal()
      }

      if (typeof actualizarResumen === 'function') {
        actualizarResumen()
      }

      // 4. Inicializar eventos de CRUD
      if (typeof inicializarEventosCRUD === 'function') {
        inicializarEventosCRUD()
      }

      // 5. Inicializar eventos de marcar área
      if (typeof inicializarEventosMarcarArea === 'function') {
        inicializarEventosMarcarArea()
      }
    } catch (error) {
      console.error('❌ Error en inicialización:', error)
      const listaCultivos = document.getElementById('lista-cultivos')
      if (listaCultivos) {
        listaCultivos.innerHTML = '<li class="cultivo-item-loading">Error al cargar</li>'
      }
    }
  }

  // ========== CARGAR/RECARGAR CULTIVOS ==========
  async function cargarCultivos () {
    if (!verificarSesionActiva()) {
      return
    }

    const listaCultivos = document.getElementById('lista-cultivos')
    if (listaCultivos) {
      listaCultivos.innerHTML = '<li class="cultivo-item-loading">Cargando...</li>'
    }

    try {
      const usuario = await obtenerUsuario(CORREO)

      if (!usuario) {
        cerrarSesion()
        return
      }

      window.cultivosState.usuarioData = usuario

      // ✅ LIMPIAR ANTES DE ACTUALIZAR
      window.cultivosState.cultivosData = {}

      if (Array.isArray(usuario.cultivos)) {
        window.cultivosState.cultivosData = {}
        usuario.cultivos.forEach(cultivo => {
          window.cultivosState.cultivosData[cultivo.nombre] = cultivo
        })
      }
      

      // Renderizar en UI
      if (typeof renderizarLista === 'function') {
        renderizarLista()
      }

      if (typeof renderizarMapaPrincipal === 'function') {
        renderizarMapaPrincipal()
      }

      if (typeof actualizarResumen === 'function') {
        actualizarResumen()
      }

      console.log('✅ Cultivos recargados:', Object.keys(window.cultivosState.cultivosData).length)
    } catch (error) {
      console.error('❌ Error en cargarCultivos:', error)
      if (listaCultivos) {
        listaCultivos.innerHTML = '<li class="cultivo-item-loading">Error al cargar</li>'
      }
    }
  }

  // Exponer función global para recargar
  window.recargarCultivos = cargarCultivos

  // ========== INICIAR ==========
  inicializar()
})
