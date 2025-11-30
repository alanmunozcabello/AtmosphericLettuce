/* global window, document */

// ========== RENDERIZAR LISTA INICIAL (primeros 20) ==========
function renderizarListaInicial () {
  const listaCultivos = document.getElementById('lista-cultivos')
  if (!listaCultivos) return

  listaCultivos.innerHTML = ''

  const { cultivosData, scrollInfinito } = window.cultivosState
  const entries = Object.entries(cultivosData)
  const totalCultivos = entries.length

  // ✅ Resetear flags PRIMERO
  scrollInfinito.cargando = false
  scrollInfinito.todosCargados = false
  scrollInfinito.cultivosCargados = 0

  // ✅ Caso: Sin cultivos
  if (totalCultivos === 0) {
    listaCultivos.innerHTML = '<li class="cultivo-item-loading">No tienes cultivos 🌱</li>'
    scrollInfinito.todosCargados = true
    console.log('ℹ️ No hay cultivos')
    return
  }

  // ✅ Determinar cuántos cargar
  const cantidadACargar = Math.min(scrollInfinito.cultivosPorCarga, totalCultivos)
  const cultivosIniciales = entries.slice(0, cantidadACargar)
  
  // ✅ Agregar cultivos al DOM
  cultivosIniciales.forEach(([nombre, cultivo]) => {
    const li = crearElementoCultivo(nombre, cultivo)
    listaCultivos.appendChild(li)
  })

  // ✅ Actualizar estado
  scrollInfinito.cultivosCargados = cantidadACargar

  // ✅ CRÍTICO: Determinar si hay más por cargar
  const hayMasCultivos = cantidadACargar < totalCultivos

  if (hayMasCultivos) {
    // Hay más cultivos pendientes
    scrollInfinito.todosCargados = false
    const indicador = crearIndicadorCargaMas()
    listaCultivos.appendChild(indicador)
    console.log(`✅ ${cantidadACargar} de ${totalCultivos} cultivos cargados inicialmente`)
    console.log(`📥 Quedan ${totalCultivos - cantidadACargar} cultivos por cargar`)
  } else {
    // Ya se cargaron todos
    scrollInfinito.todosCargados = true
    console.log(`✅ ${cantidadACargar} de ${totalCultivos} cultivos cargados`)
    console.log('✅ Todos los cultivos ya están cargados')
  }
}

// ========== CREAR ELEMENTO DE CULTIVO (sin tocar DOM global) ==========
function crearElementoCultivo (nombre, cultivo) {
  const hectareas = cultivo.hectareas || 0
  const puntos = cultivo.puntos || []
  const tienePuntos = puntos.length > 0 && puntos.some(p => p !== null)

  const li = document.createElement('li')
  li.className = 'item-cultivo'
  li.dataset.nombre = nombre
  li.dataset.cultivoId = cultivo.id

  li.innerHTML = `
    <span class="tick">✔</span>
    <span>
      <strong>${nombre}</strong> — ${hectareas.toFixed(2)} ha
      ${tienePuntos ? ' 📍' : ''}
    </span>
    <div class="botones-grupo">
      <button class="btn-config" data-nombre="${nombre}" aria-label="Configurar">⚙️</button>
      <button class="btn-eliminar" data-nombre="${nombre}" aria-label="Eliminar">✕</button>
    </div>
  `

  return li
}

