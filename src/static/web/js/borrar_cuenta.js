document.addEventListener('DOMContentLoaded', () => {
  const API_BASE = 'http://localhost:8000';
  const correoUsuario = localStorage.getItem('correoUsuario');

  const btnDelete = document.getElementById('btn-delete');
  const alerta = document.getElementById('alerta-borrar');
  const btnCancelar = document.getElementById('btn-cancelar-borrar');
  const btnConfirmar = document.getElementById('btn-confirmar-borrar');

  // --- Abrir alerta ---
  if (btnDelete) {
    btnDelete.addEventListener('click', () => {
      alerta.style.display = 'flex'; // mostrar alerta
    });
  }

  // --- Cancelar ---
  btnCancelar.addEventListener('click', () => {
    alerta.style.display = 'none';
  });

  // --- Confirmar borrado ---
  btnConfirmar.addEventListener('click', async () => {
    try {
      const res = await fetch(`${API_BASE}/usuarios/${encodeURIComponent(correoUsuario)}`, {
        method: 'DELETE'
      });

      if (res.ok) {
        alert("✅ Cuenta eliminada correctamente");
        localStorage.clear();

        // Redirige y evita volver atrás
        window.location.replace("index.html");
        window.history.pushState(null, "", window.location.href);
        window.onpopstate = function () {
          window.history.go(1);
        };
      } else {
        const errorMsg = await res.text();
        alert("❌ Error al borrar cuenta: " + errorMsg);
      }
    } catch (err) {
      console.error("Error en la petición DELETE", err);
      alert("❌ No se pudo conectar al servidor");
    }
  });

  // --- Cerrar si se hace clic fuera de la alerta ---
  window.addEventListener('click', (e) => {
    if (e.target === alerta) {
      alerta.style.display = 'none';
    }
  });

  // --- Cerrar con tecla ESC ---
  window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
      alerta.style.display = 'none';
    }
  });
});
