document.addEventListener("DOMContentLoaded", () => {
  const chatToggle = document.getElementById("chatToggle");
  const chatWindow = document.getElementById("chatWindow");
  const closeChat = document.getElementById("closeChat");
  const fileBtn = document.getElementById("fileBtn");   // <-- aquí
  const fileInput = document.getElementById("fileInput"); // <-- y aquí

  // Abrir/cerrar con el botón flotante
  chatToggle.addEventListener("click", () => {
    chatWindow.style.display = chatWindow.style.display === "flex" ? "none" : "flex";
  });

  // Cerrar con el circulito rojo
  closeChat.addEventListener("click", () => {
    chatWindow.style.display = "none";
  });

  // cuando haces click en el botón, abre el input oculto
  fileBtn.addEventListener("click", () => {
    fileInput.click();
  });
});

document.getElementById("enviarBtn").addEventListener("click", async () => {
    const texto = document.getElementById("textoInput").value.trim();
    const inputArchivos = document.getElementById('fileInput');


    // Arreglo con el payload final
    let payload = {
        pdf: [],
        imagen:[],
    };

    // Caso 1: hay texto
    if (texto) {
        payload.texto = texto;
    }
    // console.log(inputArchivos.files[0].name);

    if (inputArchivos.files.length > 0) {
    console.log('Archivos seleccionados:');
        for(let archivo of inputArchivos.files){
            // const archivo=inputArchivos.file[i];//<-- deberia iterar bien sobre los elementos
            console.log(archivo.name, archivo.type); // Muestra el nombre de cada archivo
            // Caso 2: hay archivo  
            if(archivo.type==="image/png"){
                const imagen_base64 =  await leerArchivoBase64(archivo);
                // console.log("Imagen en base64:", imagen_base64);
                payload.imagen.push(imagen_base64); // se añade al payload la imagen en base64

            }else if(archivo.type==="application/pdf"){
                const pdf_base64 = await leerArchivoBase64(archivo);
                // console.log("pdf en base64:", pdf_base64);
                payload.pdf.push(pdf_base64); // se añade al payload la imagen en base64
            }
        }
    }

    // Si no hay nada, no enviamos
    if (Object.keys(payload).length === 0) {
        alert("Escribe algo o sube un archivo");
        return;
    }

    // console.log(payload);

    // Enviar al backend
    const respuesta = await fetch("http://127.0.0.1:8000/chat/consulta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    const result = await respuesta.json();
    console.log(result.respuesta);

    // mostrar respuesta
    document.getElementById("chatBox").innerHTML += `
        <p><b>Tú:</b> ${payload.texto}</p>
        <p><b>Lechuguin:</b> ${result.respuesta}</p>
    `;
});

function leerArchivoBase64(archivo) { //comvertir archivo imagen o pdf a base64
    return new Promise((resolve, reject) => {
        const lector = new FileReader();
        lector.onloadend = () => {
          resolve(lector.result.split(",")[1]); // devuelve solo la parte base64
        };
        lector.onerror = reject;
        lector.readAsDataURL(archivo);
    });
}
