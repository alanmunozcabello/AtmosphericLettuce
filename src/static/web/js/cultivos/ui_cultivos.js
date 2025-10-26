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

  entries.forEach(([nombre, cultivo]) => {
    const hectareas = cultivo.hectareas || 0;
    const puntos = cultivo.puntos || [];
    const tienePuntos = puntos.length > 0 && puntos.some(p => p !== null);
    
    const li = document.createElement('li');
    li.className = 'item-cultivo';
    li.dataset.nombre = nombre;
    li.dataset.cultivoId = cultivo.id; // ✅ Guardar ID del cultivo
    
    li.innerHTML = `
      <span class="tick">✔</span>
      <span>
        <strong>${nombre}</strong> — ${hectareas.toFixed(2)} ha
        ${tienePuntos ? ' 📍' : ''}
      </span>
      <div class="botones-grupo">
        <button class="btn-config" data-nombre="${nombre}" aria-label="Configurar">⚙️</button>
        <button class="btn-eliminar" data-nombre="${nombre}" aria-label="Eliminar">✕</button>
      </div>
    `;

    // ❌ REMOVER ESTO (ahora se maneja con event delegation)
    // li.addEventListener('click', (e) => { ... });

    listaCultivos.appendChild(li);
  });

  console.log(`✅ === FIN renderizarLista === ${entries.length} cultivos en DOM`);
}

// ========== ACTUALIZAR RESUMEN ==========
function actualizarResumen() {
  const { cultivosData } = window.cultivosState;
  const totalCultivosEl = document.getElementById('total-cultivos');
  const areaTotalEl = document.getElementById('area-total');

  const total = Object.keys(cultivosData).length;
  let areaTotal = 0;

  Object.values(cultivosData).forEach((cultivo) => {
    // ✅ Acceder a hectareas desde cultivo.hectareas
    areaTotal += cultivo.hectareas || 0;
  });

  if (totalCultivosEl) totalCultivosEl.textContent = total;
  if (areaTotalEl) areaTotalEl.textContent = `${areaTotal.toFixed(2)} ha`;

  console.log('✅ Resumen actualizado:', total, 'cultivos,', areaTotal.toFixed(2), 'ha');
}