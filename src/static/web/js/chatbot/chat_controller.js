/* global localStorage, document, obtenerUsuario, obtenerCorreoDelToken, verificarSesionActiva, marked */

document.addEventListener('DOMContentLoaded', () => {
  const chatToggle = document.getElementById('chatToggle')
  const chatWindow = document.getElementById('chatWindow')
  const closeChat = document.getElementById('closeChat')
  const fileBtn = document.getElementById('fileBtn')
  const fileInput = document.getElementById('fileInput')

  // Cargar los cultivos en el selector
  cargarCultivosEnSelector()

  // Abrir/cerrar con el botón flotante
  chatToggle.addEventListener('click', () => {
    chatWindow.style.display = chatWindow.style.display === 'flex' ? 'none' : 'flex';
    cargarCultivosEnSelector()
  })

  // Cerrar con el circulito rojo
  closeChat.addEventListener('click', () => {
    chatWindow.style.display = 'none'
  })

  // cuando haces click en el botón, abre el input oculto
  fileBtn.addEventListener('click', () => {
    fileInput.click()
  })
})

let archivosSeleccionados = [] // lista global de los archivos seleccionados

fileInput.addEventListener('change', () => {
  const feedback = document.getElementById('fileFeedback')

  // Agregar los nuevos al arreglo
  archivosSeleccionados.push(...fileInput.files)

  // Limpiar el input real (para que puedas volver a elegir más tarde)
  fileInput.value = ''

  // Refrescar vista
  feedback.innerHTML = ''
  archivosSeleccionados.forEach((file, idx) => {
    const tag = document.createElement('div')
    tag.className = 'file-tag'
    tag.innerHTML = `${file.name} <span data-idx="${idx}">✖</span>`
    feedback.appendChild(tag)

    // evento para eliminar
    tag.querySelector('span').addEventListener('click', () => {
      archivosSeleccionados.splice(idx, 1)
      tag.remove()
    })
  })
})

// Eliminar archivo seleccionado con la X
document.getElementById('fileFeedback').addEventListener('click', (e) => {
  if (e.target.tagName === 'SPAN') {
    const idx = e.target.dataset.idx
    const dt = new DataTransfer()
    Array.from(fileInput.files).forEach((f, i) => {
      if (i !== idx) dt.items.add(f)
    })
    fileInput.files = dt.files

    // refrescar feedback
    const event = new Event('change')
    fileInput.dispatchEvent(event)
  }
})

const enviarBtn = document.getElementById('enviarBtn')

// Funciones para mostrar/ocultar loader en el botón
function showLoader () {
  // HTML From Uiverse.io by Shoh2008 (ENCAPSULADO EN EL JS PARA TENERLO DENTRO DEL BOTON Y NO COMO DIV APARTE)
  enviarBtn.innerHTML = `
    <div class="lds-ellipsis">
      <div></div><div></div><div></div><div></div>
    </div>
  `
  enviarBtn.disabled = true
}

function hideLoader () {
  enviarBtn.innerHTML = 'Enviar'
  enviarBtn.disabled = false
}

