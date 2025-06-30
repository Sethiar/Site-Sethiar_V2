// Fichier javascript concernant le carrousel de présentation de l'accueil.

const swiper = new Swiper('.swiper-container', {
    loop: true,
    slidesPerView: 3,
    spaceBetween: 50,
    centeredSlides: true,
    autoplay: {
        delay: 3000,
        disableOnInteraction: true,
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        320: {
            slidesPerView: 1,
        },
        640: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 1,
        },
        1024: {
            slidesPerView: 3,
        },
    },
});

/// Sélection des slides
const slides = document.querySelectorAll('.swiper-slide');

// Cibles dans la modale
const modal = document.getElementById('slide-modal');
const modalImage = document.getElementById('modal-image');
const modalTitle = document.getElementById('modal-title');
const modalDescription = document.getElementById('modal-description');
const closeModalBtn = document.querySelector('.close-btn');

// Gestion des clics sur les slides
slides.forEach((slide) => {
    slide.addEventListener('click', () => {
        // Récupérer l'image
        const imgSrc = slide.querySelector('img')?.src || '';
        const title = slide.querySelector('h3')?.innerText || 'Titre indisponible';

        // Concaténer tous les paragraphes dans la description
        const description = Array.from(slide.querySelectorAll('.product-p'))
            .map((pBlock) => pBlock.innerText.trim()) // Récupère le texte de chaque bloc
            .join('\n\n'); // Ajoute une séparation entre les blocs

        // Mise à jour de la modale
        modalImage.src = imgSrc;
        modalTitle.innerText = title;
        modalDescription.innerText = description || 'Aucune description disponible';

        // Afficher la modale
        modal.style.display = 'flex';
    });
});

// Gestion de la fermeture de la modale
closeModalBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Fermeture de la modale en cliquant en dehors
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});