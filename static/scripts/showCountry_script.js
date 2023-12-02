$(document).ready(function () {
    // Ukryj kontener po załadowaniu strony
    $('#country-info').hide();
    // Obsługa formularza
    $('form').on('submit', function (e) {
        e.preventDefault();
        // Pobierz wybrany kraj
        var selectedCountryId = $('#country-select').val();
        // Wyślij żądanie AJAX, aby pobrać informacje o wybranym kraju
        $.ajax({
            type: 'GET',
            url: window.location.href,
            data: { selected_country: selectedCountryId },
            success: function (data) {
                // Zaktualizuj sekcję z informacjami o kraju bez przeładowywania strony
                $('#country-info').html(
                    data.id ?
                        `<h3>${data.country}</h3>
                        ${data.flag_path ? `<img id="flag-image" src="${data.flag_path}" alt="Flaga ${data.country}">` : ''}
                        <p><strong>Kontynent:</strong> ${data.continent}</p>
                        <p><strong>Stolica:</strong> ${data.capital}</p>
                        <p><strong>Powierzchnia:</strong> ${data.area} km²</p>
                        <p><strong>Populacja:</strong> ${data.population}</p>
                        <p><strong>Kod telefoniczny:</strong> +${data.phone_code}</p>`
                        : ''
                );
                // Pokaż kontener po uzyskaniu danych o kraju
                $('#country-info').show();
            },

            error: function () {
                console.log('Wystąpił błąd przy pobieraniu danych o kraju.');
            }
        });
    });
});