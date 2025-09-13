async function enviarImagen() {
    const input = document.getElementById("fileInput");

    if (!input.files.length) {
        alert("Primero selecciona una imagen");
        return;
    }

    const archivo = input.files[0];
    const lector = new FileReader();

    lector.onloadend = async () => {
        const base64 = lector.result.split(",")[1]; // nos quedamos unicamente con lo de despues de la coma (el base64)
        const data = { "imagen": base64 }; //importante hacer el diccionario, sino el backend explota

        console.log(data);

        // enviar al backend
        const respuesta = await fetch("http://127.0.0.1:8000/chat/consulta", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await respuesta.json();

        // mostrar respuesta
        document.getElementById("chatBox").innerHTML += `
            <p><b>Tú:</b> Imagen enviada (${archivo.name})</p>
            <p><b>Bot:</b> ${result.respuesta}</p>
        `;

        input.value = "";
    };

    // ¡IMPORTANTE! Esto inicia la lectura y dispara onloadend
    lector.readAsDataURL(archivo);
}