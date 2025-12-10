/* global localStorage, location, document, ol, verificarSesionActiva, obtenerCorreoDelToken, cerrarSesion, fetchConToken, obtenerUsuario */

document.addEventListener('DOMContentLoaded', () => {
  if (!verificarSesionActiva()) {
    return
  }

  const inputUbicacion = document.getElementById('input-ubicacion')
  const mapaOverlay = document.getElementById('mapa-overlay')
  const btnCerrar = document.getElementById('cerrar-mapa')
  const btnConfirmar = document.getElementById('confirmar-ubicacion')
  const btnCancelar = document.getElementById('cancelar-ubicacion')

  let map = null
  let vectorSource = null
  let latUsuario, lonUsuario
  let correo
  let ciudad = 'Desconocida'
  let region = 'Desconocida'
  let pais = 'Desconocido'
  let latMod, lonMod

  // Mostrar mapa al hacer clic en el input
  inputUbicacion.addEventListener('click', async () => {
    if (map) {
      return
    }
    mapaOverlay.style.display = 'flex'
    correo = obtenerCorreoDelToken()

    if (!correo) {
      console.error('❌ No se pudo obtener correo del token')
      cerrarSesion()
      return
    }

    try {
      const usuario = await obtenerUsuario(correo)

      if (!usuario) {
        cerrarSesion()
        return
      }
      // 3. Extraer coordenadas
      latUsuario = usuario.ubicacion?.latitud ?? usuario.ubicacion?.lat ?? -33.446
      lonUsuario = usuario.ubicacion?.longitud ?? usuario.ubicacion?.lon ?? -70.681
    } catch (error) {
      console.error('❌ Error obteniendo usuario:', error)
      // Usar Santiago como fallback
      latUsuario = -33.446
      lonUsuario = -70.681
    }
    // Crear mapa base centrado en Chile
    map = new ol.Map({
      target: 'map',
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM()
        })
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([lonUsuario, latUsuario]), // Ubicacion
        zoom: 16
      })
    })
    // Capa para marcadores
    vectorSource = new ol.source.Vector()
    const vectorLayer = new ol.layer.Vector({ source: vectorSource })
    map.addLayer(vectorLayer)

    // Crear popup
    const popup = document.createElement('div')
    popup.className = 'ol-popup'
    const overlay = new ol.Overlay({ element: popup, positioning: 'bottom-center', stopEvent: false })
    map.addOverlay(overlay)

    // Evento de clic
    map.on('click', async function (evt) {
      const [lon, lat] = ol.proj.toLonLat(evt.coordinate)

      // Eliminar marcador anterior
      vectorSource.clear()

      // Crear nuevo marcador
      const marker = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat]))
      })
      // pointer más bonito y visible apra el usuario
      marker.setStyle(new ol.style.Style({
        image: new ol.style.Icon({
          src: 'data:image/svg+xml;utf8,' + encodeURIComponent(`
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
              <text x="16" y="24" text-anchor="middle" font-size="20" font-family="Arial">📍</text>
            </svg>
          `),
          scale: 1,
          anchor: [0.5, 1] // Punto de anclaje (centro-abajo)
        })
      }))

      vectorSource.addFeature(marker)

      // ✅ ACTUALIZAR PANEL LATERAL EN LUGAR DE POPUP
      // Referencias a elementos del panel
      const panelCiudad = document.getElementById('panel-ciudad')
      const panelRegion = document.getElementById('panel-region')
      const panelPais = document.getElementById('panel-pais')
      const panelLat = document.getElementById('panel-lat')
      const panelLon = document.getElementById('panel-lon')
      const panelStatus = document.getElementById('panel-status')

      // Mostrar coordenadas inmediatamente
      if (panelLat) panelLat.textContent = lat.toFixed(6)
      if (panelLon) panelLon.textContent = lon.toFixed(6)

      // Mostrar valores temporales mientras se carga
      if (panelCiudad) panelCiudad.textContent = 'Cargando...'
      if (panelRegion) panelRegion.textContent = 'Cargando...'
      if (panelPais) panelPais.textContent = 'Cargando...'

      // Deshabilitar botón mientras carga
      const originalText = btnConfirmar.textContent
      btnConfirmar.disabled = true
      btnConfirmar.textContent = 'Obteniendo dirección...'

      latMod = lat
      lonMod = lon

      try {
        // Petición a Nominatim
        const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10&addressdetails=1`
        const res = await fetch(url)
        const data = await res.json()

        if (data.address) {
          ciudad = data.address.city || data.address.town || data.address.village || 'Desconocida'
          region = data.address.state || 'Desconocida'
          pais = data.address.country || 'Desconocido'
        } else {
          ciudad = 'Desconocida'
          region = 'Desconocida'
          pais = 'Desconocido'
        }

        // ACTUALIZAR PANEL CON LA INFORMACIÓN
        if (panelCiudad) panelCiudad.textContent = ciudad
        if (panelRegion) panelRegion.textContent = region
        if (panelPais) panelPais.textContent = pais

      } catch (error) {
        console.error('❌ Error obteniendo información:', error)

        // Estado de error
        if (panelCiudad) panelCiudad.textContent = 'Error'
        if (panelRegion) panelRegion.textContent = 'Error'
        if (panelPais) panelPais.textContent = 'Error'

        ciudad = 'Desconocida'
        region = 'Desconocida'
      } finally {
        // Habilitar botón nuevamente
        btnConfirmar.disabled = false
        btnConfirmar.textContent = originalText || 'Confirmar Ubicación'
      }
    })
  })

  function matarMapa() {

    // 1. Remover todos los overlays y layers
    map.getOverlays().clear()
    map.getLayers().clear()

    // 2. Limpiar el target (contenedor)
    map.setTarget(null)

    // 3. Destruir la instancia
    map.dispose()
    map = null
    vectorSource = null

    // 4. Limpiar el contenedor HTML. sin el if da error
    const mapContainer = document.getElementById('map')
    if (mapContainer) {
      mapContainer.innerHTML = ''
    }
  }

  // Cerrar mapa con el botón X
  btnCerrar.addEventListener('click', () => {
    mapaOverlay.style.display = 'none'
    matarMapa()
  })

  // Cerrar mapa con confirmar
  btnConfirmar.addEventListener('click', async () => {
    // Validar que se haya seleccionado una ubicación
    if (!latMod || !lonMod) {
      alert('⚠️ Selecciona una ubicación en el mapa primero')
      return
    }

    try {
      // 1. Actualizar coordenadas (lat/lon via Body con UbicacionUsuario)
      const respuesta1 = await fetchConToken(
        `/usuarios/${encodeURIComponent(correo)}/ubicacion/modificar`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            latitud: latMod,
            longitud: lonMod
          })
        }
      )

      if (!respuesta1 || !respuesta1.ok) {
        const error1 = await respuesta1.json().catch(() => ({}))
        throw new Error(error1.error || 'Error actualizando coordenadas')
      }

      // 2. Actualizar región/ciudad
      const respuesta2 = await fetchConToken(
        `/usuarios/${encodeURIComponent(correo)}/ubicacion/region/${encodeURIComponent(region)}/${encodeURIComponent(ciudad)}/modificar`,
        {
          method: 'PATCH'
        }
      )

      if (!respuesta2 || !respuesta2.ok) {
        const error2 = await respuesta2.json().catch(() => ({}))
        throw new Error(error2.error || 'Error actualizando región/ciudad')
      }

      // INVALIDAR CACHE DE CLIMA (nueva ubicación = nuevo clima)
      if (typeof invalidarCacheClima === 'function') {
        invalidarCacheClima()
      }

      // ACTUALIZAR CACHÉ DEL USUARIO
      // ✅ FIX: Invalidar cache local para forzar a obtenerUsuario a ir al backend
      // De lo contrario, nos devuelve el usuario viejo almacenado en localStorage
      if (typeof invalidarCache === 'function') {
        invalidarCache()
      } else {
        localStorage.removeItem('usuario')
        localStorage.removeItem('ultimaActualizacion')
      }

      const usuarioActualizado = await obtenerUsuario(correo)

      if (usuarioActualizado) {
        // Actualizar localStorage
        localStorage.setItem('usuario', JSON.stringify(usuarioActualizado))

        // Actualizar window.homeState si existe (para home.html)
        if (window.homeState) {
          window.homeState.usuario = usuarioActualizado
          window.homeState.latitud = usuarioActualizado.ubicacion?.latitud || latMod
          window.homeState.longitud = usuarioActualizado.ubicacion?.longitud || lonMod
        }

        // Actualizar window.cultivosState si existe (para gestor_cultivos.html)
        if (window.cultivosState) {
          window.cultivosState.usuarioData = usuarioActualizado
          window.cultivosState.usuarioLatitud = usuarioActualizado.ubicacion?.latitud || latMod
          window.cultivosState.usuarioLongitud = usuarioActualizado.ubicacion?.longitud || lonMod
        }
      }

      // 4. Actualizar input visual
      inputUbicacion.value = `${ciudad}, ${region}`

      // 5. Cerrar overlay
      mapaOverlay.style.display = 'none'
      matarMapa()

      // detectar en que pagina se llamó
      const paginaActual = window.location.pathname

      // si es desde el perfil se actualiza la vista manualmente sin recargar
      if (paginaActual.includes('perfil.html')) {
        alert('✅ Ubicación actualizada correctamente')

        // Actualizar elementos del DOM en perfil.html
        const valorCiudad = document.getElementById('valor-cuidad') // Nota: el ID en HTML es 'valor-cuidad' (sic)
        const valorRegion = document.getElementById('valor-region')
        const inpUbicacion = document.getElementById('inp-ubicacion') // Input del form
        const inpRegion = document.getElementById('inp-region') // Input del form

        if (valorCiudad) valorCiudad.textContent = ciudad
        if (valorRegion) valorRegion.textContent = region

        // También actualizar los inputs del formulario si existen
        if (inpUbicacion) inpUbicacion.value = ciudad
        if (inpRegion) inpRegion.value = region

        return
      }

      // si es desde el home se recargan los cultivos
      if (paginaActual.includes('home.html')) {
        alert('✅ Ubicación actualizada correctamente')

        // Mostrar pantalla de carga
        const loadingScreen = document.getElementById('loadingScreen')
        if (loadingScreen) {
          loadingScreen.classList.remove('hide')
          loadingScreen.style.display = 'flex'
        }

        // Invalidar cache del clima para forzar nuevos datos
        if (typeof invalidarCacheClima === 'function') {
          invalidarCacheClima()
        }

        // Actualizar las variables de estado de clima con nuevas coordenadas
        if (typeof actualizarCoordsClima === 'function') {
          actualizarCoordsClima(latMod, lonMod)
        }

        // Recargar clima con nuevas coordenadas (ahora sin cache)
        if (typeof cargarClimaHome === 'function') {
          await cargarClimaHome(true)  // true = forzar datos frescos

          // Pequeño delay para asegurar que los datos estén frescos
          await new Promise(resolve => setTimeout(resolve, 500))

          // Explícitamente recargar consejos CON los nuevos datos
          if (typeof cargarConsejosClima === 'function') {
            await cargarConsejosClima()
          }
        }

        // Ocultar pantalla de carga después de cargar
        if (loadingScreen) {
          loadingScreen.classList.add('hide')
          setTimeout(() => {
            loadingScreen.style.display = 'none'
          }, 300)
        }

        // Recargar página para actualizar todo
        // window.location.reload()
        return
      }

      // si es desde dias.html se recarga el clima semanal
      if (paginaActual.includes('dias.html')) {
        alert('✅ Ubicación actualizada correctamente')

        // Mostrar pantalla de carga
        const loadingScreen = document.getElementById('loadingScreen')
        if (loadingScreen) {
          loadingScreen.classList.remove('hide')
          loadingScreen.style.display = 'flex'
        }

        // Invalidar cache del clima para forzar nuevos datos
        if (typeof invalidarCacheClima === 'function') {
          invalidarCacheClima()
        }

        // Actualizar las variables de estado de clima con nuevas coordenadas
        if (typeof actualizarCoordsClima === 'function') {
          actualizarCoordsClima(latMod, lonMod)
        }

        // Recargar clima semanal
        if (typeof cargarClimaSemana === 'function') {
          await cargarClimaSemana()
        }

        // Ocultar pantalla de carga después de cargar
        if (loadingScreen) {
          loadingScreen.classList.add('hide')
          setTimeout(() => {
            loadingScreen.style.display = 'none'
          }, 300)
        }
        return
      }

      alert('✅ Ubicación actualizada correctamente')
    } catch (error) {
      console.error('❌ Error actualizando ubicación:', error)
      alert(`⚠️ Error: ${error.message}`)
    }
  })

  // Cerrar mapa con cancelar
  btnCancelar.addEventListener('click', () => {
    mapaOverlay.style.display = 'none'
    matarMapa()
  })

  // Cerrar al hacer clic fuera del contenedor
  mapaOverlay.addEventListener('click', (e) => {
    if (e.target === mapaOverlay) {
      mapaOverlay.style.display = 'none'
      matarMapa()
    }
  })
})
