/* global verificarSesionActiva, obtenerCorreoDelToken, cerrarSesion, obtenerUsuario, location, localStorage */

window.recargarCultivos = async function () {
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

  localStorage.setItem('correoUsuario', CORREO)

  // ========== ESTADO GLOBAL COMPARTIDO ==========
  window.cultivosState = {
    correo: CORREO,
    usuarioData: null,
    cultivosData: {}, // Se mantiene para acceso rápido
    cultivoSeleccionado: null,
    usuarioLatitud: -33.446,
    usuarioLongitud: -70.681,
    colores: [
      '#ef4444', '#f59e0b', '#10b981', '#3b82f6',
      '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'
    ],
    scrollInfinito: {
      paginaActual: 1,      // ✅ PAGINACIÓN SERVER
      totalPaginas: 1,      // ✅ PAGINACIÓN SERVER
      limite: 20,           // ✅ PAGINACIÓN SERVER
      totalCultivos: 0,
      cargando: false,
      todosCargados: false
    }
  }

  // ========== FUNCIÓN: FETCH PÁGINA DE CULTIVOS ==========
  window.fetchPaginaCultivos = async function (pagina = 1) {
    const { correo, scrollInfinito } = window.cultivosState
    const { limite } = scrollInfinito

    try {
      const response = await fetchConToken(
        `/usuarios/${encodeURIComponent(correo)}/cultivos?pagina=${pagina}&limite=${limite}`,
        { method: 'GET' }
      )

      if (!response.ok) {
        throw new Error('Error al obtener cultivos')
      }

      const data = await response.json()

      if (data.mensaje) {
        return { cultivos: [], paginacion: null }
      }

      return data

    } catch (error) {
      console.error('❌ Error fetchPaginaCultivos:', error)
      return { cultivos: [], paginacion: null }
    }
  }

  // ========== INICIALIZACIÓN ==========
  async function inicializar() {
    try {
      // 1. Obtener datos datos del usuario (Perfil)
      const usuario = await obtenerUsuario(CORREO)

      if (!usuario) {
        cerrarSesion()
        return
      }

      window.cultivosState.usuarioData = usuario

      if (usuario.ubicacion) {
        window.cultivosState.usuarioLatitud = usuario.ubicacion.latitud || -33.446
        window.cultivosState.usuarioLongitud = usuario.ubicacion.longitud || -70.681
      }

      // 2. Inicializar mapa principal
      if (typeof inicializarMapaPrincipal === 'function') {
        inicializarMapaPrincipal()
      }

      // 3. CARGAR PRIMERA PÁGINA (Sobrescribe cualquier dato previo)
      await window.recargarCultivos()

      // 4. Inicializar eventos de CRUD
      if (typeof inicializarEventosCRUD === 'function') {
        inicializarEventosCRUD()
      }

      // 5. Inicializar eventos de marcar área
      if (typeof inicializarEventosMarcarArea === 'function') {
        inicializarEventosMarcarArea()
      }
      // 6. Inicializar detector de scroll
      if (typeof inicializarScrollInfinito === 'function') {
        inicializarScrollInfinito()
      }

      // 7. Inicializar búsqueda de cultivos
      if (typeof inicializarBusqueda === 'function') {
        inicializarBusqueda()
      }

      // Marcar como listo
      window.cultivosCargados = true

    } catch (error) {
      console.error('❌ Error en inicialización:', error)
      const listaCultivos = document.getElementById('lista-cultivos')
      if (listaCultivos) {
        listaCultivos.innerHTML = '<li class="cultivo-item-loading">Error al cargar</li>'
      }
      // Marcar como listo
      window.cultivosCargados = true
    }
  }

  // ========== CARGAR/RECARGAR CULTIVOS (Página 1) ==========
  async function cargarCultivos() {
    if (!verificarSesionActiva()) return

    const listaCultivos = document.getElementById('lista-cultivos')

    // Mostrar loading si está vacío
    if (listaCultivos && listaCultivos.children.length === 0) {
      listaCultivos.innerHTML = '<li class="cultivo-item-loading">Cargando...</li>'
    }

    try {
      // Resetear estado paginación
      window.cultivosState.scrollInfinito.paginaActual = 1
      window.cultivosState.scrollInfinito.todosCargados = false
      window.cultivosState.scrollInfinito.cultivosCargados = 0
      window.cultivosState.cultivosData = {}

      // ✅ Resetear tracker de scroll para evitar bloqueos
      if (typeof window.resetearScrollTracker === 'function') {
        window.resetearScrollTracker()
      }

      // Fetch Página 1
      const data = await window.fetchPaginaCultivos(1)

      const nuevosCultivos = data.cultivos || []
      const paginacion = data.paginacion

      // Actualizar estado local
      nuevosCultivos.forEach(c => {
        window.cultivosState.cultivosData[c.nombre] = c
      })

      // Actualizar contadores
      if (paginacion) {
        window.cultivosState.scrollInfinito.totalCultivos = paginacion.total
        window.cultivosState.scrollInfinito.totalPaginas = paginacion.total_paginas
        window.cultivosState.scrollInfinito.todosCargados = !paginacion.tiene_siguiente
      } else {
        window.cultivosState.scrollInfinito.totalCultivos = 0
        window.cultivosState.scrollInfinito.todosCargados = true
      }

      // Renderizar UI (Página 1)
      if (typeof renderizarListaInicial === 'function') {
        renderizarListaInicial(nuevosCultivos)
      }

      if (typeof renderizarMapaPrincipal === 'function') {
        renderizarMapaPrincipal()
      }

      if (typeof actualizarResumen === 'function') {
        actualizarResumen()
      }

    } catch (error) {
      console.error('❌ Error en cargarCultivos:', error)
      if (listaCultivos) listaCultivos.innerHTML = '<li class="cultivo-item-loading">Error al cargar</li>'
    }
  }

  // Exponer función global para recargar
  window.recargarCultivos = cargarCultivos

  // ========== INICIAR ==========
  inicializar()
})
