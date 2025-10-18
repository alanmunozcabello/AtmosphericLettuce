async function cargarClimaHome() {
    console.log('🌤️ Iniciando carga de clima para home...');
  
    // Verificar que la función existe
    if (typeof obtenerClimaDia !== 'function') {
        console.error('❌ obtenerClimaDia no está disponible');
        mostrarClimaFallback();
        return;
    }

    // Mostrar estado de carga
    const temperatura = document.querySelector('.clima-card .temperatura');
    const descripcion = document.querySelector('.clima-card .descripcion');
  
    if (temperatura) temperatura.textContent = 'Cargando...';
    if (descripcion) descripcion.textContent = 'Obteniendo clima...';

    try {
        // Obtener datos del clima (con cache incluido)
        const clima = await obtenerClimaDia();
        const clima_semana = await obtenerClimaSemana();

        clima.min = clima_semana["1"].min;
        clima.max = clima_semana["1"].max;
        
        if (clima) {
            mostrarClimaEnHome(clima);
        } else {
            mostrarClimaFallback();
        }
    } catch (error) {
        console.error('❌ Error cargando clima:', error);
        mostrarClimaFallback();
    }
}

// Resto de funciones sin cambios...
function mostrarClimaEnHome(datosClima) {
    if (!datosClima) {
        console.log('❌ No hay datos de clima para mostrar');
        return;
    }

    const temperatura = document.querySelector('.clima-card .temperatura');
    const descripcion = document.querySelector('.clima-card .descripcion');
    const tempMax = document.querySelector('.clima-card .max');
    const tempMin = document.querySelector('.clima-card .min');
    const iconoClima = document.querySelector('.clima-card .icono-clima');

    if (temperatura) {
        temperatura.textContent = `${Math.round(datosClima.temp || 0)}°C`;
    }

    if (descripcion) {
        descripcion.textContent = datosClima.estado || 'No disponible';
    }

    if (tempMax) {
        tempMax.textContent = `Máx: ${Math.round(datosClima.max || 0)}°C`;
    }

    if (tempMin) {
        tempMin.textContent = `Mín: ${Math.round(datosClima.min || 0)}°C`;
    }

    if (iconoClima) {
        const icono = obtenerIconoClima(datosClima.estado || '');
        iconoClima.textContent = icono;
    }

    console.log('✅ Clima actualizado en home');
}

function obtenerIconoClima(descripcion) {
    const desc = descripcion.toLowerCase();
    
    if (desc.includes('clear') || desc.includes('sunny')) {
        return '☀️';
    } else if (desc.includes('cloud')) {
        return '☁️';
    } else if (desc.includes('rain')) {
        return '🌧️';
    } else if (desc.includes('storm')) {
        return '⛈️';
    } else if (desc.includes('snow')) {
        return '❄️';
    } else {
        return '🌤️';
    }
}

function mostrarClimaFallback() {
    const climaPorDefecto = {
        temp: 20,
        max: 25,
        min: 15,
        estado: 'No disponible'
    };
  
    mostrarClimaEnHome(climaPorDefecto);
    console.log('📦 Mostrando clima por defecto');
}