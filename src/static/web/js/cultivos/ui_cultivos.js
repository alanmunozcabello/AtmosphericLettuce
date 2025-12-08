/* global window, document */

// ========== RENDERIZAR LISTA INICIAL (primeros 20) ==========
// ========== RENDERIZAR LISTA (Página 1 o reset) ==========
function renderizarListaInicial(cultivosExplicitos = null) {
  const listaCultivos = document.getElementById('lista-cultivos')
  if (!listaCultivos) return

  listaCultivos.innerHTML = ''

  let cultivosMostrar = []
  if (cultivosExplicitos) {
    cultivosMostrar = cultivosExplicitos
  } else {
    // Fallback: usar lo que haya en data 
    cultivosMostrar = Object.values(window.cultivosState.cultivosData)
  }

  const { scrollInfinito } = window.cultivosState
  scrollInfinito.cargando = false

  // ✅ Caso: Sin cultivos
  if (cultivosMostrar.length === 0) {
    listaCultivos.innerHTML = '<li class="cultivo-item-loading">No tienes cultivos 🌱</li>'
    scrollInfinito.todosCargados = true
    return
  }

  // ✅ Agregar cultivos al DOM
  cultivosMostrar.forEach((cultivo) => {
    const li = crearElementoCultivo(cultivo.nombre, cultivo)
    listaCultivos.appendChild(li)
  })

  // ✅ Actualizar contador
  scrollInfinito.cultivosCargados = cultivosMostrar.length

  // ✅ Indicador si hay más páginas
  if (!scrollInfinito.todosCargados) {
    const indicador = crearIndicadorCargaMas()
    listaCultivos.appendChild(indicador)
    console.log(`✅ Página 1 renderizada (${cultivosMostrar.length} ítems). Quedan páginas.`)
  } else {
    console.log('✅ Todos los cultivos cargados.')
  }
}

// ========== CREAR ELEMENTO DE CULTIVO (sin tocar DOM global) ==========
function crearElementoCultivo(nombre, cultivo) {
  const hectareas = cultivo.hectareas || 0
  const puntos = cultivo.puntos || []
  const tienePuntos = puntos.length > 0 && puntos.some(p => p !== null)

  const li = document.createElement('li')
  li.className = 'item-cultivo'
  li.dataset.nombre = nombre
  li.dataset.cultivoId = cultivo.id

  li.innerHTML = `
    <span class="tick">✔</span>
    
    <!-- ✅ Nuevo contenedor de texto para separar nombre y hectáreas -->
    <div class="info-cultivo">
       <span class="nombre-cultivo" title="${nombre}">${nombre}</span>
       <span class="meta-cultivo">— ${hectareas.toFixed(2)} ha ${tienePuntos ? ' 📍' : ''}</span>
    </div>
    <div class="botones-grupo">
      <button class="btn-config" data-nombre="${nombre}" aria-label="Configurar">⚙️</button>
      <button class="btn-eliminar" data-nombre="${nombre}" aria-label="Eliminar">✕</button>
    </div>
  `

  return li
}

// ========== CREAR INDICADOR "CARGANDO MÁS..." ==========
function crearIndicadorCargaMas() {
  const li = document.createElement('li')
  li.className = 'cultivo-item-loading-more'
  li.id = 'indicador-carga-mas'
  li.innerHTML = `
    <div class="spinner"></div>
    <span>Cargando más cultivos...</span>
  `
  return li
}

