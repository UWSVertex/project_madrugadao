/**
 * Rotates outgoing WhatsApp clicks across multiple sales numbers so leads are
 * distributed evenly between sales people. The icon/label never changes —
 * only the destination phone number does, picked round-robin on each click
 * and persisted in localStorage so the rotation keeps advancing across
 * page loads and visits.
 */
(function () {
    var numbers = window.WHATSAPP_NUMBERS || [];
    if (!numbers.length) {
        return;
    }

    var STORAGE_KEY = 'myrWhatsappRotationIndex';

    function nextNumber() {
        var index = 0;
        try {
            index = parseInt(localStorage.getItem(STORAGE_KEY), 10);
            if (isNaN(index) || index < 0) {
                index = 0;
            }
        } catch (e) {
            index = Math.floor(Math.random() * numbers.length);
        }

        var number = numbers[index % numbers.length];

        try {
            localStorage.setItem(STORAGE_KEY, String((index + 1) % numbers.length));
        } catch (e) {
            /* localStorage unavailable (private mode, etc.) — rotation just won't persist. */
        }

        return number;
    }

    document.querySelectorAll('.whatsapp-link').forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            var number = nextNumber();
            var text = link.getAttribute('data-wa-text') || '';
            var url = 'https://wa.me/' + number;
            if (text) {
                url += '?text=' + encodeURIComponent(text);
            }
            window.open(url, '_blank', 'noopener');
        });
    });
})();
