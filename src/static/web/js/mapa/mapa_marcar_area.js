// ========== VARIABLES DEL MAPA DE MARCAR ÁREA ==========
let mapSuperficie = null;
let vectorSourceSuperficie = null;
let puntosMarcados = [];
let poligonoActual = null;

const MAX_PUNTOS = 20;
const MIN_PUNTOS = 3;

// ========== INICIALIZAR EVENTOS ==========
function inicializarEventosMarcarArea() {
  const btnMarcar = document.getElementById('btn-marcar-area');
  const btnCerrar = document.getElementById('cerrar-overlay-marcar');
  const btnDeshacer = document.getElementById('btn-deshacer');
  const btnLimpiar = document.getElementById('btn-limpiar');
  const btnCompletar = document.getElementById('btn-completar');

  if (btnMarcar) {
    btnMarcar.addEventListener('click', abrirOverlayMarcar);
  }

  if (btnCerrar) {
    btnCerrar.addEventListener('click', cerrarOverlayMarcar);
  }

  if (btnDeshacer) {
    btnDeshacer.addEventListener('click', deshacerUltimoPunto);
  }

  if (btnLimpiar) {
    btnLimpiar.addEventListener('click', limpiarPuntos);
  }

  if (btnCompletar) {
    btnCompletar.addEventListener('click', guardarArea);
  }

  console.log('✅ Eventos de marcar área inicializados');
}

// ========== ABRIR OVERLAY ==========
function abrirOverlayMarcar() {
  const { cultivoSeleccionado, cultivosData } = window.cultivosState;

  if (!cultivoSeleccionado || !cultivosData[cultivoSeleccionado]) {
    alert('⚠️ Selecciona un cultivo primero');
    return;
  }

  const overlay = document.getElementById('overlay-marcar-area');
  if (overlay) {
    overlay.style.display = 'flex';
  }

  setTimeout(() => {
    inicializarMapaMarcarArea();
  }, 100);
}

// ========== CERRAR OVERLAY ==========
function cerrarOverlayMarcar() {
  // limpiar cultivo seleccionado
  window.cultivosState.cultivoSeleccionado = null;

  const overlay = document.getElementById('overlay-marcar-area');
  if (overlay) {
    overlay.style.display = 'none';
  }

  // Destruir mapa
  if (mapSuperficie) {
    mapSuperficie.setTarget(null);
    mapSuperficie = null;
    vectorSourceSuperficie = null;
    puntosMarcados = [];
    poligonoActual = null;
  }
}

// ========== INICIALIZAR MAPA ==========
function inicializarMapaMarcarArea() {
  const { cultivoSeleccionado, cultivosData, usuarioLatitud, usuarioLongitud } = window.cultivosState;

  console.log('🗺️ Inicializando mapa de marcar área para:', cultivoSeleccionado);

  // Actualizar UI
  const cultivoActual = document.getElementById('cultivo-actual');
  if (cultivoActual) {
    cultivoActual.textContent = cultivoSeleccionado;
  }

  // Limpiar estado
  puntosMarcados = [];
  poligonoActual = null;

  // Destruir mapa anterior
  if (mapSuperficie) {
    mapSuperficie.setTarget(null);
  }

  const cultivoData = cultivosData[cultivoSeleccionado];
  let centroLat = usuarioLatitud;
  let centroLon = usuarioLongitud;

  // ✅ Cargar puntos existentes ANTES de crear el mapa
  let puntosExistentes = [];
  if (cultivoData && cultivoData.puntos && cultivoData.puntos.length > 0) {
    puntosExistentes = cultivoData.puntos.filter(p => 
      p !== null && 
      p.latitud != null && 
      p.longitud != null &&
      !isNaN(p.latitud) &&
      !isNaN(p.longitud)
    );

    // Calcular centro si hay puntos válidos
    if (puntosExistentes.length > 0) {
      const sumLat = puntosExistentes.reduce((sum, p) => sum + p.latitud, 0);
      const sumLon = puntosExistentes.reduce((sum, p) => sum + p.longitud, 0);
      
      centroLat = sumLat / puntosExistentes.length;
      centroLon = sumLon / puntosExistentes.length;
      
      console.log('📍 Centrando en cultivo existente:', centroLat.toFixed(6), centroLon.toFixed(6));
    }
  }

  // Crear mapa
  mapSuperficie = new ol.Map({
    target: 'map-superficie',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM(),
      }),
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([centroLon, centroLat]),
      zoom: 18,
    }),
  });

  // Capa vectorial
  vectorSourceSuperficie = new ol.source.Vector();
  const vectorLayer = new ol.layer.Vector({
    source: vectorSourceSuperficie,
    style: estiloFeatureSuperficie,
  });
  mapSuperficie.addLayer(vectorLayer);

  // cargar polígono existente y agregar puntos al array puntosMarcados
  if (puntosExistentes.length >= 3) {
    puntosExistentes.forEach((p) => {
      const coord = ol.proj.fromLonLat([p.longitud, p.latitud]);
      agregarPuntoSuperficie(coord, p.latitud, p.longitud);
    });
    actualizarPoligonoSuperficie();
  }

  actualizarInterfazMarcar();

  // Eventos
  mapSuperficie.on('click', manejarClicMapaSuperficie);

  console.log('✅ Mapa de marcar área listo con', puntosMarcados.length, 'puntos');
}