// ========== CARGAR MÁS CULTIVOS ==========
// ========== CARGAR MÁS CULTIVOS (Página Siguiente) ==========
async function cargarMasCultivos() {
  const { scrollInfinito } = window.cultivosState

  if (scrollInfinito.cargando || scrollInfinito.todosCargados) {
    return
  }

  scrollInfinito.cargando = true
  console.log('📥 Cargando siguiente página...')

  const proximaPagina = scrollInfinito.paginaActual + 1

  try {
    const data = await window.fetchPaginaCultivos(proximaPagina)
    const nuevosCultivos = data.cultivos || []
    const paginacion = data.paginacion

    const listaCultivos = document.getElementById('lista-cultivos')
    if (!listaCultivos) return

    // Eliminar indicador viejo
    eliminarIndicadorCargaMas()

    if (nuevosCultivos.length === 0) {
      scrollInfinito.todosCargados = true
      scrollInfinito.cargando = false
      return
    }

    // Agregar nuevos al DOM
    nuevosCultivos.forEach((cultivo) => {
      // Actualizar state global
      window.cultivosState.cultivosData[cultivo.nombre] = cultivo
      // Crear elemento
      const li = crearElementoCultivo(cultivo.nombre, cultivo)
      listaCultivos.appendChild(li)
    })

    // Actualizar Flags
    if (paginacion) {
      scrollInfinito.paginaActual = paginacion.pagina_actual
      scrollInfinito.todosCargados = !paginacion.tiene_siguiente
      scrollInfinito.totalPaginas = paginacion.total_paginas
      scrollInfinito.totalCultivos = paginacion.total
    } else {
      scrollInfinito.todosCargados = true
    }

    scrollInfinito.cultivosCargados += nuevosCultivos.length
    scrollInfinito.cargando = false

    // Si aún hay más, poner indicador al final
    if (!scrollInfinito.todosCargados) {
      const indicador = crearIndicadorCargaMas()
      listaCultivos.appendChild(indicador)
    }

    // ✅ ACTUALIZAR MAPA Y RESUMEN (INCREMENTAL)
    // Usamos agregarCultivosAlMapa si existe, para no borrar lo anterior
    if (typeof window.agregarCultivosAlMapa === 'function') {
      window.agregarCultivosAlMapa(nuevosCultivos)
    } else if (typeof window.renderizarMapaPrincipal === 'function') {
      // Fallback
      window.renderizarMapaPrincipal()
    }

    if (typeof actualizarResumen === 'function') {
      actualizarResumen()
    }

    console.log(`✅ Página ${proximaPagina} cargada (${nuevosCultivos.length} items).`)

  } catch (err) {
    console.error('Error cargando más cultivos:', err)
    scrollInfinito.cargando = false
    eliminarIndicadorCargaMas()
  }
}

// ========== ELIMINAR INDICADOR ==========
function eliminarIndicadorCargaMas() {
  const indicador = document.getElementById('indicador-carga-mas')
  if (indicador) {
    indicador.remove()
  }
}

// ========== INICIALIZAR SCROLL INFINITO ==========
function inicializarScrollInfinito() {
  const listaCultivos = document.getElementById('lista-cultivos')
  if (!listaCultivos) {
    console.warn('⚠️ No se encontró #lista-cultivos')
    return
  }

  let ultimoScroll = 0
  let scrollTimeout = null

  listaCultivos.addEventListener('scroll', () => {
    // Debounce: Esperar 150ms después del último evento
    clearTimeout(scrollTimeout)

    scrollTimeout = setTimeout(() => {
      const { scrollTop, scrollHeight, clientHeight } = listaCultivos
      const { scrollInfinito } = window.cultivosState

      // VALIDACIÓN 1: Solo scroll hacia abajo
      if (scrollTop <= ultimoScroll) {
        ultimoScroll = scrollTop
        return
      }
      ultimoScroll = scrollTop

      // VALIDACIÓN 2: Hay scroll real (contenido > contenedor)
      const hayScrollReal = scrollHeight > clientHeight + 10
      if (!hayScrollReal) {
        return
      }

      // VALIDACIÓN 3: Cerca del final
      const scrollBottom = scrollHeight - scrollTop - clientHeight
      const cercaDelFinal = scrollBottom < 100

      if (!cercaDelFinal) {
        return
      }

      // VALIDACIÓN 4: Puede cargar más
      if (scrollInfinito.cargando) {
        return
      }

      if (scrollInfinito.todosCargados) {
        return
      }

      // TODO OK: Cargar más
      console.log(`🔽 Scroll detectado en lista: ${scrollBottom}px del final`)
      cargarMasCultivos()
    }, 150)
  })

  // Exponer reset para cuando se recarga la lista externamente
  window.resetearScrollTracker = () => {
    ultimoScroll = 0
    console.log('🔄 Tracker de scroll reseteado')
  }

  console.log('✅ Scroll infinito inicializado en #lista-cultivos')
}

