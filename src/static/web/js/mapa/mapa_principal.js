// ========== VARIABLES DEL MAPA PRINCIPAL ==========
let mapPrincipal = null;
let vectorSourcePrincipal = null;

// ========== INICIALIZAR MAPA PRINCIPAL ==========
function inicializarMapaPrincipal() {
  const { usuarioLatitud, usuarioLongitud } = window.cultivosState;

  mapPrincipal = new ol.Map({
    target: 'map-gestor',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM(),
      }),
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([usuarioLongitud, usuarioLatitud]),
      zoom: 16,
    }),
  });

  // Capa para polígonos
  vectorSourcePrincipal = new ol.source.Vector();
  const vectorLayer = new ol.layer.Vector({
    source: vectorSourcePrincipal,
  });
  mapPrincipal.addLayer(vectorLayer);

  // Eventos
  mapPrincipal.on('pointermove', manejarHoverMapa);
  mapPrincipal.on('click', manejarClickMapa);

  // Botón centrar vista
  const btnCentrar = document.getElementById('btn-centrar-vista');
  if (btnCentrar) {
    btnCentrar.addEventListener('click', centrarVistaMapa);
  }

  console.log('✅ Mapa principal creado');
}

// ========== RENDERIZAR CULTIVOS EN MAPA ==========
function renderizarMapaPrincipal() {
  if (!vectorSourcePrincipal) return;

  vectorSourcePrincipal.clear();

  const { cultivosData, colores } = window.cultivosState;
  const entries = Object.entries(cultivosData);
  
  if (entries.length === 0) return;

  const bounds = [];

  entries.forEach(([nombre, data], index) => {
    const color = colores[index % colores.length];
    const puntos = Array.isArray(data.puntos) ? data.puntos : [];

    if (puntos.length >= 3) {
      const coordenadas = puntos.map(p =>
        ol.proj.fromLonLat([p.longitud || p.lon, p.latitud || p.lat])
      );

      const poligono = new ol.Feature({
        geometry: new ol.geom.Polygon([coordenadas]),
        cultivoNombre: nombre,
        cultivoHectareas: typeof data === 'number' ? data : data.hectareas || 0,
        cultivoColor: color,
      });

      poligono.setStyle(crearEstiloPoligono(color, false));
      vectorSourcePrincipal.addFeature(poligono);

      coordenadas.forEach(coord => bounds.push(coord));
    }
  });

  // Centrar en todos los cultivos
  if (bounds.length > 0) {
    const extent = ol.extent.boundingExtent(bounds);
    mapPrincipal.getView().fit(extent, { padding: [50, 50, 50, 400], maxZoom: 18 });
  }
}

// ========== ESTILO POLÍGONO ==========
function crearEstiloPoligono(color, seleccionado) {
  return new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: color,
      width: seleccionado ? 4 : 2,
    }),
    fill: new ol.style.Fill({
      color: color + (seleccionado ? '40' : '20'),
    }),
  });
}

// ========== SELECCIONAR CULTIVO ==========
function seleccionarCultivoMapa(nombre) {
  window.cultivosState.cultivoSeleccionado = nombre;

  // Actualizar estilos
  if (vectorSourcePrincipal) {
    vectorSourcePrincipal.getFeatures().forEach((feature) => {
      const esteNombre = feature.get('cultivoNombre');
      const color = feature.get('cultivoColor');
      feature.setStyle(crearEstiloPoligono(color, esteNombre === nombre));
    });
  }

  // Actualizar lista
  document.querySelectorAll('.item-cultivo').forEach((item) => {
    if (item.dataset.nombre === nombre) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });

  // Centrar en el cultivo
  const feature = vectorSourcePrincipal.getFeatures().find(f => f.get('cultivoNombre') === nombre);
  if (feature) {
    const extent = feature.getGeometry().getExtent();
    mapPrincipal.getView().fit(extent, { padding: [50, 50, 50, 400], maxZoom: 19 });
  }

  console.log('🎯 Cultivo seleccionado:', nombre);
}

// ========== HOVER ==========
function manejarHoverMapa(evt) {
  const feature = mapPrincipal.forEachFeatureAtPixel(evt.pixel, (f) => f);

  if (feature && feature.get('cultivoNombre')) {
    mapPrincipal.getTargetElement().style.cursor = 'pointer';
  } else {
    mapPrincipal.getTargetElement().style.cursor = '';
  }
}

// ========== CLICK (POPUP) ==========
function manejarClickMapa(evt) {
  // Eliminar popups previos
  document.querySelectorAll('.ol-popup-cultivo').forEach(p => p.remove());

  const feature = mapPrincipal.forEachFeatureAtPixel(evt.pixel, (f) => f);

  if (feature && feature.get('cultivoNombre')) {
    const nombre = feature.get('cultivoNombre');
    const hectareas = feature.get('cultivoHectareas');

    // Crear popup
    const popup = document.createElement('div');
    popup.className = 'ol-popup-cultivo';
    popup.innerHTML = `
      <button class="btn-cerrar-popup">✕</button>
      <div class="popup-nombre">${nombre}</div>
      <div class="popup-hectareas">📏 ${hectareas} ha</div>
    `;

    const overlay = new ol.Overlay({
      element: popup,
      positioning: 'bottom-center',
      offset: [0, -10],
      stopEvent: false,
    });

    mapPrincipal.addOverlay(overlay);
    overlay.setPosition(evt.coordinate);

    popup.querySelector('.btn-cerrar-popup').addEventListener('click', () => {
      mapPrincipal.removeOverlay(overlay);
    });

    seleccionarCultivoMapa(nombre);
  }
}

// ========== CENTRAR VISTA ==========
function centrarVistaMapa() {
  const { usuarioLatitud, usuarioLongitud } = window.cultivosState;
  
  mapPrincipal.getView().animate({
    center: ol.proj.fromLonLat([usuarioLongitud, usuarioLatitud]),
    zoom: 16,
    duration: 500,
  });
}

// Exponer funciones globales
window.seleccionarCultivoMapa = seleccionarCultivoMapa;