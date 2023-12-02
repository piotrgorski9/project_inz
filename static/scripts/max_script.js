// Max wartośc dla wybranego roku
function calculateMaxEmigrationForYear() {
    var selectedYear = document.getElementById('selected-year').value;

    // Wywołaj żądanie AJAX do Django, aby obliczyć maksymalną emigrację dla wybranego roku
    fetch('/calculate_max_emigration_for_year/?selected_year=' + encodeURIComponent(selectedYear))
        .then(response => response.json())
        .then(data => {
            if ('max_emigration' in data && 'max_country' in data) {
                var maxEmigrationResult = document.getElementById('maxEmigrationResult');
                maxEmigrationResult.innerHTML = "Maksymalna emigracja dla roku " + selectedYear + ": " + data.max_emigration +
                    " w kraju " + data.max_country;

                maxEmigrationResult.style.display = 'block';
            } else {
                alert('An error occurred: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error during AJAX request:', error);
        });
}