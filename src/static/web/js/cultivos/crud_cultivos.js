// ========== INICIALIZAR EVENTOS CRUD ==========
function inicializarEventosCRUD() {
  const form = document.getElementById('form-cultivo');
  const listaCultivos = document.getElementById('lista-cultivos');

  if (form) {
    form.addEventListener('submit', agregarCultivo);
  }

  if (listaCultivos) {
    listaCultivos.addEventListener('click', eliminarCultivo);
  }

  console.log('✅ Eventos CRUD inicializados');
}

// ========== AGREGAR/MODIFICAR CULTIVO ==========
async function agregarCultivo(e) {
  e.preventDefault();

  const { correo, cultivosData } = window.cultivosState;
  const inputCultivo = document.getElementById('input-cultivo');
  const inputHectareas = document.getElementById('input-hectareas');

  const nombre = inputCultivo.value.trim();
  const hectareas = parseFloat(inputHectareas.value);

  if (!nombre || hectareas <= 0) {
    alert('⚠️ Completa los campos correctamente');
    return;
  }

  try {
    // ✅ Verificar si ya existe
    const cultivoExiste = cultivosData.hasOwnProperty(nombre);
    
    const accionTexto = cultivoExiste ? 'Modificando' : 'Agregando';
    console.log(`${accionTexto} cultivo:`, nombre);
    
    const response = await fetch(
      `/usuarios/${encodeURIComponent(correo)}/agregar_cultivo`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nombre_cultivo: nombre,
          hectareas: hectareas,
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

    console.log('✅', data.mensaje || 'Cultivo guardado');

    // ✅ Recargar cultivos completos
    await window.recargarCultivos?.();

    // Limpiar formulario
    inputCultivo.value = '';
    inputHectareas.value = '';
    inputCultivo.focus();

    const accion = cultivoExiste ? 'modificado' : 'agregado';
    alert(`✅ Cultivo ${accion} correctamente`);
    
  } catch (error) {
    console.error('❌ Error guardando cultivo:', error);
    alert(`⚠️ ${error.message}`);
  }
}

// ========== ELIMINAR CULTIVO ==========
async function eliminarCultivo(e) {
  const btn = e.target.closest('.btn-eliminar');
  if (!btn) return;

  const { correo } = window.cultivosState;
  const nombre = btn.dataset.nombre;

  if (!confirm(`¿Eliminar "${nombre}"?`)) return;

  try {
    const response = await fetch(
      `/usuarios/${encodeURIComponent(correo)}/${encodeURIComponent(nombre)}/eliminar`,
      { method: 'DELETE' }
    );

    const data = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    if (!response.ok) {
      throw new Error(data.error || data.detail || 'Error en el servidor');
    }

    console.log('✅', data.mensaje || 'Cultivo eliminado');

    // ✅ Recargar cultivos completos
    await window.recargarCultivos?.();

    alert('✅ Cultivo eliminado correctamente');
    
  } catch (error) {
    console.error('❌ Error eliminando cultivo:', error);
    alert(`⚠️ ${error.message}`);
  }
}