// ========== MANEJADOR DE CLIC ==========
function manejarClicMapaSuperficie(evt) {
  if (puntosMarcados.length >= MAX_PUNTOS) {
    mostrarEstadoMarcar('⚠️ Límite de 20 puntos alcanzado', 'error');
    return;
  }

  const coordenadas = evt.coordinate;
  const [lon, lat] = ol.proj.toLonLat(coordenadas);

  agregarPuntoSuperficie(coordenadas, lat, lon);

  if (puntosMarcados.length >= MIN_PUNTOS) {
    actualizarPoligonoSuperficie();
  }

  actualizarInterfazMarcar();
}

// ========== AGREGAR PUNTO ==========
function agregarPuntoSuperficie(coordenadas, lat, lon) {
  const punto = new ol.Feature({
    geometry: new ol.geom.Point(coordenadas),
    tipo: 'punto',
    orden: puntosMarcados.length,
    lat: lat,
    lon: lon,
  });

  vectorSourceSuperficie.addFeature(punto);
  puntosMarcados.push({
    feature: punto,
    coordenadas: coordenadas,
    lat: lat,
    lon: lon,
  });
}

// ========== ACTUALIZAR POLÍGONO ==========
function actualizarPoligonoSuperficie() {
  if (poligonoActual) {
    vectorSourceSuperficie.removeFeature(poligonoActual);
  }

  const coordenadasPoligono = puntosMarcados.map((p) => p.coordenadas);

  poligonoActual = new ol.Feature({
    geometry: new ol.geom.Polygon([coordenadasPoligono]),
    tipo: 'poligono',
  });

  vectorSourceSuperficie.addFeature(poligonoActual);
  calcularAreaSuperficie();
}

// ========== CALCULAR ÁREA ==========
function calcularAreaSuperficie() {
  if (!poligonoActual) return;

  const geometria = poligonoActual.getGeometry();
  const areaMetros = ol.sphere.getArea(geometria, { projection: 'EPSG:3857' });

  const areaHectareas = areaMetros / 10000;

  const areaSuperficie = document.getElementById('area-superficie');
  if (areaSuperficie) {
    areaSuperficie.textContent = `${areaHectareas.toFixed(2)} ha`;
  }
}

// ========== ESTILOS ==========
function estiloFeatureSuperficie(feature) {
  const tipo = feature.get('tipo');

  if (tipo === 'punto') {
    return new ol.style.Style({
      image: new ol.style.Circle({
        radius: 6,
        fill: new ol.style.Fill({ color: '#ef4444' }),
        stroke: new ol.style.Stroke({ color: '#ffffff', width: 2 }),
      }),
      text: new ol.style.Text({
        text: String(feature.get('orden') + 1),
        font: 'bold 10px sans-serif',
        fill: new ol.style.Fill({ color: '#ffffff' }),
        offsetY: -12,
      }),
    });
  }

  if (tipo === 'poligono') {
    return new ol.style.Style({
      stroke: new ol.style.Stroke({ color: '#667eea', width: 3 }),
      fill: new ol.style.Fill({ color: 'rgba(102, 126, 234, 0.2)' }),
    });
  }
}

