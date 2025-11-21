/* global localStorage, location, history, document, alert, obtenerUsuario, actualizarCacheUsuario, FileReader */
document.addEventListener('DOMContentLoaded', () => {
  // URL base del backend FastAPI
  // Clave para guardar el perfil en localStorage
  if (!verificarSesionActiva()) {
    return
  }
  const LS_KEY = 'perfilAL'

  // ---cerrar sesion ---
  const logoutButton = document.getElementById('btn-logout')
  logoutButton.addEventListener('click', () => {
    /*localStorage.clear() // limpia todo (sesión, caches, etc.)
    location.replace('index.html') // redirige reemplazando la entrada del historial
    */
    cerrarSesion() // <-- Es de la función helper
  })

  // --- actualizar el correo en la URL sin recargar la página ---
  const replaceCorreoInURL = (nuevoCorreo) => {
    try {
      const url = new URL(location.href) // instancia un objeto URL con la URL actual
      url.searchParams.set('correo', nuevoCorreo) // cambia el parametro 'correo'
      history.replaceState(null, '', url.toString()) // reemplaza la URL en el historial sin recargar
    } catch { /* noop */ }
  }

  // Envia un JSON con { nombre, correo, ciudad, region } al endpoint PUT /usuarios/{correo}/modificar
  const putUsuario = async (correoActual, body) => {
    const url = `/usuarios/${encodeURIComponent(correoActual)}/modificar`
    /*const res = await fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' }, // se envía JSON
      body: JSON.stringify(body) // serializa el body a JSON
      */
    const res = await fetchConToken(url, {
      method: 'PUT',
      body: JSON.stringify(body)
    })

    // Si la respuesta no es postiva, lanza error con detalle
    if (!res || !res.ok) {
      const text = await res.text().catch(() => 'Error desconocido')
      throw new Error(`PUT falló: ${res.status} ${res.statusText} ${text}`)
    }

    // Intenta parsear el JSON de respuesta; si no hay, devuelve {}
    try {
      return await res.json()
    } catch {
      return {}
    }
  }

  // Prioriza el parametro correo, luego localStorage, si no hay nada, cadena vacía
  const CORREO = obtenerCorreoDelToken() ||
                 new URLSearchParams(location.search).get('correo') ||
                 localStorage.getItem('correoUsuario') ||
                 ''

  // Si no obtiene ni el token ni el correo entonces redirige al login, pero con jwt
  if (!CORREO) {
    console.warn('⚠️ Usuario no identificado')
    cerrarSesion()
    return // detiene el script
  }
  // Asegura persistencia del correo en localStorage
  localStorage.setItem('correoUsuario', CORREO)

  // --- referencias a la vistamodo lectura y modo edición---
  const nombreV = document.querySelector('.nombre') // título/nombre visible
  const filas = document.querySelectorAll('.tarjeta-perfil .fila') // filas de datos (correo, ciudad, región)
  const correoV = filas[0]?.querySelector('.valor') // span con valor de correo
  const ubicV = filas[1]?.querySelector('.valor')
  const regionV = filas[2]?.querySelector('.valor')
  const avatarV = document.querySelector('.avatar-fondo img') // imagen de avatar

  const form = document.getElementById('form-perfil') // formulario de edición
  const inpNombre = document.getElementById('inp-nombre') // input nombre
  const inpCorreo = document.getElementById('inp-correo')
  const inpUbic = document.getElementById('inp-ubicacion')
  const inpRegion = document.getElementById('inp-region')
  const inpAvatar = document.getElementById('inp-avatar')

  const btnEditar = document.getElementById('btn-editar') // botón para entrar en modo edición
  const btnGuardar = document.getElementById('btn-guardar')
  const btnCancelar = document.getElementById('btn-cancelar')

  // --- ayuda de LocalStorage (cache del perfil) ---
  const leerLS = () => {
    try {
      return JSON.parse(localStorage.getItem(LS_KEY) || 'null') // lee y parsea JSON; si no hay, null
    } catch {
      return null // si falla el parseo, devuelve null
    }
  }
  const guardarLS = (obj) => localStorage.setItem(LS_KEY, JSON.stringify(obj)) // guarda el objeto perfil como JSON

  // --- pintar hace que los datos se vean y guarden en el formuladrio  ---
  function pintar (data) {
    // Vista (labels/valores visibles)
    if (nombreV) nombreV.textContent = data.nombre ?? 'Usuario'
    if (correoV) correoV.textContent = data.correo ?? ''
    if (ubicV) ubicV.textContent = data.ubic ?? 'No especificada'
    if (regionV) regionV.textContent = data.region ?? 'No especificada'
    // if (avatarV && data.avatar) avatarV.src = data.avatar; // solo si hay avatar en data

    if (avatarV) {
      if (data.avatar && data.avatar.startsWith('data:')) {
        // Si hay avatar en formato base64, mostrarlo
        avatarV.src = data.avatar
        console.log('✅ Mostrando avatar desde cache/backend')
      } else if (data.foto_perfil && data.foto_perfil.startsWith('data:')) {
        // Si viene del backend con nombre foto_perfil
        avatarV.src = data.foto_perfil
        console.log('✅ Mostrando foto_perfil desde backend')
      } else {
        // Avatar por defecto o placeholder
        avatarV.src = 'img/avatar-default.png' // o cualquier imagen por defecto
        console.log('📷 Usando avatar por defecto')
      }
    }

    // Formulario (inputs editables)
    if (inpNombre) inpNombre.value = data.nombre ?? 'Usuario'
    if (inpCorreo) inpCorreo.value = data.correo ?? CORREO
    if (inpUbic) inpUbic.value = data.ubic ?? ''
    if (inpRegion) inpRegion.value = data.region ?? ''
  }

  // --- usa cache si existe si no, toma lo que ya está en la vista ---
  function cargarInicial () {
    const cached = leerLS() // intenta leer el perfil
    const base = cached || { // si no hay cache, arma un objeto base desde la vista/por defecto
      nombre: (nombreV?.textContent || 'Usuario').trim(),
      correo: (correoV?.textContent?.trim()) || CORREO,
      ubic: (ubicV?.textContent || '').trim(),
      region: (regionV?.textContent || '').trim(),
      avatar: null
    }
    guardarLS(base) // guarda en cache
    pintar(base) // muestra en en pantalla
  }

  // ---  GET /usuarios/{correo} ---
  async function syncConBackend () {
    try {
      const res = await fetchConToken(`/usuarios/${encodeURIComponent(CORREO)}`)

      if (!res || !res.ok) {
        console.warn('No se pudo cargar el perfil desde el backend')
        return
      }
      const usuario = await res.json()
      
      const previo = leerLS() || {} // lee lo que ya estaba en cache

      // A veces el backend puede mandar "nombre" con un email; lo tratamos para mostrar algo amigable
      const nombreSrv = (usuario?.nombre ?? '').trim() // nombre recibido
      const esEmail = nombreSrv.includes('@') // detecta si parece correo
      const displayName = esEmail
        ? (previo.nombre && !previo.nombre.includes('@') // si en cache ya teníamos un nombre lo usa
            ? previo.nombre
            : (CORREO.split('@')[0] || 'Usuario')) // si no, usa la parte antes de la @ como nombre
        : (nombreSrv || previo.nombre || 'Usuario') // si no es correo, usa el del server o el previo

      let avatarFinal = null
      if (usuario?.foto_perfil && usuario.foto_perfil.startsWith('data:')) {
        // Prioridad 1: Foto del backend
        avatarFinal = usuario.foto_perfil
        console.log('Foto de perfil cargada desde backend')
      } else if (previo.avatar && previo.avatar.startsWith('data:')) {
        // Prioridad 2: Foto del cache local
        avatarFinal = previo.avatar
        console.log('📸 Foto de perfil mantenida desde cache')
      }

      // Fusiona datos previos con los nuevos del backend (ubicación/region anidadas)
      const fusionado = {
        ...previo,
        nombre: displayName,
        correo: usuario?.correo ?? CORREO,
        ubic: usuario?.ubicacion?.ciudad ?? previo.ubic ?? '',
        region: usuario?.ubicacion?.region ?? previo.region ?? '',
        avatar: avatarFinal
      }

      guardarLS(fusionado) // actualiza cache
      pintar(fusionado) // y pantalla
    } catch (e) {
      console.warn('No se pudo sincronizar perfil:', e)
    }
  }

  // ---  muestra y oculta form y botones según estado ---
  function modoEdicion (on) {
    if (form) form.style.display = on ? 'block' : 'none'
    if (btnGuardar) btnGuardar.style.display = on ? 'inline-block' : 'none'
    if (btnCancelar) btnCancelar.style.display = on ? 'inline-block' : 'none'
    if (btnEditar) btnEditar.style.display = on ? 'none' : 'inline-block'
  }

  //  entra a modo edición y enfoca el nombre
  btnEditar?.addEventListener('click', () => {
    const data = leerLS() || {} // toma los datos actuales
    pintar(data) // sincroniza el form con esos datos
    modoEdicion(true) // muestra el formulario
    inpNombre?.focus() // enfoca el input de nombre
  })

  // Botón "Cancelar": sale de edición y restaura lo que hay en cache
  btnCancelar?.addEventListener('click', () => {
    modoEdicion(false) // oculta formulario
    const data = leerLS() || {} // recarga desde cache
    pintar(data) // repinta la vista
  })

  // ---valida, hace PUT al backend y actualiza los datos---
  btnGuardar?.addEventListener('click', async (e) => {
    e.preventDefault()
    if (!inpNombre || !inpCorreo) return // seguridad: requiere inputs clave

    // Limpia estados de error previos
    inpNombre.classList.remove('invalid')
    inpCorreo.classList.remove('invalid')
    inpUbic.classList.remove('invalid')
    inpRegion.classList.remove('invalid')

    // Toma valores nuevos del formulario (trim para limpiar espacios)
    const nombreNuevo = inpNombre.value.trim()
    const correoNuevo = (inpCorreo.value.trim() || CORREO).trim()
    const ciudadNueva = inpUbic.value.trim()
    const regionNueva = inpRegion.value.trim()

    // --- validaciones ---
    let valido = true

    // Nombre: obligatorio, 1-60 chars, solo letras y espacios (incluye tildes/ñ)
    if (!nombreNuevo) {
      inpNombre.classList.add('invalid')
      alert('El nombre es obligatorio')
      valido = false
    } else if (nombreNuevo.length < 1 || nombreNuevo.length > 60) {
      inpNombre.classList.add('invalid')
      alert('El nombre debe tener entre 1 y 60 caracteres')
      valido = false
    } else if (!/^[a-záéíóúüñA-ZÁÉÍÓÚÜÑ\s]+$/.test(nombreNuevo)) {
      inpNombre.classList.add('invalid')
      alert('El nombre solo puede contener letras y espacios')
      valido = false
    }

    // Correo: formato básico válido
    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correoNuevo)
    if (!correoNuevo || !emailOk) {
      inpCorreo.classList.add('invalid')
      alert('El correo electrónico debe tener un formato válido')
      valido = false
    }

    // Ciudad : solo letras y espacios
    if (ciudadNueva && !/^[a-záéíóúüñA-ZÁÉÍÓÚÜÑ\s]*$/.test(ciudadNueva)) {
      inpUbic.classList.add('invalid')
      alert('La ciudad solo puede contener letras y espacios')
      valido = false
    }

    // Región : solo letras y espacios
    if (regionNueva && !/^[a-záéíóúüñA-ZÁÉÍÓÚÜÑ\s]*$/.test(regionNueva)) {
      inpRegion.classList.add('invalid')
      alert('La región solo puede contener letras y espacios')
      valido = false
    }

    // Si no pasa validaciones, no continúa
    if (!valido) return

    // Indicadores de "guardando" para el botón
    btnGuardar.textContent = 'Guardando...'
    btnGuardar.classList.add('loading')
    btnGuardar.disabled = true

    // Lee el perfil previo del cache
    const previo = leerLS() || {}

    // obtener foto de perfil
    let fotoActual = ''
    if (avatarV?.src && avatarV.src.startsWith('data:')) {
      fotoActual = avatarV.src
    } else if (previo.avatar) {
      fotoActual = previo.avatar
    }

    // Construye el cuerpo que enviará al backend
    const body = {
      nombre: nombreNuevo,
      correo: correoNuevo,
      ciudad: ciudadNueva || '',
      region: regionNueva || '',
      foto_perfil: fotoActual || ''
    }

    try {
      // PUT al backend usando el correo previo
      await putUsuario(previo.correo || CORREO, body)

      actualizarCacheUsuario({
        nombre: nombreNuevo,
        correo: correoNuevo,
        ubicacion: {
          ciudad: ciudadNueva || '',
          region: regionNueva || ''
        }
      })

      //  Actualiza los datos locales con los nuevos valores
      const fusionado = {
        ...previo,
        nombre: nombreNuevo,
        correo: correoNuevo,
        ubic: ciudadNueva || previo.ubic || '',
        region: regionNueva || previo.region || '',
        avatar: fotoActual || previo.avatar || null
      }

      guardarLS(fusionado) // guarda en cache
      localStorage.setItem('correoUsuario', correoNuevo) // actualiza el correo de sesión
      replaceCorreoInURL(correoNuevo) // cambia ?correo=... en la URL sin recargar
      pintar(fusionado) // repinta vista y form
      modoEdicion(false) // sale de modo edición

      console.log('✅ Perfil actualizado correctamente')
    } catch (err) {
      console.error('❌ No se pudo guardar en backend:', err)
      alert('No se pudo actualizar tus datos en el servidor. Intenta nuevamente.')
    } finally {
      // Restablece el estado del botón "Guardar"
      btnGuardar.textContent = 'Guardar'
      btnGuardar.classList.remove('loading')
      btnGuardar.disabled = false
    }
  })

  // Al seleccionar un archivo, lo lee como DataURL (base64) y lo muestra en <img>
  inpAvatar?.addEventListener('change', () => {
    const file = inpAvatar.files?.[0] // toma el primer archivo seleccionado
    if (!file) return // si no hay archivo, no hace nada
    const reader = new FileReader() // lector de archivos del navegador
    reader.onload = () => { // cuando termina de leer
      if (avatarV) avatarV.src = reader.result // coloca la imagen en el <img>
    }
    reader.readAsDataURL(file) // lee el archivo como base64 (data URL)
  })

  // --- inicializacion al cargar pagina---
  cargarInicial() // pinta con cache o con lo que haya en la vista
  modoEdicion(false)
  syncConBackend() // trae datos desde el backend y los muestra
})

window.addEventListener('pageshow', (event) => {
  if (event.persisted) {
    console.log('⚠️ Perfil restaurado desde caché (botón Atrás)')
    
    // Verificar sesión activa
    if (!verificarSesionActiva()) {
      return // Redirige automáticamente a login
    }

    const correoUsuario = obtenerCorreoDelToken()
    if (!correoUsuario) {
      cerrarSesion()
      return
    }

    console.log('✅ Sesión válida en perfil restaurado')
  }
})