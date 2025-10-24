// ========== RENDERIZAR LISTA ==========
function renderizarLista() {
  const listaCultivos = document.getElementById('lista-cultivos');
  if (!listaCultivos) return;

  listaCultivos.innerHTML = '';

  const { cultivosData } = window.cultivosState;
  const entries = Object.entries(cultivosData);

  if (entries.length === 0) {
    listaCultivos.innerHTML = '<li class="cultivo-item-loading">No tienes cultivos 🌱</li>';
    return;
  }

  entries.forEach(([nombre, data]) => {
    const hectareas = typeof data === 'number' ? data : data.hectareas || 0;
    
    const li = document.createElement('li');
    li.className = 'item-cultivo';
    li.dataset.nombre = nombre;
    
    li.innerHTML = `
      <span class="tick">✔</span>
      <span><strong>${nombre}</strong> — ${hectareas} ha</span>
      <div class="botones-grupo">
        <button class="btn-config" data-nombre="${nombre}" aria-label="Configurar">⚙️</button>
        <button class="btn-eliminar" data-nombre="${nombre}" aria-label="Eliminar">✕</button>
      </div>
    `;

    li.addEventListener('click', (e) => {
      // Si es botón de configuración, redirigir a formulario
      if (e.target.classList.contains('btn-config')) {
        const { correo } = window.cultivosState;
        window.location.href = `formulario_plantas.html?cultivo=${encodeURIComponent(nombre)}&correo=${encodeURIComponent(correo)}`;
        return;
      }
      
      // Si no es botón de eliminar ni config, , seleccionar en mapa
      if (!e.target.classList.contains('btn-eliminar') && !e.target.classList.contains('btn-config')) {
        if (typeof seleccionarCultivoMapa === 'function') {
          seleccionarCultivoMapa(nombre);
        }
      }
    });

    listaCultivos.appendChild(li);
  });
}

// ========== ACTUALIZAR RESUMEN ==========
function actualizarResumen() {
  const { cultivosData } = window.cultivosState;
  const totalCultivosEl = document.getElementById('total-cultivos');
  const areaTotalEl = document.getElementById('area-total');

  const total = Object.keys(cultivosData).length;
  let areaTotal = 0;

  Object.values(cultivosData).forEach((data) => {
    const hectareas = typeof data === 'number' ? data : data.hectareas || 0;
    areaTotal += hectareas;
  });

  if (totalCultivosEl) totalCultivosEl.textContent = total;
  if (areaTotalEl) areaTotalEl.textContent = `${areaTotal.toFixed(2)} ha`;
}