// ========== ACTUALIZAR INTERFAZ ==========
function actualizarInterfazMarcar() {
  const numPuntos = puntosMarcados.length;

  const puntosCount = document.getElementById('puntos-count');
  if (puntosCount) {
    puntosCount.textContent = `${numPuntos} / ${MAX_PUNTOS}`;
  }

  const btnDeshacer = document.getElementById('btn-deshacer');
  const btnLimpiar = document.getElementById('btn-limpiar');
  const btnCompletar = document.getElementById('btn-completar');

  if (btnDeshacer) btnDeshacer.disabled = numPuntos === 0;
  if (btnLimpiar) btnLimpiar.disabled = numPuntos === 0;
  if (btnCompletar) btnCompletar.disabled = numPuntos < MIN_PUNTOS;

  if (numPuntos === 0) {
    mostrarEstadoMarcar('👆 Haz clic en el mapa para marcar', 'info');
  } else if (numPuntos < MIN_PUNTOS) {
    mostrarEstadoMarcar(`📍 Marca al menos ${MIN_PUNTOS} puntos`, 'info');
  } else if (numPuntos < MAX_PUNTOS) {
    mostrarEstadoMarcar('✅ Puedes agregar más o guardar', 'success');
  } else {
    mostrarEstadoMarcar('⚠️ Límite alcanzado. Guarda ahora.', 'error');
  }
}

// ========== MOSTRAR ESTADO ==========
function mostrarEstadoMarcar(mensaje, tipo = 'info') {
  const panel = document.getElementById('panel-status-marcar');
  if (panel) {
    panel.textContent = mensaje;
    panel.className = `panel-status ${tipo}`;
  }
}

// ========== DESHACER ==========
function deshacerUltimoPunto() {
  if (puntosMarcados.length === 0) return;

  const ultimoPunto = puntosMarcados.pop();
  vectorSourceSuperficie.removeFeature(ultimoPunto.feature);

  if (puntosMarcados.length >= MIN_PUNTOS) {
    actualizarPoligonoSuperficie();
  } else if (poligonoActual) {
    vectorSourceSuperficie.removeFeature(poligonoActual);
    poligonoActual = null;
    const areaSuperficie = document.getElementById('area-superficie');
    if (areaSuperficie) areaSuperficie.textContent = '0 m²';
  }

  actualizarInterfazMarcar();
}

// ========== LIMPIAR ==========
function limpiarPuntos() {
  if (!confirm('¿Limpiar todos los puntos?')) return;

  vectorSourceSuperficie.clear();
  puntosMarcados = [];
  poligonoActual = null;

  const areaSuperficie = document.getElementById('area-superficie');
  if (areaSuperficie) areaSuperficie.textContent = '0 m²';

  actualizarInterfazMarcar();
}

// ========== GUARDAR ÁREA ==========
async function guardarArea() {
  if (puntosMarcados.length < MIN_PUNTOS) {
    alert('⚠️ Necesitas al menos 3 puntos');
    return;
  }

  const { correo, cultivoSeleccionado, cultivosData } = window.cultivosState;

  if (!cultivosData[cultivoSeleccionado]) {
    alert('⚠️ El cultivo seleccionado ya no existe');
    cerrarOverlayMarcar();
    return;
  }

  try {
    // ✅ Crear array de 20 puntos
    const puntosParaGuardar = Array.from({ length: MAX_PUNTOS }, (_, index) => {
      if (index < puntosMarcados.length) {
        return {
          latitud: puntosMarcados[index].lat,
          longitud: puntosMarcados[index].lon,
        };
      } else {
        return null;
      }
    });

    const areaMetros = poligonoActual
      ? ol.sphere.getArea(poligonoActual.getGeometry(), { projection: 'EPSG:3857' })
      : 0;
    
    const areaHectareas = (areaMetros / 10000).toFixed(2); // ✅ Convertir m^2 a hectáreas
    
    console.log('📤 Enviando al backend:', {
      cultivo: cultivoSeleccionado,
      area: areaHectareas,
      puntos: puntosParaGuardar,
    });

    const response = await fetch(
      `/usuarios/${encodeURIComponent(correo)}/cultivo/modificar_area_cultivo`,
      {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          cultivo: cultivoSeleccionado,
          area: areaHectareas,
          puntos: puntosParaGuardar,
        }),
      }
    );
    
    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    if (!response.ok) {
      throw new Error(data.error || data.detail || 'Error en el servidor');
    }

    console.log('✅', data.mensaje || 'Área guardada');

    cerrarOverlayMarcar();

    // ✅ Recargar cultivos completos
    await window.recargarCultivos?.();

    alert('✅ Área guardada correctamente');
    console.log('💾 Área guardada');

    renderizarMapaPrincipal();
    
  } catch (error) {
    console.error('❌ Error guardando área:', error);
    alert(`⚠️ ${error.message}`);
  }
}