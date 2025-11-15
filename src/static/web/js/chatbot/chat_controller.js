document.addEventListener('DOMContentLoaded', () => {
  const chatToggle = document.getElementById('chatToggle')
  const chatWindow = document.getElementById('chatWindow')
  const closeChat = document.getElementById('closeChat')
  const fileBtn = document.getElementById('fileBtn')
  const fileInput = document.getElementById('fileInput')

  // Abrir/cerrar con el botón flotante
  chatToggle.addEventListener('click', () => {
    chatWindow.style.display = chatWindow.style.display === 'flex' ? 'none' : 'flex'
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
  const CORREO = localStorage.getItem('correoUsuario') || null;
  // const inputArchivos = document.getElementById('fileInput');

  // Arreglo con el payload final
  let payload = {
    pdf: [],
    imagen: []
  }

  showLoader() // comenzar animacion de carga

  // Caso 1: hay texto
  if (texto) {
    payload.texto = texto
  }
  // console.log(inputArchivos.files[0].name);

  textoInput.value = ''
  // mostrar la pregunta del usuario
  document.getElementById('chatBox').innerHTML += `
    <p><b>Tú:</b> ${texto}</p>
  `

  if (archivosSeleccionados.length > 0) {
    console.log('Archivos seleccionados:')
    for (let archivo of archivosSeleccionados) {
      // const archivo=inputArchivos.file[i];//<-- deberia iterar bien sobre los elementos
      console.log(archivo.name, archivo.type) // Muestra el nombre de cada archivo
      // Caso 2: hay archivo
      if (archivo.type === 'image/png' || archivo.type === 'image/jpeg') {
        const imagenBase64 = await leerArchivoBase64(archivo)
        // console.log("Imagen en base64:", imagen_base64);
        payload.imagen.push(imagenBase64) // se añade al payload la imagen en base64
      } else if (archivo.type === 'application/pdf') {
        const pdfBase64 = await leerArchivoBase64(archivo)
        // console.log("pdf en base64:", pdf_base64);
        payload.pdf.push(pdfBase64) // se añade al payload la imagen en base64
      }
    }
  }

  if(cultivoSeleccionado !== '(Sin cultivo)' && CORREO !== null){
    payload.cultivo = cultivoSeleccionado || null,
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
  const respuesta = await fetch('/chat/consulta', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

  const result = await respuesta.json()

  let formatted = 'Hubo un error, intente nuevamente más tarde.' // estado inicial como error

  if (result.success === undefined && typeof result.respuesta === 'string') { // por algun motivo solo cuando hay error existe success
    formatted = marked.parse(result.respuesta)
  }

  hideLoader() // terminar animacion de carga

  // mostrar respuesta del chatbot
  document.getElementById('chatBox').innerHTML += `
      <p><b>Lechuguin:</b> ${formatted}</p>
  `
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
