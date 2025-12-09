document.addEventListener('DOMContentLoaded', () => {
    // Referencias a elementos
    const btnNotificaciones = document.getElementById('btn-notificaciones'); // El botón de la campana

    // Identificador único para evitar duplicados
    const MODAL_ID = 'modal-notificaciones';

    // Crear el HTML del modal dinámicamente si no existe
    if (!document.getElementById(MODAL_ID)) {
        // Nota: Agregamos style="display: none;" para asegurar que no aparezca al inicio
        const modalHTML = `
            <div id="${MODAL_ID}" class="modal-notificaciones-overlay" style="display: none;">
                <div class="modal-notificaciones-content">
                    <button type="button" id="btn-cerrar-noti" class="btn-cerrar-modal">&times;</button>
                    <h2>🔔 Notificaciones</h2>
                    <p>¿Deseas recibir notificaciones de tus cultivos?</p>
                    <span id="estado-noti-texto" class="estado-notificaciones">Cargando estado...</span>
                    
                    <div class="botones-notificaciones">
                        <button type="button" id="btn-noti-no" class="btn-noti btn-desactivar" title="Desactivar Notificaciones">
                            ✕
                        </button>
                        <button type="button" id="btn-noti-si" class="btn-noti btn-activar" title="Activar Notificaciones">
                            ✓
                        </button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    const modal = document.getElementById(MODAL_ID);
    const btnCerrar = document.getElementById('btn-cerrar-noti');
    const btnNo = document.getElementById('btn-noti-no');
    const btnSi = document.getElementById('btn-noti-si');
    const estadoTexto = document.getElementById('estado-noti-texto');

    // Estado interno para evitar llamadas innecesarias
    let isFetching = false;

    // Funciones
    async function obtenerEstadoNotificaciones() {
        const token = localStorage.getItem('token');
        const correo = localStorage.getItem('correoUsuario');

        if (!token || !correo) {
            estadoTexto.textContent = "Sesión no válida";
            return;
        }

        if (isFetching) return;
        isFetching = true;
        estadoTexto.textContent = "Cargando estado..."; // Feedback visual

        try {
            // Nueva ruta POST: /notificaciones/verificar_estado_notificaciones
            const url = `/notificaciones/verificar_estado_notificaciones?correo=${encodeURIComponent(correo)}`;

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                // Se asume que retorna un JSON con el estado, ej: { "estado": true/false } o boolean directo
                // El endpoint dice 'return verificar_estado_notificaciones(correo)' que devuelve un bool o valor.
                const resultado = await response.json();

                // Si el resultado es un objeto, intentar acceder a una propiedad lógica, si no, usar el resultado directo
                let estado = resultado;
                if (typeof resultado === 'object' && resultado !== null && 'notificaciones' in resultado) {
                    estado = resultado.notificaciones;
                }
                actualizarUIEstado(estado);
            } else {
                console.error('Error del servidor:', response.status);
                estadoTexto.textContent = "Error al obtener estado";
            }
        } catch (error) {
            console.error('Error al obtener notificaciones:', error);
            estadoTexto.textContent = "Error de conexión";
        } finally {
            isFetching = false;
        }
    }

    async function cambiarNotificaciones(activar) {
        const token = localStorage.getItem('token');
        const correo = localStorage.getItem('correoUsuario');

        if (!token || !correo) {
            alert("No hay sesión activa");
            return;
        }

        try {
            // ruta_modificar_notificaciones_usuario: /usuarios/{correo}/modificar_notificaciones/{notificaciones}
            const url = `/usuarios/${encodeURIComponent(correo)}/modificar_notificaciones/${activar}`;

            const response = await fetch(url, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                actualizarUIEstado(activar);
                // Opcional: Cerrar modal automáticamente después de éxito
                // setTimeout(cerrarModal, 500);
            } else {
                console.error('Error al modificar notificaciones');
                alert("No se pudo actualizar la preferencia (Error servidor).");
            }
        } catch (error) {
            console.error('Error de red:', error);
            alert("Error de conexión.");
        }
    }

    function actualizarUIEstado(activo) {
        // Convertir a booleano explícito por si viene string "true"/"false" o 1/0
        const esActivo = activo === true || activo === 'true' || activo === 1;

        if (esActivo) {
            estadoTexto.textContent = "Estado actual: Recibiendo notificaciones ✅";
            estadoTexto.classList.remove('estado-inactivo');
            estadoTexto.classList.add('estado-activo');
            btnSi.style.opacity = '1';
            btnNo.style.opacity = '0.5';
        } else {
            estadoTexto.textContent = "Estado actual: No recibiendo notificaciones 🔕";
            estadoTexto.classList.remove('estado-activo');
            estadoTexto.classList.add('estado-inactivo');
            btnSi.style.opacity = '0.5';
            btnNo.style.opacity = '1';
        }
    }

    function abrirModal() {
        modal.style.display = 'flex'; // Mostrar el contenedor
        // Pequeño delay para permitir transición de opacidad si se desea (opcional)
        setTimeout(() => {
            modal.classList.add('activo');
        }, 10);

        obtenerEstadoNotificaciones();
    }

    function cerrarModal() {
        modal.classList.remove('activo');
        // Esperar a que termine la transición CSS (0.3s) antes de ocultar
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
    }

    // Event Listeners
    // Usar 'click' tanto en el icono como en el ID
    if (btnNotificaciones) {
        btnNotificaciones.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation(); // Evitar propagación
            abrirModal();
        };
    }

    if (btnCerrar) {
        btnCerrar.onclick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            cerrarModal();
        };
    }

    // Cerrar si se hace click fuera del contenido (en el overlay)
    modal.onclick = (e) => {
        if (e.target === modal) {
            cerrarModal();
        }
    };

    if (btnNo) btnNo.onclick = () => cambiarNotificaciones(false);
    if (btnSi) btnSi.onclick = () => cambiarNotificaciones(true);
});
