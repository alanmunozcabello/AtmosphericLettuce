/* global obtenerClimaSemana, document */
document.addEventListener('DOMContentLoaded', async () => {
  // Esperar un poco para que otros scripts se inicialicen
  setTimeout(async () => {
    if (typeof cargarClimaSemana === 'function') {
      await cargarClimaSemana()
    }
  }, 1000)
})

async function cargarClimaSemana() {

  try {
    // Obtener datos del clima semanal
    const climaSemana = await obtenerClimaSemana()

    if (climaSemana) {
      mostrarClimaSemanaEnDias(climaSemana)
    } else {
      mostrarClimaFallbackSemana()
    }
  } catch (error) {
    console.error('❌ Error cargando clima semanal:', error)
    mostrarClimaFallbackSemana()
  } finally {
    // Marcar como listo
    window.climaSemanaCargado = true
  }
}

function mostrarClimaSemanaEnDias(climaSemana) {
  const tarjetas = document.querySelectorAll('.clima-card')

  for (let i = 1; i <= 7; i++) {
    const diaData = climaSemana[i.toString()]
    if (!diaData) continue

    const tarjeta = tarjetas[i - 1] // Las tarjetas están indexadas desde 0
    if (!tarjeta) continue

    // Actualizar contenido de cada tarjeta
    const dia = tarjeta.querySelector('.dia')
    const temperatura = tarjeta.querySelector('.temperatura')
    const tempMax = tarjeta.querySelector('.max')
    const tempMin = tarjeta.querySelector('.min')
    const descripcion = tarjeta.querySelector('.descripcion')
    const icono = tarjeta.querySelector('.icono-clima')

    if (dia) dia.textContent = diaData.dia
    if (temperatura) temperatura.textContent = `${Math.round(diaData.temp)}°C`
    if (tempMax) tempMax.textContent = `Máx: ${Math.round(diaData.max)}°C`
    if (tempMin) tempMin.textContent = `Mín: ${Math.round(diaData.min)}°C`
    if (descripcion) descripcion.textContent = diaData.estado
    if (icono) icono.textContent = obtenerIconoClima(diaData.estado)
  }

}

function mostrarClimaFallbackSemana() {
  // Mantener los datos hardcodeados como fallback
}

function obtenerIconoClima(estado) {
  const desc = estado.toLowerCase()

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
