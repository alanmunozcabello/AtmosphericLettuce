// ========== INICIALIZAR EVENTOS CRUD ==========
function inicializarEventosCRUD() {
  const form = document.getElementById('form-cultivo');
  const listaCultivos = document.getElementById('lista-cultivos');

  // Agregar/Modificar
  if (form) {
    form.addEventListener('submit', agregarModificarCultivo);
  }

  // Eliminar
  if (listaCultivos) {
    listaCultivos.addEventListener('click', eliminarCultivo);
  }

  console.log('✅ Eventos CRUD inicializados');
}

// ========== AGREGAR/MODIFICAR CULTIVO ==========
async function agregarModificarCultivo(e) {
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
    // Verificar si el cultivo ya existe
    const cultivoExiste = cultivosData.hasOwnProperty(nombre);
    
    const accionTexto = cultivoExiste ? 'Modificando' : 'Agregando';
    console.log(`${accionTexto} cultivo:`, nombre);
    
    // ✅ AGREGAR/MODIFICAR: PATCH /usuarios/{correo}/agregar_modificar
    const response = await fetch(
      `/usuarios/${encodeURIComponent(correo)}/agregar_modificar`,
      {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nombre_cultivo: nombre,
          hectareas: hectareas,
          fecha_siembra: null,
          notas: null,
          etapa_planta: null,
          tipo_riego: null,
          ultimo_riego: null,
          frecuencia_riego: null,
          humedad_suelo: null,
          textura_suelo: null,
          variedad_planta: null,
          estado_planta: null,
          estres_hidrico: null,
          profundidad_radical: null,
          densidad_plantacion: null,
          tipo_sensor: null,
          eficiencia_riego: null,
          caudal: null,
          ph_agua: null,
          acolchado: null
        }),
      }
    );

    const data = await response.json();

    if(data.error){
        throw new Error(data.error);
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Error en el servidor');
    }

    // Actualizar cache local
    const usuarioActual = JSON.parse(localStorage.getItem('usuario') || '{}');
    actualizarCacheUsuario({
      cultivos: {
        ...usuarioActual.cultivos,
        [nombre]: hectareas,
      },
    });

    // Recargar vista
    if (typeof window.recargarCultivos === 'function') {
      await window.recargarCultivos();
    }

    // Limpiar formulario
    inputCultivo.value = '';
    inputHectareas.value = '';
    inputCultivo.focus();

    const accion = cultivoExiste ? 'modificado' : 'agregado';
    console.log(`✅ Cultivo ${accion}:`, nombre);
    
  } catch (error) {
    console.error('❌ Error guardando cultivo:', error);
    alert(`⚠️ Error: ${error.message}`);
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
    // ✅ ELIMINAR: DELETE /usuarios/{correo}/{cultivo}/eliminar
    const response = await fetch(
      `/usuarios/${encodeURIComponent(correo)}/${encodeURIComponent(nombre)}/eliminar`,
      { method: 'DELETE' }
    );

    const data = await response.json();

    if(data.error){
        throw new Error(data.error);
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Error en el servidor');
    }

    // Actualizar cache local
    const usuarioActual = JSON.parse(localStorage.getItem('usuario') || '{}');
    const cultivosActualizados = { ...usuarioActual.cultivos };
    delete cultivosActualizados[nombre];

    actualizarCacheUsuario({ cultivos: cultivosActualizados });

    // Recargar vista
    if (typeof window.recargarCultivos === 'function') {
      await window.recargarCultivos();
    }

    console.log('🗑️ Cultivo eliminado:', nombre);
    
  } catch (error) {
    console.error('❌ Error eliminando cultivo:', error);
    alert(`⚠️ Error: ${error.message}`);
  }
}