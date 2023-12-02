from django.shortcuts import render
from analysis.models import Country, Emigration

def demoaction(request):
    # Pobierz tylko pierwszy kraj (lub dostosuj zapytanie do swoich potrzeb)
    country = Country.objects.first()
    
    emigrations = Emigration.objects.filter(country=country)
    
    # Pobierz unikalne lata z danych o emigracji dla wybranego kraju
    unique_years = emigrations.values('year').distinct().order_by('-year')[:1]
    selected_country = Country.objects.first()

    return render(request, 'demo_page.html', {
        'countries': [selected_country],  # Przekazujesz listę z jednym krajem
        'emigrations': emigrations,
        'unique_years': unique_years,
    })
