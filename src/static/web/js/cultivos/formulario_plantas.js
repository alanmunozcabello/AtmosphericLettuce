document.addEventListener('DOMContentLoaded', function () {
  // Elementos del DOM
  const btnDatosAdicionales = document.getElementById('btnDatosAdicionales')
  const camposAdicionales = document.getElementById('camposAdicionales')
  const otroRiegoRadio = document.getElementById('otro_riego_radio')
  const otroRiegoInput = document.getElementById('otro_riego')
  const tipoRiegoRadios = document.querySelectorAll('input[name="tipo_riego"]')
  const btnRegresar = document.getElementById('btnRegresar')
  const infoCultivo = document.getElementById('infoCultivo')
  const nombreCultivo = document.getElementById('nombreCultivo')
  const tituloGeneral = document.getElementById('tituloGeneral')
  const barra = document.getElementById("barraProgreso");
  const texto = document.getElementById("textoProgreso");
  let adicionalesVisible = false

  // Obtener parámetros de la URL
  const urlParams = new URLSearchParams(window.location.search)
  const cultivo = urlParams.get('cultivo')
  const correo = urlParams.get('correo')

  function actualizarProgreso() {
      // Selecciona TODOS los campos (visibles e invisibles)
      // Excluye campos opcionales como "otro_riego"
      const todosCampos = Array.from(document.querySelectorAll("input, select, textarea"))
        .filter(el => el.id !== 'otro_riego' && el.id !== 'btnRegresar'); // Excluir campos opcionales y botones

      let total = 0;
      let completados = 0;
      const radioGroups = new Set();

      todosCampos.forEach(el => {
        if (el.type === "radio") {
          if (!radioGroups.has(el.name)) {
            radioGroups.add(el.name);
            total++;
            const checked = document.querySelector(`input[name="${el.name}"]:checked`);
            if (checked) completados++;
          }
        } else {
          total++;
          if (el.value.trim() !== "") completados++;
        }
      });

      const progreso = total > 0 ? Math.round((completados / total) * 100) : 0;
      barra.style.width = `${progreso}%`;
      texto.textContent = `${progreso}%`;
    }

    // --- Escuchar cambios en los campos ---
    document.addEventListener("input", actualizarProgreso);
    document.addEventListener("change", actualizarProgreso);

    // --- Detectar cuando se abre/cierra "Datos adicionales" ---
    // No se recalcula aquí porque ya contamos todos los campos (visibles e invisibles)

    actualizarProgreso(); // cálculo inicial

  // Si viene de la página de cultivos, mostrar información específica
  if (cultivo && correo) {
    infoCultivo.style.display = 'block'
    tituloGeneral.style.display = 'none'
    nombreCultivo.textContent = cultivo

    // Configurar botón regresar
    btnRegresar.addEventListener('click', function () {
      window.location.href = `gestor_cultivos.html?correo=${encodeURIComponent(correo)}`
    })
  } else {
    // Si no viene de cultivos, ocultar botón regresar
    btnRegresar.style.display = 'none'
  }

  // Función para mostrar/ocultar campos adicionales
  btnDatosAdicionales.addEventListener('click', function () {
    if (adicionalesVisible) {
      camposAdicionales.style.display = 'none'
      btnDatosAdicionales.textContent = 'Datos adicionales'
      adicionalesVisible = false
    } else {
      camposAdicionales.style.display = 'block'
      btnDatosAdicionales.textContent = 'Ocultar datos adicionales'
      adicionalesVisible = true
    }
  })

  // Función para mostrar/ocultar el campo "Otro" tipo de riego
  tipoRiegoRadios.forEach(radio => {
    radio.addEventListener('change', function () {
      if (otroRiegoRadio.checked) {
        otroRiegoInput.style.display = 'block'
        otroRiegoInput.required = true
      } else {
        otroRiegoInput.style.display = 'none'
        otroRiegoInput.required = false
        otroRiegoInput.value = ''
      }
    })
  })

  // Manejar el envío del formulario
  const formulario = document.getElementById('formulario-plantas')
  formulario.addEventListener('submit', function (e) {
    e.preventDefault()

    // Validar que tenemos la información del cultivo
    if (!correo || !cultivo) {
      alert('⚠️ Error: Falta información del cultivo o usuario. Por favor accede desde la página de cultivos.')
      return
    }

    // Recopilar todos los datos del formulario
    const formData = new FormData(formulario)

    // Mapear los nombres de los campos del HTML a los nombres que espera el backend
    const datosParaBackend = {
      nombre_cultivo: cultivo,
      hectareas: 0,
      fecha_siembra: null,
      notas: null,
      etapa_planta: formData.get('etapa') || null,
      tipo_riego: formData.get('tipo_riego') || null,
      ultimo_riego: formData.get('ultimo_riego') || null,
      frecuencia_riego: formData.get('frecuencia') || null,
      humedad_suelo: formData.get('humedad_suelo') || null,
      textura_suelo: formData.get('textura') || null,
      variedad_planta: formData.get('variedad') || null,
      estado_planta: formData.get('estado_planta') || null,
      estres_hidrico: formData.get('estres_hidrico') ? (formData.get('estres_hidrico') === 'si' ? 1 : 0) : null,
      profundidad_radical: formData.get('profundidad_radical') ? parseInt(formData.get('profundidad_radical')) : null,
      densidad_plantacion: formData.get('densidad_plantacion') ? parseInt(formData.get('densidad_plantacion')) : null,
      tipo_sensor: formData.get('sensor_humedad') || null,
      eficiencia_riego: formData.get('eficiencia') ? parseFloat(formData.get('eficiencia')) : null,
      caudal: formData.get('caudal') ? parseFloat(formData.get('caudal')) : null,
      ph_agua: formData.get('ph_agua') ? parseFloat(formData.get('ph_agua')) : null,
      acolchado: formData.get('acolchado') ? (formData.get('acolchado') === 'si' ? 1 : 0) : null
    }

    console.log('Datos del formulario mapeados:', datosParaBackend)

    // Enviar al backend
    fetch(`/usuarios/${encodeURIComponent(correo)}/cultivos/modificar_formulario_cultivo`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(datosParaBackend)
    })
      .then(response => {
        if (!response.ok) {
          return response.text().then(text => {
            throw new Error(`HTTP ${response.status}: ${text || response.statusText}`)
          })
        }
        return response.json()
      })
      .then(data => {
        console.log('Respuesta del servidor:', data)
        if (data.mensaje) {
          alert(`✅ ${data.mensaje}`)
          window.location.href = 'gestor_cultivos.html'
        } else if (data.error) {
          alert(`❌ Error: ${data.error}`)
        }
      })
      .catch(error => {
        console.error('Error completo:', error)
        alert(`❌ Error al guardar la configuración del cultivo: ${error.message}`)
      })
  })
})
