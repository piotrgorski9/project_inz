// Obliczanie procentu dla wybranego kraju
function calculatePercentageForSelectedCountryAndYear() {
    var selectedCountry = document.getElementById('selected-country').value;
    var selectedYear = document.getElementById('selected-year').value;

    // Wywołaj żądanie AJAX do Django, aby obliczyć procent dla wybranego kraju i roku
    fetch('/calculate_percentage_for_country_and_year/?selected_country=' + encodeURIComponent(selectedCountry) + '&selected_year=' + encodeURIComponent(selectedYear))
        .then(response => response.json())
        .then(data => {
            if ('percentage' in data) {
                var countryYearPercentageResult = document.getElementById('country-year-percentage-result');
                countryYearPercentageResult.innerHTML = "Procent emigrantów dla kraju " + selectedCountry + " w roku " + selectedYear + ": " + data.percentage.toFixed(2) + "%";
                countryYearPercentageResult.style.display = 'block';
            } else {
                alert('An error occurred: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error during AJAX request:', error);
        });
}