document.getElementById('enviarBtn').addEventListener('click', async () => {
  const textoInput = document.getElementById('textoInput')
  const texto = textoInput.value.trim()
  const cultivoSeleccionado = document.getElementById("cultivoSelect").value
  
  const CORREO = obtenerCorreoDelToken()
  // const inputArchivos = document.getElementById('fileInput');

  // Arreglo con el payload final
  let payload = {
    pdf: [],
    imagen: []
  }

  showLoader() // comenzar animacion de carga

  // Construir HTML con previews de archivos
  let mensajeHTML = '<p><b>Tú:</b> '

  // Caso 1: hay texto
  if (texto) {
    payload.texto = texto
    mensajeHTML += texto
  }
  // console.log(inputArchivos.files[0].name);

  textoInput.value = ''

  if (archivosSeleccionados.length > 0) {
    mensajeHTML += '<div class="archivo-previews">'
    
    for (let archivo of archivosSeleccionados) {
      console.log(archivo.name, archivo.type)
      // Caso 2: hay archivo
      if (archivo.type === 'image/png' || archivo.type === 'image/jpeg') {
        const imagenBase64 = await leerArchivoBase64(archivo)
        payload.imagen.push(imagenBase64)
        
        // Preview de imagen pequeña
        mensajeHTML += `
          <div class="file-preview image-preview">
            <img src="data:${archivo.type};base64,${imagenBase64}" 
                 alt="${archivo.name}" 
                 title="${archivo.name}">
          </div>
        `
      } 
      else if (archivo.type === 'application/pdf') {
        const pdfBase64 = await leerArchivoBase64(archivo)
        payload.pdf.push(pdfBase64)
        
        // Preview de PDF con ícono
        mensajeHTML += `
          <div class="file-preview pdf-preview">
            <svg class="pdf-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <span class="pdf-name">${archivo.name}</span>
          </div>
        `
      }
    }

    mensajeHTML += '</div>'
  }

  mensajeHTML += '</p>'

  // Mostrar mensaje con previews
  document.getElementById('chatBox').innerHTML += mensajeHTML

  if(cultivoSeleccionado !== '(Sin cultivo)' && CORREO){
    payload.cultivo = cultivoSeleccionado
    payload.correo = CORREO
  }

  // Si no hay nada, no enviamos
  if (!payload.texto && payload.pdf.length === 0 && payload.imagen.length === 0) {
    alert('Escribe algo o sube un archivo')
    hideLoader() // terminar animacion de carga
    return
  }

  // console.log(payload);

  // Enviar al backend
  try {
    const respuesta = await fetch('/chat/consulta', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (!respuesta.ok) {
      throw new Error(`Error ${respuesta.status}: ${respuesta.statusText}`)
    }

    const result = await respuesta.json()

    let formatted = 'Hubo un error, intente nuevamente más tarde.'

    if (result.success === undefined && typeof result.respuesta === 'string') {
      formatted = marked.parse(result.respuesta)
    } else if (result.error) {
      formatted = `Error: ${result.error}`
    }

    hideLoader()

    // Mostrar respuesta del chatbot
    document.getElementById('chatBox').innerHTML += `
      <p><b>Lechuguin:</b> ${formatted}</p>
    `

    // ✅ CAMBIO 4: Limpiar archivos después de enviar
    archivosSeleccionados = []
    document.getElementById('fileFeedback').innerHTML = ''

  } catch (error) {
    console.error('❌ Error en chatbot:', error)
    hideLoader()
    
    document.getElementById('chatBox').innerHTML += `
      <p><b>Lechuguin:</b> ❌ Error de conexión. Por favor, intenta nuevamente.</p>
    `
  }
})

function leerArchivoBase64 (archivo) { // comvertir archivo imagen o pdf a base64
  return new Promise((resolve, reject) => {
    const lector = new FileReader()
    lector.onloadend = () => {
      resolve(lector.result.split(',')[1]) // devuelve solo la parte base64
    }
    lector.onerror = reject
    lector.readAsDataURL(archivo)
  })
}

// Carga cultivos y los agrega al selector
async function cargarCultivosEnSelector() {
  const select = document.getElementById('cultivoSelect')
  if (!select) {
    console.warn('⚠️ No se encontró el selector de cultivos')
    return
  }

  if (typeof verificarSesionActiva === 'function' && !verificarSesionActiva()) {
    console.warn('⚠️ No hay sesión activa')
    return
  }
  // Obtener correo del usuario
  const CORREO = obtenerCorreoDelToken()
  
  if (!CORREO) {
    console.warn('⚠️ No hay correo de usuario')
    return
  }

  try {
    // Obtener datos del usuario desde el backend
    const usuario = await obtenerUsuario(CORREO)
    
    if (!usuario) {
      console.warn('⚠️ No se encontró usuario')
      return
    }

    // Obtener array de cultivos
    const cultivos = usuario.cultivos || []

    // Limpiar selector (mantener solo "Sin cultivo")
    select.innerHTML = '<option value="">(Sin cultivo)</option>'

    // ✅ Validar si hay cultivos
    if (!Array.isArray(cultivos) && cultivos.mensaje === 'Usuario no posee cultivos') {
      console.log('ℹ️ Usuario sin cultivos registrados')
      return
    }

    // Agregar cada cultivo al selector
    cultivos.forEach(cultivo => {
      const option = document.createElement('option')
      const nombreCultivo = cultivo.nombre_cultivo || cultivo.nombre
      option.value = nombreCultivo
      option.textContent = nombreCultivo
      select.appendChild(option)
    })

    console.log(`✅ ${cultivos.length} cultivos cargados en el selector`)

  } catch (error) {
    console.error('❌ Error cargando cultivos:', error)
  }
}