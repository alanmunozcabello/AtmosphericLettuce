// Crear mapa base centrado en Chile
const map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM(),
    }),
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([-71.543, -35.426]), // Chile central
    zoom: 6,
  }),
});

// Capa para marcadores
const vectorSource = new ol.source.Vector();
const vectorLayer = new ol.layer.Vector({ source: vectorSource });
map.addLayer(vectorLayer);

// Crear popup
const popup = document.createElement('div');
popup.className = 'ol-popup';
const overlay = new ol.Overlay({ element: popup, positioning: 'bottom-center', stopEvent: false });
map.addOverlay(overlay);

// Evento de clic
map.on('click', async function (evt) {
  const [lon, lat] = ol.proj.toLonLat(evt.coordinate);

  // Eliminar marcador anterior
  vectorSource.clear();

  // Crear nuevo marcador
  const marker = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat])),
  });
  vectorSource.addFeature(marker);

  // Petición a Nominatim
  const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10&addressdetails=1`;
  const res = await fetch(url);
  const data = await res.json();

  let ciudad = "Desconocida", region = "Desconocida", pais = "Desconocido";
  if (data.address) {
    ubi = lat + " , " + lon;
    ciudad = data.address.city || data.address.town || data.address.village || "Desconocida";
    region = data.address.state || "Desconocida";
    pais = data.address.country || "Desconocido";
  }

  // Mostrar popup
  popup.innerHTML = `
    <strong>📍 Ubicación:</strong> ${ubi}<br>
    <strong>📍 Ciudad:</strong> ${ciudad}<br>
    <strong>🗺️ Región:</strong> ${region}<br>
    <strong>🌎 País:</strong> ${pais}
  `;
  overlay.setPosition(evt.coordinate);
});
