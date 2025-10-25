document.addEventListener('DOMContentLoaded', () => {
      const inputUbicacion = document.getElementById('input-ubicacion');
      const mapaOverlay = document.getElementById('mapa-overlay');
      const btnCerrar = document.getElementById('cerrar-mapa');
      const btnConfirmar = document.getElementById('confirmar-ubicacion');
      const btnCancelar = document.getElementById('cancelar-ubicacion');

      let map = null;
      let vectorSource = null;
      let latUsuario, lonUsuario;
      let correo;
      let ciudad = "Desconocida", region = "Desconocida", pais = "Desconocido", latMod, lonMod;

      // Mostrar mapa al hacer clic en el input
      inputUbicacion.addEventListener('click', async () => {
        if(map){
            return;
        }
        mapaOverlay.style.display = 'flex';
        // console.log('🗺️ Mapa abierto');
        // 1. Obtener correo como en otros archivos
          const CORREO = new URLSearchParams(location.search).get('correo')
            || localStorage.getItem('correoUsuario');
            
          if (!CORREO) {
            console.warn("⚠️ Usuario no identificado");
            window.location.href = "index.html";
            return;
          }
      
          localStorage.setItem('correoUsuario', CORREO);
          correo = CORREO;

          try {
            // 2. ✅ Usar obtenerUsuario() como en el resto del proyecto
            const usuario = await obtenerUsuario(CORREO);
            
            if (!usuario) {
              console.warn("⚠️ No se pudo obtener datos del usuario");
              window.location.href = "index.html";
              return;
            }
        
            // 3. Extraer coordenadas
            latUsuario = usuario.ubicacion?.latitud ?? usuario.ubicacion?.lat ?? -33.446;
            lonUsuario = usuario.ubicacion?.longitud ?? usuario.ubicacion?.lon ?? -70.681;
        
          } catch (error) {
            console.error("❌ Error obteniendo usuario:", error);
            // Usar Santiago como fallback
            latUsuario = -33.446;
            lonUsuario = -70.681;
          }
        // Crear mapa base centrado en Chile
        map = new ol.Map({
          target: 'map',
          layers: [
            new ol.layer.Tile({
              source: new ol.source.OSM(),
            }),
          ],
          view: new ol.View({
            center: ol.proj.fromLonLat([lonUsuario, latUsuario]), // Ubicacion
            zoom: 16,
          }),
        });
        console.log(latUsuario, lonUsuario);
        // Capa para marcadores
        vectorSource = new ol.source.Vector();
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
          //pointer más bonito y visible apra el usuario
          marker.setStyle(new ol.style.Style({
              image: new ol.style.Icon({
                src: 'data:image/svg+xml;utf8,' + encodeURIComponent(`
                  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">
                    <text x="16" y="24" text-anchor="middle" font-size="20" font-family="Arial">📍</text>
                  </svg>
                `),
                scale: 1,
                anchor: [0.5, 1], // Punto de anclaje (centro-abajo)
              })
            }));

          vectorSource.addFeature(marker);
      
          // ✅ ACTUALIZAR PANEL LATERAL EN LUGAR DE POPUP
          // Referencias a elementos del panel
          const panelCiudad = document.getElementById('panel-ciudad');
          const panelRegion = document.getElementById('panel-region');
          const panelPais = document.getElementById('panel-pais');
          const panelLat = document.getElementById('panel-lat');
          const panelLon = document.getElementById('panel-lon');
          const panelStatus = document.getElementById('panel-status');
      
          // Mostrar coordenadas inmediatamente
          if (panelLat) panelLat.textContent = lat.toFixed(6);
          if (panelLon) panelLon.textContent = lon.toFixed(6);

          // Mostrar valores temporales mientras se carga
          if (panelCiudad) panelCiudad.textContent = 'Cargando...';
          if (panelRegion) panelRegion.textContent = 'Cargando...';
          if (panelPais) panelPais.textContent = 'Cargando...';
      
          // ✅ MOSTRAR EN CONSOLA COMO ANTES
          console.log('📍 Latitud:', lat);
          console.log('📍 Longitud:', lon);
          latMod = lat;
          lonMod = lon;
      
          try {
            // Petición a Nominatim
            const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10&addressdetails=1`;
            const res = await fetch(url);
            const data = await res.json();
        
            if (data.address) {
              ciudad = data.address.city || data.address.town || data.address.village || "Desconocida";
              region = data.address.state || "Desconocida";
              pais = data.address.country || "Desconocido";
            }
        
            // ✅ ACTUALIZAR PANEL CON LA INFORMACIÓN
            if (panelCiudad) panelCiudad.textContent = ciudad;
            if (panelRegion) panelRegion.textContent = region;
            if (panelPais) panelPais.textContent = pais;
        
            // ✅ MOSTRAR EN CONSOLA
            console.log('🏙️ Ciudad:', ciudad);
            console.log('🗺️ Región:', region);
            console.log('🌎 País:', pais);
        
          } catch (error) {
            console.error('❌ Error obteniendo información:', error);

            // Estado de error
            if (panelCiudad) panelCiudad.textContent = 'Error';
            if (panelRegion) panelRegion.textContent = 'Error';
            if (panelPais) panelPais.textContent = 'Error';
          }
        });
      });

    function matarMapa(){
        console.log('🗑️ Destruyendo mapa...');
      
        // 1. Remover todos los overlays y layers
        map.getOverlays().clear();
        map.getLayers().clear();
        
        // 2. Limpiar el target (contenedor)
        map.setTarget(null);
        
        // 3. Destruir la instancia
        map.dispose();
        map = null;
        vectorSource = null;
        
        // 4. Limpiar el contenedor HTML. sin el if da error
        const mapContainer = document.getElementById('map');
        if (mapContainer) {
        mapContainer.innerHTML = '';
        }

        console.log('✅ Mapa destruido completamente');
      }

      // Cerrar mapa con el botón X
      btnCerrar.addEventListener('click', () => {
        mapaOverlay.style.display = 'none';
        matarMapa();
        console.log('🗺️ Mapa cerrado (X)');
      });

      // Cerrar mapa con confirmar
      btnConfirmar.addEventListener('click', async () => {
        // Validar que se haya seleccionado una ubicación
        if (!latMod || !lonMod) {
          alert('⚠️ Selecciona una ubicación en el mapa primero');
          return;
        }
      
        try {
          console.log('📤 Enviando ubicación al backend...');
        
          // 1. Actualizar coordenadas
          const respuesta1 = await fetch(
            `/usuarios/${encodeURIComponent(correo)}/ubicacion/${latMod}/${lonMod}/modificar`, 
            {
              method: "PATCH",
              headers: { "Content-Type": "application/json" },
            }
          );
        
          if (!respuesta1.ok) {
            const error1 = await respuesta1.json();
            throw new Error(error1.error || 'Error actualizando coordenadas');
          }
        
          console.log('✅ Coordenadas actualizadas');
        
          // 2. Actualizar región/ciudad
          const respuesta2 = await fetch(
            `/usuarios/${encodeURIComponent(correo)}/ubicacion/region/${encodeURIComponent(region)}/${encodeURIComponent(ciudad)}/modificar`, 
            {
              method: "PATCH",
              headers: { "Content-Type": "application/json" },
            }
          );
        
          if (!respuesta2.ok) {
            const error2 = await respuesta2.json();
            throw new Error(error2.error || 'Error actualizando región/ciudad');
          }
        
          console.log('✅ Región/ciudad actualizadas');
        
          // ✅ 3. ACTUALIZAR CACHÉ DEL USUARIO
          const usuarioActualizado = await obtenerUsuario(correo);
          
          if (usuarioActualizado) {
            // Actualizar localStorage
            localStorage.setItem('usuario', JSON.stringify(usuarioActualizado));
            
            // Actualizar window.homeState si existe (para home.html)
            if (window.homeState) {
              window.homeState.usuario = usuarioActualizado;
              window.homeState.latitud = usuarioActualizado.ubicacion?.latitud || latMod;
              window.homeState.longitud = usuarioActualizado.ubicacion?.longitud || lonMod;
              console.log('✅ homeState actualizado');
            }
          
            // Actualizar window.cultivosState si existe (para gestor_cultivos.html)
            if (window.cultivosState) {
              window.cultivosState.usuarioData = usuarioActualizado;
              window.cultivosState.usuarioLatitud = usuarioActualizado.ubicacion?.latitud || latMod;
              window.cultivosState.usuarioLongitud = usuarioActualizado.ubicacion?.longitud || lonMod;
              console.log('✅ cultivosState actualizado');
            }
          
            console.log('✅ Caché del usuario actualizada');
          }
        
          // 4. Actualizar input visual
          inputUbicacion.value = `${ciudad}, ${region}`;
        
          // 5. Cerrar overlay
          mapaOverlay.style.display = 'none';
          matarMapa();
        
          alert('✅ Ubicación actualizada correctamente');
          console.log('✅ Ubicación confirmada y guardada');
        
        } catch (error) {
          console.error('❌ Error actualizando ubicación:', error);
          alert(`⚠️ Error: ${error.message}`);
        }
      });

      // Cerrar mapa con cancelar
      btnCancelar.addEventListener('click', () => {
        mapaOverlay.style.display = 'none';
        matarMapa()
        console.log('❌ Selección cancelada');
      });

      // Cerrar al hacer clic fuera del contenedor
      mapaOverlay.addEventListener('click', (e) => {
        if (e.target === mapaOverlay) {
          mapaOverlay.style.display = 'none';
          matarMapa();
          console.log('🗺️ Mapa cerrado (click fuera)');
        }
      });
    });