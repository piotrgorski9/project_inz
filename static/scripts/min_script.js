// Min wartośc dla wybranego roku
function calculateMinForSelectedYear() {
    var selectedYear = document.getElementById('selected-year').value;

    // Wywołaj żądanie AJAX do Django, aby obliczyć minimalną wartość dla wybranego roku
    fetch('/calculate_min_for_year/?selected_year=' + encodeURIComponent(selectedYear))
        .then(response => response.json())
        .then(data => {
            if ('min_emigration' in data && 'country_with_min_emigration' in data) {
                var minResult = document.getElementById('minResult');

                minResult.innerHTML = "Minimalna emigracja dla roku " + selectedYear + ": " + data.min_emigration +
                    " w kraju " + data.country_with_min_emigration;

                minResult.style.display = 'block';
            } else {
                alert('An error occurred: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error during AJAX request:', error);
        });
}