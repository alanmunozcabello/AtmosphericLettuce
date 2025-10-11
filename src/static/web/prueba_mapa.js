// Crear capa base con OpenStreetMap
const map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    })
  ],
  view: new ol.View({
    center: ol.proj.fromLonLat([-70.65, -33.45]), // Santiago, Chile
    zoom: 10
  })
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
