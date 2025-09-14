document.getElementById("enviarBtn").addEventListener("click", async () => {
    console.log("hola")
    const texto = document.getElementById("textoInput").value.trim();
    const archivo = document.getElementById("fileInput").files[0];

    // console.log(archivo);

    // Arreglo con el payload final
    let payload = {};

    // Caso 1: hay texto
    if (texto) {
        payload.texto = texto;
    }

    // Caso 2: hay archivo
    if (archivo) {
        if (archivo.type.startsWith("image/")) {
            const imagen_base64 =  await leerArchivoBase64(archivo);
            // console.log("Imagen en base64:", imagen_base64);

            payload.imagen = imagen_base64; // se añade al payload la imagen en base64

      } else if (archivo.type === "application/pdf") {
            const pdf_base64 = await leerArchivoBase64(archivo);
            // console.log("pdf en base64:", pdf_base64);

            payload.pdf = pdf_base64; // se añade al payload la imagen en base64

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
        <p><b>Tú:</b> Enviado: (${payload.texto})</p>
        <p><b>Bot:</b> ${result.respuesta}</p>
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
