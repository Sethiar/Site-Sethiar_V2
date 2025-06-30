document.addEventListener('DOMContentLoaded', () => {
    const logoElement = document.getElementById('logo');
    const sprites = logoElement.querySelectorAll('.sprite');
    let currentSprite = 0;
    const spriteDurations = [4500, 4500, 4500, 4500, 4500, 4500, 4500, 4500];
    let animationTimeout;

    // Fonction masquant tous les sprites
    function resetSprites() {
        sprites.forEach((sprite) => {
            sprite.style.visibility = 'hidden';
            sprite.style.animation = 'none';
        });
    }

    // Fonction démarrant un sprite
    function startAnimation(spriteIndex) {
        const sprite = sprites[spriteIndex];
        // Affichage du sprite
        sprite.style.visibility = 'visible';
        sprite.style.animation = `animateLogo${spriteIndex + 1} ${spriteDurations[spriteIndex] / 1000}s steps(20, end) forwards`;
    }

    // Fonction pour arrêter un sprite
    function stopAnimation(spriteIndex) {
        const sprite = sprites[spriteIndex];
        // Masquage du sprite
        sprite.style.visibility = 'hidden';
        sprite.style.animation = 'none';
    }

    // Fonction pour changer de sprite
    function changeLogo() {
        // Arrête le sprite actuel
        stopAnimation(currentSprite);

        // Passer au script suivant
        currentSprite++;

        // Si dernière vignette n'est pas atteinte
        if (currentSprite < sprites.length) {
            // Démarrer sprite suivant
            startAnimation(currentSprite);
            // Planification du suivant
            animationTimeout = setTimeout(changeLogo, spriteDurations[currentSprite]);
        } else {
        // Affichage de la dernière vignette
        // Vérification du positionnement sur le dernier index
        currentSprite = sprites.length - 1;
        // Maintien de la dernière vignette visible
        startAnimation(currentSprite);
    }
}
    // Bouton "Rejouer"
    document.getElementById('btn-logo').addEventListener('click', () => {
        clearTimeout(animationTimeout);
        resetSprites();
        currentSprite = 0;
        startAnimation(currentSprite);
        animationTimeout = setTimeout(changeLogo, spriteDurations[currentSprite]);
    });

    // Initialisation
    resetSprites();
    startAnimation(currentSprite);
    animationTimeout = setTimeout(changeLogo, spriteDurations[currentSprite]);
});