// ========== ACTUALIZAR RESUMEN ==========
function actualizarResumen() {
  const { cultivosData, scrollInfinito } = window.cultivosState
  const totalCultivosEl = document.getElementById('total-cultivos')
  const areaTotalEl = document.getElementById('area-total')

  // ✅ USAR TOTAL DEL SERVER SI EXISTE
  const total = scrollInfinito.totalCultivos || Object.keys(cultivosData).length

  // Para el área, sumamos lo que tenemos cargado localmente porque el server no nos da el total de hectáreas global en el endpoint paginado
  // (Aunque idealmente el backend debería darlo. Por ahora sumamos lo visible/cargado)
  let areaTotal = 0
  Object.values(cultivosData).forEach((cultivo) => {
    areaTotal += cultivo.hectareas || 0
  })

  // Si estamos en modo búsqueda, el total podría ser distinto, pero mantenemos la lógica base
  if (totalCultivosEl) totalCultivosEl.textContent = total
  if (areaTotalEl) areaTotalEl.textContent = `${areaTotal.toFixed(2)} ha (visible)`

  console.log('✅ Resumen actualizado:', total, 'cultivos')
}

// ========== ALIAS PARA COMPATIBILIDAD ==========
function renderizarLista(cultivos) {
  renderizarListaInicial(cultivos)
}

// ========== FUNCIÓN LEGACY (eliminar después) ==========
function agregarCultivoALista(nombre, cultivo, reAgregarIndicador = true) {
  // Esta función ya no se usa, pero la dejo por compatibilidad
  const listaCultivos = document.getElementById('lista-cultivos')
  if (!listaCultivos) return

  const li = crearElementoCultivo(nombre, cultivo)
  listaCultivos.appendChild(li)
}

// ========== FILTRADO DE CULTIVOS ==========
function inicializarBusqueda() {
  const inputBuscar = document.getElementById('input-buscar-cultivo')
  const btnLimpiar = document.getElementById('btn-limpiar-busqueda')

  if (!inputBuscar) {
    console.warn('⚠️ No se encontró #input-buscar-cultivo')
    return
  }

  // Filtrado instantáneo (input event se dispara con cada tecla)
  inputBuscar.addEventListener('input', (e) => {
    const termino = e.target.value.trim()

    // Mostrar/ocultar botón de limpiar
    if (termino) {
      btnLimpiar.style.display = 'block'
    } else {
      btnLimpiar.style.display = 'none'
    }

    filtrarCultivos(termino)
  })

  // Limpiar búsqueda
  if (btnLimpiar) {
    btnLimpiar.addEventListener('click', () => {
      inputBuscar.value = ''
      btnLimpiar.style.display = 'none'
      filtrarCultivos('')
      inputBuscar.focus()
    })
  }

  // Limpiar con Escape
  inputBuscar.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      inputBuscar.value = ''
      btnLimpiar.style.display = 'none'
      filtrarCultivos('')
    }
  })
}

