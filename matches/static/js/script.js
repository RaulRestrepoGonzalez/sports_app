// Manejar el menú de pantalla completa
const menuButton = document.getElementById('menuButton');
const menuOverlay = document.getElementById('menuOverlay');

if (menuButton && menuOverlay) {
    menuButton.addEventListener('click', () => {
        menuOverlay.classList.toggle('active');
    });
}

// Función para cerrar el modal
function closeModal() {
    const leagueModal = document.getElementById('leagueModal');
    if (leagueModal) {
        leagueModal.style.display = 'none';
    }
}

// Mostrar el modal cuando se hace clic en el enlace "Ligas"
document.addEventListener('DOMContentLoaded', () => {
    const leagueLink = document.querySelector('[data-toggle="modal"]');
    if (leagueLink) {
        leagueLink.addEventListener('click', (event) => {
            event.preventDefault(); // Evitar que el enlace redirija
            const leagueModal = document.getElementById('leagueModal');
            if (leagueModal) {
                leagueModal.style.display = 'block';
            }
        });
    }
});