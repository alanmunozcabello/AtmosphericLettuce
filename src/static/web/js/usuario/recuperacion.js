
document.addEventListener('DOMContentLoaded', () => {
    // Referencias a elementos del DOM
    const formSolicitar = document.getElementById('form-solicitar');
    const formVerificar = document.getElementById('form-verificar');
    const formCambio = document.getElementById('form-cambio');

    const containerSolicitar = document.getElementById('step-solicitar');
    const containerVerificar = document.getElementById('step-verificar');
    const containerCambio = document.getElementById('step-cambio');

    let correoUsuario = '';
    let codigoVerificado = '';

    // --- PASO 1: SOLICITAR CÓDIGO ---
    if (formSolicitar) {
        formSolicitar.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emailInput = document.getElementById('email-solicitar');
            correoUsuario = emailInput.value.trim();

            if (!correoUsuario) return mostrarError('Ingresa tu correo');

            mostrarLoading(true);
            try {
                const response = await fetch('/api/recuperacion/solicitar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ correo: correoUsuario })
                });

                const data = await response.json();

                if (response.ok) {
                    mostrarExito(data.mensaje);
                    cambiarPaso(containerSolicitar, containerVerificar);
                } else {
                    mostrarError(data.detail || 'Error al solicitar código');
                }
            } catch (error) {
                mostrarError('Error de conexión');
            } finally {
                mostrarLoading(false);
            }
        });
    }

    // --- PASO 2: VERIFICAR CÓDIGO ---
    if (formVerificar) {
        formVerificar.addEventListener('submit', async (e) => {
            e.preventDefault();
            const codigoInput = document.getElementById('codigo-verificar');
            const codigo = codigoInput.value.trim();

            if (!codigo) return mostrarError('Ingresa el código');

            mostrarLoading(true);
            try {
                const response = await fetch('/api/recuperacion/verificar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ correo: correoUsuario, codigo: codigo })
                });

                const data = await response.json();

                if (response.ok) {
                    codigoVerificado = codigo;
                    mostrarExito('Código verificado correctamente');
                    cambiarPaso(containerVerificar, containerCambio);
                } else {
                    mostrarError(data.detail || 'Código incorrecto');
                }
            } catch (error) {
                mostrarError('Error de conexión');
            } finally {
                mostrarLoading(false);
            }
        });
    }

    // --- PASO 3: CAMBIAR CONTRASEÑA ---
    if (formCambio) {
        formCambio.addEventListener('submit', async (e) => {
            e.preventDefault();
            const pass1 = document.getElementById('new-password').value;
            const pass2 = document.getElementById('confirm-password').value;

            if (pass1 !== pass2) return mostrarError('Las contraseñas no coinciden');
            if (pass1 !== pass2) return mostrarError('Las contraseñas no coinciden');
            if (pass1.length < 6) return mostrarError('La contraseña debe tener al menos 6 caracteres');
            if (/['";]/.test(pass1)) return mostrarError('La contraseña no puede contener caracteres como comillas o punto y coma');

            mostrarLoading(true);
            try {
                const response = await fetch('/api/recuperacion/cambiar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        correo: correoUsuario,
                        codigo: codigoVerificado,
                        nueva_contrasena: pass1
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    alert('Contraseña actualizada exitosamente. Ahora puedes iniciar sesión.');
                    window.location.href = 'login.html';
                } else {
                    mostrarError(data.detail || 'Error al cambiar contraseña');
                }
            } catch (error) {
                mostrarError('Error de conexión');
            } finally {
                mostrarLoading(false);
            }
        });
    }
});

// Funciones auxiliares
function cambiarPaso(actual, siguiente) {
    actual.style.display = 'none';
    siguiente.style.display = 'block';
}

function mostrarError(msg) {
    // Si es un array (errores de Pydantic), lo formateamos
    if (Array.isArray(msg)) {
        let errores = msg.map(e => {
            // Si el mensaje es "Value error, nnnn", limpiamos el prefijo
            return e.msg.replace('Value error, ', '');
        }).join('\n');
        alert(errores);
        return;
    }

    // Si es un objeto genérico
    if (typeof msg === 'object') {
        alert(JSON.stringify(msg));
        return;
    }

    // String normal
    alert(msg);
}

function mostrarExito(msg) {
    alert(msg);
}

function mostrarLoading(show) {
    const loading = document.getElementById('loadingScreen');
    if (loading) {
        loading.style.display = show ? 'flex' : 'none';
    }
}
