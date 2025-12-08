/* global localStorage, alert, location, document */
document.addEventListener('DOMContentLoaded', () => {

  // Referencias a los elementos del formulario de registro
  const form = document.getElementById('register-form') // <form> principal
  const nombre = document.getElementById('nombre') // input: nombre
  const email = document.getElementById('email') // input: correo
  const pass = document.getElementById('password') // input: contraseña
  const pass2 = document.getElementById('confirm-password') // input: confirmar contraseña
  const btn = document.getElementById('btn-register') // botón: Crear cuenta

  let arr = [nombre, email, pass, pass2]
  // Al escribir en cualquier input, quita la clase 'invalid' para limpiar estado de error
  arr.forEach(inp => {
    inp.addEventListener('input', () => inp.classList.remove('invalid'))
  })

  // Maneja el submit del formulario (crear cuenta)
  form.addEventListener('submit', async (e) => {
    e.preventDefault(); // evita la recarga de la página por el submit HTML

    // Limpia estados de error previos
    arr.forEach(i => i.classList.remove('invalid'))

    // Flags/valores actuales del formulario
    let ok = true
    const vNombre = nombre.value.trim()
    const vEmail = email.value.trim()
    const vPass = pass.value.trim()
    const vPass2 = pass2.value.trim()

    // Validación de nombre:
    if (!vNombre || vNombre.length < 1 || vNombre.length > 60 || !/^[a-záéíóúüñA-ZÁÉÍÓÚÜÑ\s]+$/.test(vNombre)) {
      nombre.classList.add('invalid')
      ok = false
    }

    // Validación de correo:
    if (!vEmail || vEmail.length < 10 || vEmail.length > 70 || !vEmail.includes('@') || !vEmail.includes('.')) {
      email.classList.add('invalid')
      ok = false
    }

    // Validación de contraseña:
    if (!vPass ||
      vPass.length < 6 ||
      vPass.length > 25 ||
      !/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/.test(vPass) ||
      /['";]/.test(vPass)) {
      pass.classList.add('invalid')
      ok = false
    }

    // Validación de confirmacion de las contraseñas:
    if (!vPass2 || vPass2 !== vPass) {
      pass2.classList.add('invalid')
      ok = false
    }

    // Si algo falló en las validaciones, no continúa
    if (!ok) return

    // Estado visual de "creando cuenta" en el botón
    const originalText = btn.textContent
    btn.textContent = 'Creando cuenta...'
    btn.classList.add('loading')
    btn.disabled = true

    try {
      // Endpoint para registrar usuarios en tu backend
      const REGISTER_URL = '/usuarios/registrar'

      // Llamada POST con el cuerpo en JSON
      const resp = await fetch(REGISTER_URL, {
        method: 'POST',
        headers: {
          Accept: 'application/json', // preferimos al JSON en la respuesta
          'Content-Type': 'application/json' // enviamos al JSON
        },
        body: JSON.stringify({
          correo: vEmail, // email del usuario
          nombre: vNombre, // nombre del usuario
          contrasena: vPass // contraseña del usuario
        })
      })

      // Intenta leer la respuesta como JSON si el servidor avisa content-type JSON;
      // de lo contrario, la lee como texto (evita errores de parseo)
      let body = null
      const contentType = resp.headers.get('content-type') || ''
      if (contentType.includes('application/json')) {
        body = await resp.json()
      } else {
        body = await resp.text()
      }

      // Manejo de la respuesta
      if (resp.ok) {
        // Si el backend responde con {detail} o {error}, lo mostramos
        if (body && (body.detail || body.error)) {
          const detail = body.detail || body.error;
          if (Array.isArray(detail)) {
            // Formatear errores de Pydantic
            let errores = detail.map(e => e.msg.replace('Value error, ', '')).join('\n');
            alert(errores);
          } else if (typeof detail === 'object') {
            alert(JSON.stringify(detail));
          } else {
            alert(detail);
          }
        } else {
          console.log('Usuario registrado:', body)
          alert('Cuenta creada correctamente')
          window.location.href = 'login.html'
        }
      } else if (resp.status === 400) {
        // Errores típicos de datos inválidos o usuario ya existente
        alert('Error: datos inválidos o usuario ya existe')
      } else {
        // Otros códigos de error del servidor
        alert(`Error del servidor: ${resp.status}`)
        console.error(body)
      }
    } catch (error) {
      // Errores de red/conexión o excepciones no controladas
      console.error('Error al conectar con el servidor:', error)
      alert('No se pudo conectar con el servidor. Revisa la consola.')
    } finally {
      // Restaura el estado del botón siempre
      btn.textContent = originalText
      btn.classList.remove('loading')
      btn.disabled = false
    }
  })
})
