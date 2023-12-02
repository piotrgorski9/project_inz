function calculateSum() {
    var selectedYear = document.getElementById('selected-year').value;

    // Ukryj wyniki sumy emigrantów przed wysłaniem zapytania AJAX
    var sumResult = document.getElementById('sumResult');

    // Wywołaj funkcję na backendzie i obsłuż odpowiedź
    $.get('/calculate_sum_for_year/', { selected_year: selectedYear }, function (data) {
        if ('total_emigration_for_year' in data) {
            $('#sumResult').text('Suma emigrantów w roku ' + selectedYear + ': ' + data.total_emigration_for_year);
            // Pokaż wyniki sumy emigrantów po otrzymaniu odpowiedzi
            sumResult.style.display = 'block';
        } else {
            $('#sumResult').text('Błąd: ' + data.error);
        }
    });
}