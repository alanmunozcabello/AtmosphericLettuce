document.addEventListener('DOMContentLoaded', async () => {
  // 1. Obtener correo como en otros archivos
  const CORREO = new URLSearchParams(location.search).get('correo')
    || localStorage.getItem('correoUsuario');

  if (!CORREO) {
    console.warn("⚠️ Usuario no identificado");
    window.location.href = "index.html";
    return;
  }

  localStorage.setItem('correoUsuario', CORREO);

  let latUsuario, lonUsuario;

  try {
    // 2. ✅ Usar obtenerUsuario() como en el resto del proyecto
    const usuario = await obtenerUsuario(CORREO);
    
    if (!usuario) {
      console.warn("⚠️ No se pudo obtener datos del usuario");
      window.location.href = "index.html";
      return;
    }

    // 3. Extraer coordenadas
    latUsuario = usuario.ubicacion?.latitud || usuario.ubicacion?.lat || -33.446;
    lonUsuario = usuario.ubicacion?.longitud || usuario.ubicacion?.lon || -70.681;

  } catch (error) {
    console.error("❌ Error obteniendo usuario:", error);
    // Usar Santiago como fallback
    latUsuario = -33.446;
    lonUsuario = -70.681;
  }

// Crear mapa base centrado en Chile
const map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM(),
    }),
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([lonUsuario, latUsuario]), // Ubicacion
    zoom: 17,
  }),
});


// Fuente y capa vectorial donde se dibujan polígonos
const source = new ol.source.Vector({ wrapX: false });
const vector = new ol.layer.Vector({
  source: source
});
map.addLayer(vector);

// Interacción para dibujar polígonos
const draw = new ol.interaction.Draw({
  source: source,
  type: 'Polygon'
});
map.addInteraction(draw);

// Crear popup
const popup = document.createElement('div');
popup.className = 'ol-popup';
const overlay = new ol.Overlay({
  element: popup,
  positioning: 'bottom-center',
  stopEvent: false,
});
map.addOverlay(overlay);

// Evento al terminar de dibujar
draw.on('drawend', function (event) {
  const polygon = event.feature.getGeometry();
  const area = ol.sphere.getArea(polygon); // Área en m^2
  const hectareas = (area / 10000).toFixed(2);

  const coord = polygon.getInteriorPoint().getCoordinates();
  popup.innerHTML = `<b>Área:</b> ${hectareas} ha`;
  overlay.setPosition(coord);

  alert(`Área del cultivo: ${hectareas} hectáreas`);
});
});