// Fichier javascript qui permet l'animation de la page d'accueil.


document.addEventListener("DOMContentLoaded", function () {
    const options = {
        threshold: 0.1  // Une petite partie de l'élément (10%) doit être visible pour déclencher l'animation
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('appear');  // Ajoute la classe d'apparition
            } else {
                entry.target.classList.remove('appear');  // Retire la classe si on quitte la vue pour réactiver à nouveau
            }
        });
    }, options);

    const paragraphs = document.querySelectorAll('p');
    paragraphs.forEach(p => observer.observe(p));
});