// ========== CREAR INDICADOR "CARGANDO MÁS..." ==========
function crearIndicadorCargaMas () {
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
function cargarMasCultivos () {
  const { cultivosData, scrollInfinito } = window.cultivosState

  // Validaciones más estrictas
  if (scrollInfinito.cargando) {
    console.log('⏸️ Ya está cargando cultivos...')
    return
  }

  if (scrollInfinito.todosCargados) {
    console.log('⏸️ Todos los cultivos ya están cargados')
    return
  }

  const entries = Object.entries(cultivosData)
  const totalCultivos = entries.length

  // Validar que realmente hay más por cargar
  if (scrollInfinito.cultivosCargados >= totalCultivos) {
    console.log('⏸️ No hay más cultivos por cargar')
    scrollInfinito.todosCargados = true
    eliminarIndicadorCargaMas()
    return
  }

  // Marcar como cargando ANTES de hacer setTimeout
  scrollInfinito.cargando = true
  console.log('📥 Cargando más cultivos...')

  // Calcular siguiente batch
  const inicio = scrollInfinito.cultivosCargados
  const fin = Math.min(inicio + scrollInfinito.cultivosPorCarga, totalCultivos)
  const siguientesBatch = entries.slice(inicio, fin)

  console.log(`📊 Cargando cultivos ${inicio + 1}-${fin} de ${totalCultivos}`)

  // Validar que hay cultivos en el batch
  if (siguientesBatch.length === 0) {
    console.log('⚠️ Batch vacío, marcando como completado')
    scrollInfinito.todosCargados = true
    scrollInfinito.cargando = false
    eliminarIndicadorCargaMas()
    return
  }

  // Simular delay 
  setTimeout(() => {
    const listaCultivos = document.getElementById('lista-cultivos')
    if (!listaCultivos) {
      console.error('❌ No se encontró #lista-cultivos')
      scrollInfinito.cargando = false
      return
    }

    // Eliminar indicador antes de agregar
    eliminarIndicadorCargaMas()

    // Agregar nuevos cultivos
    siguientesBatch.forEach(([nombre, cultivo]) => {
      const li = crearElementoCultivo(nombre, cultivo)
      listaCultivos.appendChild(li)
    })

    // Actualizar contador
    scrollInfinito.cultivosCargados = fin

    console.log(`✅ ${siguientesBatch.length} cultivos agregados (${scrollInfinito.cultivosCargados}/${totalCultivos})`)

    // Verificar si quedan más por cargar
    if (scrollInfinito.cultivosCargados >= totalCultivos) {
      scrollInfinito.todosCargados = true
      scrollInfinito.cargando = false // Desmarcar ANTES de eliminar indicador
      console.log('✅ Todos los cultivos cargados')
    } else {
      // Re-agregar indicador al final
      const indicador = crearIndicadorCargaMas()
      listaCultivos.appendChild(indicador)
      scrollInfinito.cargando = false // Desmarcar DESPUÉS de agregar indicador
      console.log(`📄 Quedan ${totalCultivos - scrollInfinito.cultivosCargados} cultivos más`)
    }
  }, 200) // Delay de 200ms
}

// ========== ELIMINAR INDICADOR ==========
function eliminarIndicadorCargaMas () {
  const indicador = document.getElementById('indicador-carga-mas')
  if (indicador) {
    indicador.remove()
  }
}

// ========== INICIALIZAR SCROLL INFINITO ==========
function inicializarScrollInfinito () {
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

  console.log('✅ Scroll infinito inicializado en #lista-cultivos')
}

// ========== ACTUALIZAR RESUMEN ==========
function actualizarResumen () {
  const { cultivosData } = window.cultivosState
  const totalCultivosEl = document.getElementById('total-cultivos')
  const areaTotalEl = document.getElementById('area-total')

  const total = Object.keys(cultivosData).length
  let areaTotal = 0

  Object.values(cultivosData).forEach((cultivo) => {
    areaTotal += cultivo.hectareas || 0
  })

  if (totalCultivosEl) totalCultivosEl.textContent = total
  if (areaTotalEl) areaTotalEl.textContent = `${areaTotal.toFixed(2)} ha`

  console.log('✅ Resumen actualizado:', total, 'cultivos,', areaTotal.toFixed(2), 'ha')
}

// ========== ALIAS PARA COMPATIBILIDAD ==========
function renderizarLista () {
  renderizarListaInicial()
}

// ========== FUNCIÓN LEGACY (eliminar después) ==========
function agregarCultivoALista (nombre, cultivo, reAgregarIndicador = true) {
  // Esta función ya no se usa, pero la dejo por compatibilidad
  const listaCultivos = document.getElementById('lista-cultivos')
  if (!listaCultivos) return

  const li = crearElementoCultivo(nombre, cultivo)
  listaCultivos.appendChild(li)
}