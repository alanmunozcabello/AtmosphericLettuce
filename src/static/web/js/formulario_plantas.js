document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const btnDatosAdicionales = document.getElementById('btnDatosAdicionales');
    const camposAdicionales = document.getElementById('camposAdicionales');
    const otroRiegoRadio = document.getElementById('otro_riego_radio');
    const otroRiegoInput = document.getElementById('otro_riego');
    const tipoRiegoRadios = document.querySelectorAll('input[name="tipo_riego"]');
    const btnRegresar = document.getElementById('btnRegresar');
    const infoCultivo = document.getElementById('infoCultivo');
    const nombreCultivo = document.getElementById('nombreCultivo');
    const tituloGeneral = document.getElementById('tituloGeneral');
    let adicionalesVisible = false;

    // Obtener parámetros de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const cultivo = urlParams.get('cultivo');
    const correo = urlParams.get('correo');

    // Si viene de la página de cultivos, mostrar información específica
    if (cultivo && correo) {
        infoCultivo.style.display = 'block';
        tituloGeneral.style.display = 'none';
        nombreCultivo.textContent = cultivo;
        
        // Configurar botón regresar
        btnRegresar.addEventListener('click', function() {
            window.location.href = `home.html?correo=${encodeURIComponent(correo)}`;
        });
    } else {
        // Si no viene de cultivos, ocultar botón regresar
        btnRegresar.style.display = 'none';
    }

    // Función para mostrar/ocultar campos adicionales
    btnDatosAdicionales.addEventListener('click', function() {
        if (adicionalesVisible) {
            camposAdicionales.style.display = 'none';
            btnDatosAdicionales.textContent = 'Datos adicionales';
            adicionalesVisible = false;
        } else {
            camposAdicionales.style.display = 'block';
            btnDatosAdicionales.textContent = 'Ocultar datos adicionales';
            adicionalesVisible = true;
        }
    });

    // Función para mostrar/ocultar el campo "Otro" tipo de riego
    tipoRiegoRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (otroRiegoRadio.checked) {
                otroRiegoInput.style.display = 'block';
                otroRiegoInput.required = true;
            } else {
                otroRiegoInput.style.display = 'none';
                otroRiegoInput.required = false;
                otroRiegoInput.value = '';
            }
        });
    });

    // Manejar el envío del formulario
    const formulario = document.getElementById('formulario-plantas');
    formulario.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Recopilar todos los datos del formulario
        const formData = new FormData(formulario);
        const data = {};
        
        // Convertir FormData a objeto
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Agregar información del cultivo si está disponible
        if (cultivo) {
            data.nombre_cultivo = cultivo;
        }
        if (correo) {
            data.correo_usuario = correo;
        }
        
        // Convertir campos numéricos a números
        const camposNumericos = [
            'frecuencia', 'humedad_suelo', 'profundidad_radical', 
            'densidad_plantacion', 'eficiencia', 'caudal', 'ph_agua'
        ];
        
        camposNumericos.forEach(campo => {
            if (data[campo] && data[campo] !== '') {
                data[campo] = parseFloat(data[campo]);
            }
        });
        
        console.log('Datos del formulario:', data);
        
        if (cultivo) {
            alert(`Configuración guardada para el cultivo: ${cultivo}. Revisa la consola para ver los datos.`);
        } else {
            alert('Formulario preparado para envío al backend. Revisa la consola para ver los datos.');
        }
        
        // Aquí es donde enviarías los datos al backend
        // fetch('/api/plantas', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify(data)
        // });
    });
});