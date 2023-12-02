// Obliczanie sredniej dla wybranego roku
function calculateAverageForSelectedYear() {
    var selectedYear = document.getElementById('selected-year').value;

    // Wywołaj żądanie AJAX do Django, aby obliczyć średnią dla wybranego roku
    fetch('/calculate_average_for_year/?selected_year=' + encodeURIComponent(selectedYear))
        .then(response => response.json())
        .then(data => {
            if ('average_emigration' in data) {
                var averageResult = document.getElementById('averageResult');
                averageResult.innerHTML = "Średnia emigracja dla roku " + selectedYear + ": " + data.average_emigration.toFixed(2);

                averageResult.style.display = 'block';
            } else {
                alert('An error occurred: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error during AJAX request:', error);
        });
}