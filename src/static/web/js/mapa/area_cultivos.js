//marcar area de los cultivos
//  marcar el area con pinpoints en mapa y guardar esos puntos (lat y lon) en db maximo de 20 puntos por cultivo

//mostrar area de cultivos ya registrados
//  cargar puntos desde la información de los cultivos
//  iterar sobre cada punto de cada cultivo añadiendolos a estructura de area
//  estado de carga mientras se añaden los cultivos
document.addEventListener('DOMContentLoaded', () => {
  // configuracion
  const btnDeshacer = document.getElementById('btn-deshacer');
  const btnLimpiar = document.getElementById('btn-limpiar');
  const btnCompletar = document.getElementById('btn-completar');
  const puntosCount = document.getElementById('puntos-count');
  const areaSuperficie = document.getElementById('area-superficie');
  const estadoSuperficie = document.getElementById('estado-superficie');
  const panelStatus = document.getElementById('panel-status');

  const MAX_PUNTOS = 20;
  const MIN_PUNTOS = 3;

  let map = null;
  let vectorSource = null;
  let puntosMarcados = [];
  let poligonoActual = null;
  let usuarioLatitud = -33.446;
  let usuarioLongitud = -70.681;

  // inicializar
  async function inicializarMapa() {
    console.log('🗺️ Inicializando mapa de superficie...');

    // 1. Obtener ubicación del usuario
    try {
      const correo = new URLSearchParams(location.search).get('correo')
        || localStorage.getItem('correoUsuario');

      if (correo) {
        const usuario = await obtenerUsuario(correo);
        if (usuario && usuario.ubicacion) {
          usuarioLatitud = usuario.ubicacion.latitud || usuario.ubicacion.lat || -33.446;
          usuarioLongitud = usuario.ubicacion.longitud || usuario.ubicacion.lon || -70.681;
          console.log('📍 Ubicación del usuario:', usuarioLatitud, usuarioLongitud);
        }
      }
    } catch (error) {
      console.error('❌ Error obteniendo ubicación:', error);
    }

    // 2. Crear mapa centrado en ubicación del usuario
    map = new ol.Map({
      target: 'map-superficie',
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM(),
        }),
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([usuarioLongitud, usuarioLatitud]),
        zoom: 18, // Zoom alto para ver detalles del terreno
      }),
    });

    // 3. Capa para puntos y polígonos
    vectorSource = new ol.source.Vector();
    const vectorLayer = new ol.layer.Vector({
      source: vectorSource,
      style: estiloFeature
    });
    map.addLayer(vectorLayer);

    // 4. Evento de clic en el mapa
    map.on('click', manejarClicMapa);

    console.log('✅ Mapa inicializado correctamente');
  }

  // hacer click
  function manejarClicMapa(evt) {
    // Verificar límite de puntos
    if (puntosMarcados.length >= MAX_PUNTOS) {
      mostrarEstado('⚠️ Límite de puntos alcanzado (máximo 20)', 'error');
      return;
    }

    // Obtener coordenadas del clic
    const coordenadas = evt.coordinate;
    const [lon, lat] = ol.proj.toLonLat(coordenadas);

    // Agregar punto
    agregarPunto(coordenadas, lat, lon);

    // Actualizar polígono si hay suficientes puntos
    if (puntosMarcados.length >= MIN_PUNTOS) {
      actualizarPoligono();
    }

    // Actualizar UI
    actualizarInterfaz();

    console.log(`📍 Punto ${puntosMarcados.length} agregado:`, lat.toFixed(6), lon.toFixed(6));
  }

  // agregar punto
  function agregarPunto(coordenadas, lat, lon) {
    // Crear feature del punto
    const punto = new ol.Feature({
      geometry: new ol.geom.Point(coordenadas),
      tipo: 'punto',
      orden: puntosMarcados.length,
      lat: lat,
      lon: lon
    });

    vectorSource.addFeature(punto);
    puntosMarcados.push({
      feature: punto,
      coordenadas: coordenadas,
      lat: lat,
      lon: lon
    });
  }

  // actualizar poligono
  function actualizarPoligono() {
    // Eliminar polígono anterior si existe
    if (poligonoActual) {
      vectorSource.removeFeature(poligonoActual);
    }

    // Crear nuevo polígono con los puntos actuales
    const coordenadasPoligono = puntosMarcados.map(p => p.coordenadas);
    
    poligonoActual = new ol.Feature({
      geometry: new ol.geom.Polygon([coordenadasPoligono]),
      tipo: 'poligono'
    });

    vectorSource.addFeature(poligonoActual);

    // Calcular área
    calcularArea();
  }

  // calcular hectareas
  function calcularArea() {
    if (!poligonoActual) return;

    const geometria = poligonoActual.getGeometry();
    const areaMetros = ol.sphere.getArea(geometria, { projection: 'EPSG:3857' });
    
    // Actualizar UI con el área
    if (areaSuperficie) {
      if (areaMetros < 10000) {
        areaSuperficie.textContent = `${Math.round(areaMetros)} m²`;
      } else {
        areaSuperficie.textContent = `${(areaMetros / 10000).toFixed(2)} ha`;
      }
    }

    console.log('📏 Área calculada:', areaMetros, 'm²');
  }

  // estilos que no son de openlayers
  function estiloFeature(feature) {
    const tipo = feature.get('tipo');

    if (tipo === 'punto') {
      return new ol.style.Style({
        image: new ol.style.Circle({
          radius: 6,
          fill: new ol.style.Fill({ color: '#ef4444' }),
          stroke: new ol.style.Stroke({ color: '#ffffff', width: 2 })
        }),
        text: new ol.style.Text({
          text: String(feature.get('orden') + 1),
          font: 'bold 10px sans-serif',
          fill: new ol.style.Fill({ color: '#ffffff' }),
          offsetY: -12
        })
      });
    }

    if (tipo === 'poligono') {
      return new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: '#667eea',
          width: 3
        }),
        fill: new ol.style.Fill({
          color: 'rgba(102, 126, 234, 0.2)'
        })
      });
    }
  }

  // actualizar interfaz
  function actualizarInterfaz() {
    const numPuntos = puntosMarcados.length;

    // Actualizar contador
    if (puntosCount) {
      puntosCount.textContent = `${numPuntos} / ${MAX_PUNTOS}`;
    }

    // Actualizar estado
    if (estadoSuperficie) {
      if (numPuntos === 0) {
        estadoSuperficie.textContent = 'Sin marcar';
      } else if (numPuntos < MIN_PUNTOS) {
        estadoSuperficie.textContent = 'En progreso';
      } else {
        estadoSuperficie.textContent = 'Área marcada';
      }
    }

    // Habilitar/deshabilitar botones
    if (btnDeshacer) btnDeshacer.disabled = numPuntos === 0;
    if (btnLimpiar) btnLimpiar.disabled = numPuntos === 0;
    if (btnCompletar) btnCompletar.disabled = numPuntos < MIN_PUNTOS;

    // Actualizar mensaje de estado
    if (panelStatus) {
      if (numPuntos === 0) {
        mostrarEstado('👆 Haz clic en el mapa para marcar los límites de tu cultivo', 'info');
      } else if (numPuntos < MIN_PUNTOS) {
        mostrarEstado(`📍 Marca al menos ${MIN_PUNTOS} puntos para crear el área`, 'info');
      } else if (numPuntos >= MIN_PUNTOS && numPuntos < MAX_PUNTOS) {
        mostrarEstado('✅ Puedes agregar más puntos o completar el área', 'success');
      } else {
        mostrarEstado('⚠️ Límite de puntos alcanzado. Completa el área.', 'error');
      }
    }
  }

  // estado en el panel
  function mostrarEstado(mensaje, tipo = 'info') {
    if (panelStatus) {
      panelStatus.textContent = mensaje;
      panelStatus.className = `panel-status ${tipo}`;
    }
  }

  // quitar ultimo punto
  function deshacerUltimoPunto() {
    if (puntosMarcados.length === 0) return;

    // Remover último punto
    const ultimoPunto = puntosMarcados.pop();
    vectorSource.removeFeature(ultimoPunto.feature);

    // Actualizar polígono
    if (puntosMarcados.length >= MIN_PUNTOS) {
      actualizarPoligono();
    } else if (poligonoActual) {
      vectorSource.removeFeature(poligonoActual);
      poligonoActual = null;
      if (areaSuperficie) areaSuperficie.textContent = '0 m²';
    }

    actualizarInterfaz();
    console.log('↩️ Último punto eliminado');
  }

  // quitar todos los puntos
  function limpiarTodo() {
    vectorSource.clear();
    puntosMarcados = [];
    poligonoActual = null;
    
    if (areaSuperficie) areaSuperficie.textContent = '0 m²';
    
    actualizarInterfaz();
    console.log('🗑️ Mapa limpiado');
  }

  // completar el area con al menos 3 puntos
  async function completarArea() {
    if (puntosMarcados.length < MIN_PUNTOS) {
      mostrarEstado('⚠️ Necesitas al menos 3 puntos para completar el área', 'error');
      return;
    }

    try {
      // Preparar datos para enviar al backend
      const datosSuperficie = {
        puntos: puntosMarcados.map(p => ({
          latitud: p.lat,
          longitud: p.lon
        })),
        area: poligonoActual ? ol.sphere.getArea(poligonoActual.getGeometry(), { projection: 'EPSG:3857' }) : 0,
        fecha: new Date().toISOString()
      };

      console.log('💾 Guardando superficie...', datosSuperficie);

      // TODO: Enviar al backend
      // const correo = localStorage.getItem('correoUsuario');
      // await fetch('/usuarios/superficie', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ correo, superficie: datosSuperficie })
      // });

      mostrarEstado('✅ Área guardada correctamente', 'success');
      console.log('✅ Superficie completada y guardada');

    } catch (error) {
      console.error('❌ Error guardando superficie:', error);
      mostrarEstado('❌ Error al guardar el área', 'error');
    }
  }

  // event listeners
  if (btnDeshacer) {
    btnDeshacer.addEventListener('click', deshacerUltimoPunto);
  }

  if (btnLimpiar) {
    btnLimpiar.addEventListener('click', () => {
      if (confirm('¿Estás seguro de que quieres limpiar todo el área marcada?')) {
        limpiarTodo();
      }
    });
  }

  if (btnCompletar) {
    btnCompletar.addEventListener('click', completarArea);
  }

  //inicializar el mapa al abrir
  inicializarMapa();
});