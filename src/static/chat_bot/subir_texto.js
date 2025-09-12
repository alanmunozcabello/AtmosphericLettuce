document.getElementById("chat-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const input = document.getElementById("chat-input");
    let mensaje = input.value.trim();

    if (!mensaje) {
        alert("El mensaje no puede estar vacío");
        return;
    }

    //ver si hay imágenes

    // armar diccionario
    const data = { "texto": mensaje };

    // enviar al backend
    const respuesta = await fetch("http://127.0.0.1:8000/chat/consulta", {//endpoint en el backend
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const result = await respuesta.json();

    // mostrar respuesta
    document.getElementById("chatBox").innerHTML += `
        <p><b>Tú:</b> ${mensaje}</p>
        <p><b>Bot:</b> ${result.respuesta}</p>
    `;

    input.value = "";
});