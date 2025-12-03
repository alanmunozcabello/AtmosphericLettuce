/* global obtenerClimaDia, obtenerClimaSemana, document, window */

document.addEventListener('DOMContentLoaded', async () => {
  if (window.location.pathname.includes('home.html')) {
    // Solo cargar clima si estamos en home.html
    if (typeof cargarClimaHome === 'function') {
      await cargarClimaHome()
    }
    await cargarConsejosClima()

    // Marcar como listo
    window.climaCargado = true
  }
})

async function cargarClimaHome () {
  console.log('🌤️ Iniciando carga de clima para home...')

  // Verificar que la función existe
  if (typeof obtenerClimaDia !== 'function') {
    console.error('❌ obtenerClimaDia no está disponible')
    mostrarClimaFallback()
    window.climaCargado = true
    return
  }

  // Mostrar estado de carga
  const temperatura = document.querySelector('.clima-card .temperatura')
  const descripcion = document.querySelector('.clima-card .descripcion')

  if (temperatura) temperatura.textContent = 'Cargando...'
  if (descripcion) descripcion.textContent = 'Obteniendo clima...'

  try {
    // Obtener datos del clima (con cache incluido)
    const clima = await obtenerClimaDia()
    const climaSemana = await obtenerClimaSemana()

    // ✅ VALIDAR que climaSemana tiene datos antes de acceder
    if (!climaSemana || !climaSemana['1']) {
      console.warn('⚠️ climaSemana no tiene datos válidos:', climaSemana)
      mostrarClimaFallback()
      window.climaCargado = true
      return
    }

    clima.min = climaSemana['1'].min
    clima.max = climaSemana['1'].max

    if (clima) {
      mostrarClimaEnHome(clima)
    } else {
      mostrarClimaFallback()
    }
  } catch (error) {
    console.error('❌ Error cargando clima:', error)
    mostrarClimaFallback()
  } finally {
    window.climaCargado = true
  }
}

// Resto de funciones sin cambios...
function mostrarClimaEnHome (datosClima) {
  if (!datosClima) {
    console.log('❌ No hay datos de clima para mostrar')
    return
  }

  const temperatura = document.querySelector('.clima-card .temperatura')
  const descripcion = document.querySelector('.clima-card .descripcion')
  const tempMax = document.querySelector('.clima-card .max')
  const tempMin = document.querySelector('.clima-card .min')
  const iconoClima = document.querySelector('.clima-card .icono-clima')

  const humedad = document.querySelector('.detalles .info-detalles .humedad')
  const viento = document.querySelector('.detalles .info-detalles .viento')
  const sensacion = document.querySelector('.detalles .info-detalles .sensacion')


  if (temperatura) {
    temperatura.textContent = `${Math.round(datosClima.temp || 0)}°C`
  }

  if (descripcion) {
    descripcion.textContent = datosClima.estado || 'No disponible'
  }

  if (tempMax) {
    tempMax.textContent = `Máx: ${Math.round(datosClima.max || 0)}°C`
  }

  if (tempMin) {
    tempMin.textContent = `Mín: ${Math.round(datosClima.min || 0)}°C`
  }

  if (iconoClima) {
    const icono = obtenerIconoClima(datosClima.estado || '')
    iconoClima.textContent = icono
  }

  if(humedad){
    humedad.textContent = `${datosClima.humidity || 0}%`  // Humedad
  }

  if(viento){
    viento.textContent = `${Math.round(datosClima.wind_kmh || 0)} km/h`  // Viento
  }
  
  if(sensacion){
    sensacion.textContent = `${Math.round(datosClima.sence || 0)}°C`  // Sensación térmica
  }

  console.log('✅ Clima actualizado en home')
}

function obtenerIconoClima (descripcion) {
  const desc = descripcion.toLowerCase()

  if (desc.includes('clear') || desc.includes('sunny')) {
    return '☀️'
  } else if (desc.includes('cloud')) {
    return '☁️'
  } else if (desc.includes('rain')) {
    return '🌧️'
  } else if (desc.includes('storm')) {
    return '⛈️'
  } else if (desc.includes('snow')) {
    return '❄️'
  } else {
    return '🌤️'
  }
}

function mostrarClimaFallback () {
  const climaPorDefecto = {
    temp: 20,
    max: 25,
    min: 15,
    estado: 'No disponible'
  }

  mostrarClimaEnHome(climaPorDefecto)
  console.log('📦 Mostrando clima por defecto')
}

