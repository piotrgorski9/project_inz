// Funkcja do ukrywania wszystkich wyników
function hideAllResults() {
    // Ukryj wyniki średniej emigracji
    var averageResult = document.getElementById('averageResult');
    averageResult.style.display = 'none';

    // Ukryj wyniki minimalnej emigracji
    var minResult = document.getElementById('minResult');
    minResult.style.display = 'none';

    // Ukryj wyniki maksymalnej emigracji
    var maxEmigrationResult = document.getElementById('maxEmigrationResult');
    maxEmigrationResult.style.display = 'none';

    // Ukryj wyniki sumy emigrantów
    var sumResult = document.getElementById('sumResult');
    sumResult.style.display = 'none';

    // Ukryj wyniki procentu dla wybranego kraju i roku
    var countryYearPercentageResult = document.getElementById('country-year-percentage-result');
    countryYearPercentageResult.style.display = 'none';
}