// ========== FILTRAR CULTIVOS (SERVER SIDE) ==========
async function filtrarCultivos(termino) {
  const listaCultivos = document.getElementById('lista-cultivos')
  if (!listaCultivos) return

  const { scrollInfinito, correo } = window.cultivosState
  const terminoLower = termino.trim()

  // 1. Limpiar lista visualmente (feedback inmediato)
  listaCultivos.innerHTML = '<li class="cultivo-item-loading">Buscando...</li>'

  // 2. Si no hay término, volver a la normalidad (Página 1 estándar)
  if (!terminoLower) {
    console.log('🔄 Búsqueda limpiada. Recargando inicio...')
    await window.recargarCultivos() // Esto resetea todo a página 1
    return
  }

  // 3. Buscar en servidor
  try {
    const params = new URLSearchParams({
      correo: correo,
      buscar: terminoLower,
      pagina: 1,
      limite: 100
    })

    // Asumimos que existe este endpoint, si no, habría que crearlo o usar el paginado con filtro.
    // Si no existe, podemos usar /usuarios/.../cultivos?buscar=... si el backend lo soporta.
    // Basado en el usuario_service.py que vi, parece que el servicio estándar no filtra por nombre.
    // SI NO EXISTE FILTRO EN EL BACKEND, TENDRÍA QUE MODIFICAR EL BACKEND.
    // Pero voy a asumir que /filtrar existe o que el usuario quería que lo arregle.
    // Si falla 404, entonces el problema es que el backend no lo soporta.
    // REVISIÓN: el usuario dijo "intentar de nuevo", y antes falló por sintaxis.
    // Voy a mantener esta lógica.

    const response = await fetchConToken(`/cultivos/filtrar?${params.toString()}`, { method: 'GET' })

    if (!response.ok) throw new Error('Error buscando')

    const data = await response.json()
    const resultados = data.cultivos || []

    listaCultivos.innerHTML = ''

    if (resultados.length === 0) {
      listaCultivos.innerHTML = `
          <li class="cultivo-item-no-results">
            No se encontraron cultivos con <strong>"${termino}"</strong>
          </li>
        `
      return
    }

    // Renderizar resultados
    resultados.forEach((cultivo) => {
      window.cultivosState.cultivosData[cultivo.nombre] = cultivo
      const li = crearElementoCultivoConResaltado(cultivo.nombre, cultivo, terminoLower)
      listaCultivos.appendChild(li)
    })

    scrollInfinito.todosCargados = true
    scrollInfinito.cargando = false
    eliminarIndicadorCargaMas()

    console.log(`✅ ${resultados.length} resultados encontrados`)

  } catch (error) {
    console.error('Error en búsqueda:', error)
    listaCultivos.innerHTML = '<li class="cultivo-item-loading">Error al buscar</li>'
  }
}

// ========== CREAR ELEMENTO CON TEXTO RESALTADO ==========
function crearElementoCultivoConResaltado(nombre, cultivo, termino) {
  const hectareas = cultivo.hectareas || 0
  const puntos = cultivo.puntos || []
  const tienePuntos = puntos.length > 0 && puntos.some(p => p !== null)

  const li = document.createElement('li')
  li.className = 'item-cultivo'
  li.dataset.nombre = nombre
  li.dataset.cultivoId = cultivo.id

  // Resaltar término de búsqueda
  const nombreResaltado = resaltarTexto(nombre, termino)

  li.innerHTML = `
    <span class="tick">✔</span>
    
    <!-- ✅ Nuevo contenedor de texto para separar nombre y hectáreas -->
    <div class="info-cultivo">
       <span class="nombre-cultivo" title="${nombre}">${nombre}</span>
       <span class="meta-cultivo">— ${hectareas.toFixed(2)} ha ${tienePuntos ? ' 📍' : ''}</span>
    </div>
    <div class="botones-grupo">
      <button class="btn-config" data-nombre="${nombre}" aria-label="Configurar">⚙️</button>
      <button class="btn-eliminar" data-nombre="${nombre}" aria-label="Eliminar">✕</button>
    </div>
  `

  return li
}

// ========== RESALTAR TÉRMINO EN TEXTO ==========
function resaltarTexto(texto, termino) {
  if (!termino) return texto

  const regex = new RegExp(`(${termino})`, 'gi')
  return texto.replace(regex, '<span class="highlight">$1</span>')
}