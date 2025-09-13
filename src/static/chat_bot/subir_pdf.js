async function enviarPdf() {
    const input = document.getElementById("fileInputPdf");

    if (!input.files.length) {
        alert("Primero selecciona un PDF");
        return;
    }

    const archivo = input.files[0];
    const lector = new FileReader();

    lector.onloadend = async function() {
        // lector.result es un string tipo "data:application/pdf;base64,JVBERi0xLjcKJc..."
        const base64 = lector.result.split(",")[1]; // separar en la coma y quedarse con el base64 nada mas
        const data = { pdf: base64 }; // <----------------- cambiar a [base64] para implementar soporte para multiples pdf (en conjunto con el backend)
                                      //importante hacer el diccionario, sino el backend explota

        //mandar la info al backend
        const respuesta = await fetch("http://127.0.0.1:8000/chat/consulta", { 
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const result = await respuesta.json();

        // Mostrar respuesta en el chatBox
        document.getElementById("chatBox").innerHTML += `
            <p><b>Tú:</b> Pdf enviado (${archivo.name})</p>
            <p><b>Bot:</b> ${result.respuesta}</p>
        `;

        input.value = "";
    };  

    //sirbe para que no explote
    lector.readAsDataURL(archivo);

}