document.addEventListener('DOMContentLoaded', () => {
    // Referencias a elementos
    const btnNotificaciones = document.getElementById('btn-notificaciones'); // El botón de la campana

    // Crear el HTML del modal dinámicamente si no existe
    if (!document.getElementById('modal-notificaciones')) {
        const modalHTML = `
            <div id="modal-notificaciones" class="modal-notificaciones-overlay">
                <div class="modal-notificaciones-content">
                    <button id="btn-cerrar-noti" class="btn-cerrar-modal">&times;</button>
                    <h2>🔔 Notificaciones</h2>
                    <p>¿Deseas recibir notificaciones de tus cultivos?</p>
                    <span id="estado-noti-texto" class="estado-notificaciones">Cargando estado...</span>
                    
                    <div class="botones-notificaciones">
                        <button id="btn-noti-no" class="btn-noti btn-desactivar" title="Desactivar Notificaciones">
                            ✕
                        </button>
                        <button id="btn-noti-si" class="btn-noti btn-activar" title="Activar Notificaciones">
                            ✓
                        </button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    const modal = document.getElementById('modal-notificaciones');
    const btnCerrar = document.getElementById('btn-cerrar-noti');
    const btnNo = document.getElementById('btn-noti-no');
    const btnSi = document.getElementById('btn-noti-si');
    const estadoTexto = document.getElementById('estado-noti-texto');

    // Funciones
    async function obtenerEstadoNotificaciones() {
        const token = localStorage.getItem('token');
        const correo = localStorage.getItem('correoUsuario');

        if (!token || !correo) return;

        try {
            const response = await fetch(`/usuarios/${correo}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const usuario = await response.json();
                actualizarUIEstado(usuario.notificaciones);
            }
        } catch (error) {
            console.error('Error al obtener notificaciones:', error);
            estadoTexto.textContent = "Error al obtener estado";
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
            // Nota: El backend espera recibir el booleano como string 'true' o 'false' en la URL o procesarlo como bool.
            // Python FastAPI con bool en path suele esperar title case "True"/"False" o "1"/"0" o "true"/"false".
            // Vamos a probar con enviar el valor en la URL.

            const url = `/usuarios/${correo}/modificar_notificaciones/${activar}`;

            const response = await fetch(url, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const resultado = await response.json();
                // El backend devuelve el usuario modificado o un mensaje?
                // Revisando el service: return service_modificar_notificaciones_usuario(...)
                // Asumiremos que devuelve éxito si es 200.
                actualizarUIEstado(activar);
                // Opcional: Cerrar modal después de elegir
                // cerrarModal(); 
            } else {
                console.error('Error al modificar notificaciones');
                alert("No se pudo actualizar la preferencia.");
            }
        } catch (error) {
            console.error('Error de red:', error);
            alert("Error de conexión.");
        }
    }

    function actualizarUIEstado(activo) {
        if (activo) {
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
        modal.classList.add('activo');
        obtenerEstadoNotificaciones();
    }

    function cerrarModal() {
        modal.classList.remove('activo');
    }

    // Event Listeners
    if (btnNotificaciones) {
        btnNotificaciones.addEventListener('click', (e) => {
            e.preventDefault();
            abrirModal();
        });
    }

    btnCerrar.addEventListener('click', cerrarModal);

    // Cerrar si se hace click fuera del contenido
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            cerrarModal();
        }
    });

    btnNo.addEventListener('click', () => cambiarNotificaciones(false));
    btnSi.addEventListener('click', () => cambiarNotificaciones(true));
});
