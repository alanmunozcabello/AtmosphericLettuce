// Espera a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', () => {
  const LS_KEY = 'cultivos'; // Clave para localStorage

  // Obtiene los elementos del formulario, input y lista desde el HTML
  const form = document.getElementById('form-cultivo');
  const input = document.getElementById('input-cultivo');
  const lista = document.getElementById('lista-cultivos');

  // Verificación de que los elementos existen en el HTML
  if (!form || !input || !lista) {
    console.error('⚠️ Faltan elementos en el HTML: asegúrate de haber pegado la tarjeta con los IDs form-cultivo, input-cultivo y lista-cultivos.');
    return;
  }

  // Función para leer los cultivos desde localStorage
  const leer = () => JSON.parse(localStorage.getItem(LS_KEY) || '[]');
  // Función para guardar los cultivos en localStorage
  const guardar = (arr) => localStorage.setItem(LS_KEY, JSON.stringify(arr));

  // Renderiza la lista de cultivos en el DOM
  function render() {
    lista.innerHTML = ''; // Limpia la lista antes de renderizar
    let cultivos = leer();

    // Si no hay cultivos, inicializa el array y lo guarda
    if (cultivos.length === 0) {
      cultivos = [];
      guardar(cultivos);
    }

    // Por cada cultivo, crea un elemento <li> y lo agrega a la lista
    cultivos.forEach((nombre, i) => {
      const li = document.createElement('li');
      li.className = 'item-cultivo';
      li.innerHTML = `<span class="tick">✔</span>
        <span>${nombre}</span>
        <button class="btn-eliminar" data-i="${i}" aria-label="Eliminar ${nombre}">✕</button>
      `;
      lista.appendChild(li);
    });
  }

  // Evento al enviar el formulario para agregar un cultivo
  form.addEventListener('submit', (e) => {
    e.preventDefault(); // Evita el envío tradicional del formulario
    let v = input.value.trim(); // Obtiene el valor y elimina espacios

    if (!v) return; // Si el input está vacío, no hace nada

    // Normalizar a minúsculas para comparar
    const norm = (s) => s.toLowerCase();
    const cultivos = leer();

    // Verificar si ya existe (sin importar mayúsculas/minúsculas)
    if (cultivos.map(norm).includes(norm(v))) {
      alert(`⚠️ El cultivo "${v}" ya existe en la lista.`);
      input.value = '';
      input.focus();
      return;  // salimos sin agregar
    }

    // Capitalizar primera letra
    v = v.charAt(0).toUpperCase() + v.slice(1);

    cultivos.push(v);      // Agrega el cultivo al array
    guardar(cultivos);     // Guarda el array actualizado en localStorage
    render();              // Actualiza la lista en el DOM

    input.value = '';      // Limpia el input
    input.focus();         // Enfoca el input
  });

  // Evento para eliminar un cultivo al hacer clic en el botón de eliminar
  lista.addEventListener('click', (e) => {
    if (e.target.matches('.btn-eliminar')) {
      const i = Number(e.target.dataset.i); // Obtiene el índice del cultivo
      const cultivos = leer();
      cultivos.splice(i, 1); // Elimina el cultivo del array
      guardar(cultivos);     // Guarda el array actualizado
      render();              // Actualiza la lista en el DOM
    }
  });

  render(); // Renderiza la lista al cargar la página
});