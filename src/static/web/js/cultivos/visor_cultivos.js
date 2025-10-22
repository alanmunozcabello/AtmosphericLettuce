document.addEventListener('DOMContentLoaded', () => {
  // ========== ELEMENTOS DEL DOM ==========
  const loadingState = document.getElementById('loading-state');
  const emptyState = document.getElementById('empty-state');
  const errorState = document.getElementById('error-state');
  const cultivosList = document.getElementById('cultivos-list');
  const cultivosItems = document.getElementById('cultivos-items');
  const totalCultivos = document.getElementById('total-cultivos');
  const areaTotal = document.getElementById('area-total');
  const btnCentrar = document.getElementById('btn-centrar');
  const btnRetry = document.getElementById('btn-retry');
  const errorMessage = document.getElementById('error-message');

  // configuracion
  const COLORES_CULTIVOS = [
    '#ef4444', '#f59e0b', '#10b981', '#3b82f6', 
    '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'
  ];

  let map = null;
  let vectorSource = null;
  let cultivosCargados = [];
  let cultivoSeleccionado = null;
  let usuarioLatitud = -33.446;
  let usuarioLongitud = -70.681;

  // inicializar
  async function inicializarVisor() {
    console.log('🗺️ Inicializando visor de cultivos...');

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

    // 2. Crear mapa
    crearMapa();

    // 3. Cargar cultivos
    await cargarCultivos();
  }

  // crear mapa
  function crearMapa() {
    map = new ol.Map({
      target: 'map-visor',
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM(),
        }),
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([usuarioLongitud, usuarioLatitud]),
        zoom: 16,
      }),
      // DESHABILITAR INTERACCIONES (MAPA INMUTABLE)
    //   interactions: ol.interaction.defaults({
    //     doubleClickZoom: true,
    //     dragPan: true,
    //     mouseWheelZoom: true,
    //     // Deshabilitar edición
    //     draw: false,
    //     modify: false,
    //   }),
    });

    // Capa para los polígonos de cultivos
    vectorSource = new ol.source.Vector();
    const vectorLayer = new ol.layer.Vector({
      source: vectorSource,
    });
    map.addLayer(vectorLayer);

    // ✅ EVENTO DE HOVER PARA MOSTRAR INFO
    map.on('pointermove', manejarHover);

    // ✅ EVENTO DE CLICK PARA SELECCIONAR CULTIVO
    map.on('click', manejarClickCultivo);

    console.log('✅ Mapa creado (modo solo lectura)');
  }

  // cargar cultivos de momento desde el backend, despues usar la cache del usuario
  async function cargarCultivos() {
    mostrarEstado('loading');

    try {
      const correo = localStorage.getItem('correoUsuario');
      
      if (!correo) {
        throw new Error('Usuario no identificado');
      }

      console.log('📥 Cargando cultivos del usuario...');

      // TODO: Reemplazar con tu endpoint real
      const response = await fetch(`/usuarios/cultivos?correo=${encodeURIComponent(correo)}`);
      
      if (!response.ok) {
        throw new Error(`Error del servidor: ${response.status}`);
      }

      const data = await response.json();
      cultivosCargados = data.cultivos || [];

      console.log(`✅ ${cultivosCargados.length} cultivos cargados`);

      // Verificar si hay cultivos
      if (cultivosCargados.length === 0) {
        mostrarEstado('empty');
        return;
      }

      // Renderizar cultivos en el mapa y panel
      renderizarCultivos();
      mostrarEstado('success');

    } catch (error) {
      console.error('❌ Error cargando cultivos:', error);
      mostrarEstado('error', error.message);
    }
  }

  // renderizar cultivos en el mapa
  function renderizarCultivos() {
    // Limpiar mapa y lista
    vectorSource.clear();
    cultivosItems.innerHTML = '';

    let areaTotalMetros = 0;
    const bounds = [];

    cultivosCargados.forEach((cultivo, index) => {
      const color = COLORES_CULTIVOS[index % COLORES_CULTIVOS.length];

      // 1. Agregar polígono al mapa
      if (cultivo.puntos && cultivo.puntos.length >= 3) {
        const coordenadas = cultivo.puntos.map(p => 
          ol.proj.fromLonLat([p.longitud, p.latitud])
        );

        const poligono = new ol.Feature({
          geometry: new ol.geom.Polygon([coordenadas]),
          cultivoId: cultivo.id || index,
          cultivoNombre: cultivo.nombre || `Cultivo ${index + 1}`,
          cultivoArea: cultivo.area || 0,
          cultivoColor: color,
          cultivoTipo: cultivo.tipo || 'Sin especificar',
          cultivoFecha: cultivo.fecha || 'Sin fecha'
        });

        poligono.setStyle(crearEstiloPoligono(color, false));
        vectorSource.addFeature(poligono);

        // Agregar coordenadas a bounds para centrar
        coordenadas.forEach(coord => bounds.push(coord));

        // Sumar área
        areaTotalMetros += cultivo.area || 0;
      }

      // 2. Agregar item al panel
      const item = crearItemCultivo(cultivo, color, index);
      cultivosItems.appendChild(item);
    });

    // Actualizar resumen
    if (totalCultivos) totalCultivos.textContent = cultivosCargados.length;
    if (areaTotal) {
      if (areaTotalMetros < 10000) {
        areaTotal.textContent = `${Math.round(areaTotalMetros)} m²`;
      } else {
        areaTotal.textContent = `${(areaTotalMetros / 10000).toFixed(2)} ha`;
      }
    }

    // Centrar vista en todos los cultivos
    if (bounds.length > 0) {
      const extent = ol.extent.boundingExtent(bounds);
      map.getView().fit(extent, { padding: [50, 50, 50, 370], maxZoom: 18 });
    }

    console.log('✅ Cultivos renderizados en el mapa');
  }

  // crear el area del cultivo
  function crearItemCultivo(cultivo, color, index) {
    const div = document.createElement('div');
    div.className = 'cultivo-item';
    div.dataset.cultivoId = cultivo.id || index;

    const area = cultivo.area || 0;
    const areaFormateada = area < 10000 
      ? `${Math.round(area)} m²`
      : `${(area / 10000).toFixed(2)} ha`;

    div.innerHTML = `
      <div class="cultivo-color" style="background-color: ${color}"></div>
      <div class="cultivo-info">
        <div class="cultivo-nombre">${cultivo.nombre || `Cultivo ${index + 1}`}</div>
        <div class="cultivo-detalles">
          <span>📏 ${areaFormateada}</span>
          <span>🌾 ${cultivo.tipo || 'Sin tipo'}</span>
        </div>
      </div>
    `;

    // Click para resaltar cultivo
    div.addEventListener('click', () => {
      seleccionarCultivo(cultivo.id || index);
    });

    return div;
  }

  // estilo del poligono
  function crearEstiloPoligono(color, seleccionado) {
    return new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: color,
        width: seleccionado ? 4 : 2
      }),
      fill: new ol.style.Fill({
        color: color + (seleccionado ? '40' : '20') // Opacidad hex
      })
    });
  }

  // seleccionar cultivo
  function seleccionarCultivo(cultivoId) {
    cultivoSeleccionado = cultivoId;

    // Actualizar estilos en el mapa
    vectorSource.getFeatures().forEach(feature => {
      const id = feature.get('cultivoId');
      const color = feature.get('cultivoColor');
      const esSeleccionado = id === cultivoId;
      feature.setStyle(crearEstiloPoligono(color, esSeleccionado));
    });

    // Actualizar items del panel
    document.querySelectorAll('.cultivo-item').forEach(item => {
      const id = parseInt(item.dataset.cultivoId);
      if (id === cultivoId) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Centrar en el cultivo seleccionado
    const feature = vectorSource.getFeatures().find(f => f.get('cultivoId') === cultivoId);
    if (feature) {
      const extent = feature.getGeometry().getExtent();
      map.getView().fit(extent, { padding: [50, 50, 50, 370], maxZoom: 19 });
    }

    console.log('🎯 Cultivo seleccionado:', cultivoId);
  }

  // hover
  function manejarHover(evt) {
    const feature = map.forEachFeatureAtPixel(evt.pixel, f => f);
    
    if (feature && feature.get('cultivoNombre')) {
      map.getTargetElement().style.cursor = 'pointer';
    } else {
      map.getTargetElement().style.cursor = '';
    }
  }

  // doble click
  function manejarClickCultivo(evt) {
    const feature = map.forEachFeatureAtPixel(evt.pixel, f => f);
    
    if (feature && feature.get('cultivoId') !== undefined) {
      seleccionarCultivo(feature.get('cultivoId'));
    }
  }

  // ========== CENTRAR VISTA ==========
  function centrarVista() {
    map.getView().animate({
        center: ol.proj.fromLonLat([usuarioLongitud, usuarioLatitud]),
        zoom: 16,
        duration: 500 // Animación suave de medio segundo
    })
    //ver caso de que el usuario tenga cultivos en muchas partes y no solo en su ubicacion

    console.log('🎯 Vista centrada en todos los cultivos');
  }

  // mostrar estados
  function mostrarEstado(estado, mensaje = '') {
    loadingState.style.display = 'none';
    emptyState.style.display = 'none';
    errorState.style.display = 'none';
    cultivosList.style.display = 'none';

    switch (estado) {
      case 'loading':
        loadingState.style.display = 'flex';
        break;
      case 'empty':
        emptyState.style.display = 'flex';
        break;
      case 'error':
        errorState.style.display = 'flex';
        if (errorMessage) errorMessage.textContent = mensaje || 'Error al cargar cultivos';
        break;
      case 'success':
        cultivosList.style.display = 'block';
        break;
    }
  }

  // event listeners
  if (btnCentrar) {
    btnCentrar.addEventListener('click', centrarVista);
  }

//   if (btnRetry) {
//     btnRetry.addEventListener('click', () => {
//       cargarCultivos();
//     });
//   }

  // ========== INICIAR ==========
  inicializarVisor();
});