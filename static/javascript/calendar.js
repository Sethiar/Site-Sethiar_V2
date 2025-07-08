document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'fr',
        events: rdvData,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        selectable: true,
        select: function(info) {
            var selectedDate = info.startStr;
            alert('Date sélectionnée : ' + formatDateToFrench(selectedDate));
            openModalForDate(selectedDate);
        },
        eventTimeFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },
        eventClick: function(info) {
            var eventTitle = info.event.title;
            var eventDate = moment(info.event.start).format('DD/MM/YYYY');
            var eventTime = moment(info.event.start).format('HH:mm');
            var requestContent = info.event.extendedProps.content;
            
            if (info.event.url) {
                window.open(info.event.url, '_blank');
            } else {
                alert('Aucun lien disponible pour cet événement.');
            }
            info.jsEvent.preventDefault();

            alert('Rendez-vous avec ' + eventTitle + ' le ' + formatDateToFrench(eventDate) + ' à ' + eventTime + ' pour le motif suivant : ' + requestContent);

            openModalForEvent(info.event);
        }
    });

    calendar.render();

    // Fonction pour formater la date en format français.
    function formatDateToFrench(dateStr) {
        var options = { year: 'numeric', month: 'long', day: 'numeric' };
        var date = new Date(dateStr);
        return date.toLocaleDateString('fr-FR', options);
    }

    // Fonction pour ouvrir une modale lors de la sélection d'une date.
    function openModalForDate(date) {
        $('#modal-content').html(`
            <p><strong>Date sélectionnée :</strong> ${formatDateToFrench(date)}</p>
            <p>Vous pouvez maintenant ajouter un rendez-vous pour cette date.</p>
        `);
        $('#yourModalId').modal('show');
    }

    // Fonction pour ouvrir une modale lors du clic sur un événement.
    function openModalForEvent(event) {
        $('#modal-content').html(`
            <p><strong>Titre :</strong> ${event.title}</p>
            <p><strong>Date :</strong> ${moment(event.start).format('DD/MM/YYYY')}</p>
            <p><strong>Heure :</strong> ${moment(event.start).format('HH:mm')}</p>
            <p><strong>Contenu :</strong> ${event.extendedProps.content}</p>
        `);
        $('#yourModalId').modal('show');
    }
});