// ========== CONSEJOS DEL CLIMA ==========
async function cargarConsejosClima() {
  console.log('💡 Cargando consejos del clima...')
  
  try {
    const datosClimaDia = await obtenerClimaDia()
    
    if (!datosClimaDia) {
      console.warn('⚠️ No hay datos de clima para generar consejos')
      mostrarConsejosFallback()
      return
    }

    const consejos = generarConsejos(datosClimaDia)
    mostrarConsejos(consejos)

  } catch (error) {
    console.error('❌ Error cargando consejos:', error)
    mostrarConsejosFallback()
  }
}

function generarConsejos(clima) {
  const consejos = []
  
  // Obtener datos del clima
  const temp = clima.temp || 0
  const humedad = clima.humidity || 0
  const lluvia = clima.rain || 0
  const viento = clima.wind_kmh || 0
  const descripcion = (clima.estado || '').toLowerCase()

  console.log('📊 Datos para consejos:', { temp, humedad, lluvia, viento, descripcion })

  // ========== Consejos por temperatura ==========
  if (temp > 30) {
    consejos.push('🌡️ Temperatura alta: Aumenta la frecuencia de riego, especialmente en horas tempranas.')
  } else if (temp > 25) {
    consejos.push('☀️ Temperatura cálida: Monitorea la humedad del suelo regularmente.')
  } else if (temp < 5) {
    consejos.push('❄️ Temperatura baja: Protege tus cultivos sensibles a heladas.')
  } else if (temp < 10) {
    consejos.push('🌡️ Temperatura fresca: Reduce la frecuencia de riego.')
  }

  // ========== Consejos por humedad ==========
  if (humedad > 80) {
    consejos.push('💧 Humedad alta: Reduce el riego para evitar enfermedades fúngicas.')
  } else if (humedad < 30) {
    consejos.push('🏜️ Humedad baja: Considera riego por goteo para mantener humedad del suelo.')
  }

  // ========== Consejos por lluvia ==========
  if (lluvia > 10) {
    consejos.push('🌧️ Se esperan lluvias: Suspende el riego programado por hoy.')
  } else if (lluvia > 0) {
    consejos.push('🌦️ Lluvia ligera esperada: Monitorea el suelo antes de regar.')
  }

  // ========== Consejos por viento ==========
  if (viento > 30) {
    consejos.push('💨 Vientos fuertes: Asegura estructuras y protege plantas jóvenes.')
  } else if (viento > 20) {
    consejos.push('🌬️ Viento moderado: Verifica sistemas de riego y tutores.')
  }

  // ========== Consejos generales por descripción ==========
  if (descripcion.includes('clear') || descripcion.includes('sunny')) {
    consejos.push('☀️ Día despejado: Ideal para aplicar fertilizantes foliares en horas tempranas.')
  }

  if (descripcion.includes('storm')) {
    consejos.push('⛈️ Tormenta cercana: Evita trabajos en campo y asegura sistemas de riego.')
  }

  if (descripcion.includes('cloud') && !descripcion.includes('rain')) {
    consejos.push('☁️ Día nublado: Buen momento para realizar podas y mantenimiento.')
  }

  // ========== Si no hay consejos específicos ==========
  if (consejos.length === 0) {
    consejos.push('🌱 Clima estable: Buen día para monitorear tus cultivos y realizar mantenimiento.')
  }

  console.log(`✅ ${consejos.length} consejos generados`)
  return consejos
}

function mostrarConsejos(consejos) {
  const contenedorConsejos = document.getElementById('consejos-clima')
  
  if (!contenedorConsejos) {
    console.warn('⚠️ No se encontró contenedor de consejos (#consejos-clima)')
    return
  }

  // Limpiar contenedor
  contenedorConsejos.innerHTML = ''

  // Agregar cada consejo
  consejos.forEach((consejo, index) => {
    const divConsejo = document.createElement('div')
    divConsejo.className = 'consejo-item'
    divConsejo.textContent = consejo
    
    // Pequeña animación de entrada (opcional)
    setTimeout(() => {
      divConsejo.style.opacity = '1'
      divConsejo.style.transform = 'translateX(0)'
    }, index * 100)
    
    contenedorConsejos.appendChild(divConsejo)
  })

  console.log(`✅ ${consejos.length} consejos mostrados en la interfaz`)
}

function mostrarConsejosFallback() {
  const contenedorConsejos = document.getElementById('consejos-clima')
  
  if (!contenedorConsejos) {
    console.warn('⚠️ No se encontró contenedor de consejos')
    return
  }
  
  contenedorConsejos.innerHTML = `
    <div class="consejo-item loading">
      🌱 No se pudieron cargar los consejos del clima
    </div>
  `
  
  console.log('📦 Mostrando consejos fallback')
}