document.addEventListener('DOMContentLoaded', () => {
    // Obtener correo de localStorage o URL params
    const correoUsuario = new URLSearchParams(location.search).get('correo') 
                         || localStorage.getItem('correoUsuario');
    
    if (!correoUsuario) {
        console.warn("⚠️ Usuario no identificado");
        window.location.href = "index.html";
        return;
    }

    // Guardar/actualizar en localStorage
    localStorage.setItem('correoUsuario', correoUsuario);

    // Mostrar correo en la UI
    const correoElement = document.getElementById('correo-usuario');
    if (correoElement) {
        correoElement.textContent = correoUsuario;
    }

    // Manejar clic en logo
    const logo = document.querySelector('.logo img');
    if (logo) {
        logo.addEventListener('click', () => {
            window.location.href = 'home.html';
        });
    }
});

// Función global para cerrar sesión
function logout() {
    localStorage.removeItem('correoUsuario');
    window.location.href = 'index.html';
}