// Tiempo inicial del contador
let countdown = 3;
const countdownElement = document.getElementById('countdown');

// Inicia el temporizador
const timer = setInterval(() => {
    countdown--;
    countdownElement.textContent = countdown;

    if (countdown <= 0) {
        clearInterval(timer);
        window.location.href = 'index.html';
    }
}, 1000);

// También redirigir inmediatamente si se hace clic en cualquier lugar
document.addEventListener('click', () => {
    clearInterval(timer);
    window.location.href = 'index.html';
});
