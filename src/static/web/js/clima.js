//script con 3 funciones
// const API_BASE = 'http://localhost:8000';
//obtener clima del dia

//formato guia de usuario en cache
// const usuarioCompleto = {
//           correo: vEmail,
//           nombre: body.nombre || 'Usuario',
//           ubicacion: body.ubicacion || {},
//           cultivos: body.cultivos || {}
//         };

//logica hacer fetch al backend con lat y lon del usuario al endpoint .get("/clima/hoy/{lat}/{lon}")
async function obtenerClimaDia(){
    try{
        //obtener lat y lon de cache
        const usuarioStr = localStorage.getItem('usuario'); //obtener usuario string
        if(!usuarioStr){
            console.log("No hay usuario en la cache");
            return null;
        }

        usuario = JSON.parse(usuarioStr);
        const lat = usuario.ubicacion?.latitud || usuario.ubicacion?.lat || -999; //-999 valor tipo tumba/bandera -> no hay lat y lon negativas
        const lon = usuario.ubicacion?.longitud || usuario.ubicacion?.lon || -999;

        if(lat==-999 && lon==-999){
            console.log("No se pudo obtener latitud y longitud");
            return null;
        }

        const url = `${API_BASE}/clima/hoy/${lat}/${lon}`;

        //hacer fetch a backend
        const respuesta = await fetch(url, {method: 'GET'});
        if(!respuesta.ok){ //si algo salió mal retornar null
            console.log(`Error ${respuesta.status}: ${respuesta.statusText}`);
            return null;
        }

        const clima = await respuesta.json();
        console.log(clima); //debug <-----

        return clima;
        //ver como incertar información clima en html
    }
    catch (error){
        console.log('Error obteniendo datos de clima', error);
    }
}

//obtener clima de la semana
//logica hacer fetch al backend con lat y lon del usuario al endpoint .get("/clima/semana/{lat}/{lon}")
async function obtenerClimaSemana(){
    try{
        //obtener lat y lon de cache
        const usuarioStr = localStorage.getItem('usuario'); //obtener usuario string
        if(!usuarioStr){
            console.log("No hay usuario en la cache");
            return null;
        }

        usuario = JSON.parse(usuarioStr);
        const lat = usuario.ubicacion?.latitud || usuario.ubicacion?.lat || -999; //-999 valor tipo tumba/bandera -> no hay lat y lon negativas
        const lon = usuario.ubicacion?.longitud || usuario.ubicacion?.lon || -999;

        if(lat==-999 && lon==-999){
            console.log("No se pudo obtener latitud y longitud");
            return null;
        }

        const url = `${API_BASE}/clima/semana/${lat}/${lon}`;

        //hacer fetch a backend
        const respuesta = await fetch(url, {method: 'GET'});
        if(!respuesta.ok){ //si algo salió mal retornar null
            console.log(`Error ${respuesta.status}: ${respuesta.statusText}`);
            return null;
        }

        const clima = await respuesta.json();
        console.log(clima); //debug <-----

        return clima;
        //ver como incertar información clima en html
    }
    catch (error){
        console.log('Error obteniendo datos de clima', error);
    }
}

//obtener clima hora a hora de 4 dias
//logica hacer fetch al backend con lat y lon del usuario al endpoint .get("/clima/hora/{lat}/{lon}")
async function obtenerClimaHora(){
    try{
        //obtener lat y lon de cache
        const usuarioStr = localStorage.getItem('usuario'); //obtener usuario string
        if(!usuarioStr){
            console.log("No hay usuario en la cache");
            return null;
        }

        usuario = JSON.parse(usuarioStr);
        const lat = usuario.ubicacion?.latitud || usuario.ubicacion?.lat || -999; //-999 valor tipo tumba/bandera -> no hay lat y lon negativas
        const lon = usuario.ubicacion?.longitud || usuario.ubicacion?.lon || -999;

        if(lat==-999 && lon==-999){
            console.log("No se pudo obtener latitud y longitud");
            return null;
        }

        const url = `${API_BASE}/clima/hora/${lat}/${lon}`;

        //hacer fetch a backend
        const respuesta = await fetch(url, {method: 'GET'});
        if(!respuesta.ok){ //si algo salió mal retornar null
            console.log(`Error ${respuesta.status}: ${respuesta.statusText}`);
            return null;
        }

        const clima = await respuesta.json();
        console.log(clima); //debug <-----

        return clima;
        //ver como incertar información clima en html
    }
    catch (error){
        console.log('Error obteniendo datos de clima', error);
    }
}
