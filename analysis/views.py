# views.py

from django.shortcuts import render
from django.db.models import Avg, Sum, Max, Min
from django.http import JsonResponse
from .models import Country, Emigration
import numpy as np

def analysisaction(request):
    countries = Country.objects.all()
    emigrations = Emigration.objects.all()

    # Pobierz unikalne lata z danych o emigracji
    unique_years = Emigration.objects.values('year').distinct()

    return render(request, 'analysis.html', {
        'countries': countries,
        'emigrations': emigrations,
        'unique_years': unique_years,
    })

def calculate_average_for_selected_year(request):
    selected_year = request.GET.get('selected_year', None)

    if not selected_year:
        return JsonResponse({'error': 'Brak wybranego roku.'}, status=400)

    # Pobierz średnią emigracji dla danego roku
    average_emigration = Emigration.objects.filter(year=selected_year).aggregate(Avg('number_of_emigrants'))['number_of_emigrants__avg']

    return JsonResponse({'average_emigration': average_emigration})

def calculate_percentage_for_selected_country_and_year(request):
    selected_country = request.GET.get('selected_country', None)
    selected_year = request.GET.get('selected_year', None)

    if not selected_country or not selected_year:
        return JsonResponse({'error': 'Brak wybranego kraju lub roku.'}, status=400)

    country = Country.objects.filter(country=selected_country).first()

    if not country:
        return JsonResponse({'error': 'Kraj nie istnieje w bazie danych.'}, status=400)

    try:
        emigration_for_country_and_year = Emigration.objects.get(country=country, year=selected_year)
    except Emigration.DoesNotExist:
        return JsonResponse({'error': 'Brak danych dla wybranego kraju i roku.'}, status=400)

    total_emigration_for_year = Emigration.objects.filter(year=selected_year).aggregate(Sum('number_of_emigrants'))['number_of_emigrants__sum']
    
    if not total_emigration_for_year:
        return JsonResponse({'error': 'Brak danych o ogólnej liczbie emigrantów dla wybranego roku.'}, status=400)

    percentage = (emigration_for_country_and_year.number_of_emigrants / total_emigration_for_year) * 100

    return JsonResponse({'percentage': percentage})

def calculate_max_emigration_for_year(request):
    selected_year = request.GET.get('selected_year', None)

    if not selected_year:
        return JsonResponse({'error': 'Brak wybranego roku.'}, status=400)

    max_emigration_query = Emigration.objects.filter(year=selected_year).aggregate(Max('number_of_emigrants'))
    max_emigration = max_emigration_query['number_of_emigrants__max']
    
    max_country_query = Emigration.objects.filter(year=selected_year, number_of_emigrants=max_emigration).first()
    max_country = max_country_query.country.country if max_country_query else None

    return JsonResponse({'max_emigration': max_emigration, 'max_country': max_country})

def calculate_min_for_year(request):
    selected_year = request.GET.get('selected_year')

    try:
        min_emigration_data = Emigration.objects.filter(year=selected_year).aggregate(Min('number_of_emigrants'))
        min_emigration = min_emigration_data['number_of_emigrants__min']
        country_with_min_emigration = Emigration.objects.filter(year=selected_year, number_of_emigrants=min_emigration).first().country.country
    except Exception as e:
        return JsonResponse({'error': str(e)})

    return JsonResponse({'min_emigration': min_emigration, 'country_with_min_emigration': country_with_min_emigration})

# Odchylenie standardowe

def calculate_standard_deviation_for_year(request):
    if request.method == 'GET':
        selected_year = request.GET.get('selected_year')

        # Pobierz dane o emigracjach dla danego roku
        emigrations = Emigration.objects.filter(year=selected_year).values_list('number_of_emigrants', flat=True)

        if not emigrations:
            return JsonResponse({'error': 'Brak danych o emigracjach dla wybranego roku.'}, status=400)

        # Oblicz odchylenie standardowe za pomocą NumPy
        try:
            standard_deviation = np.std(emigrations)
            return JsonResponse({'standard_deviation': standard_deviation})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Nieprawidłowe żądanie'}, status=400)

def calculate_standard_deviation(data):
    try:
        standard_deviation = np.std(data)
        return standard_deviation
    except Exception as e:
        raise ValueError(f'Błąd obliczania odchylenia standardowego: {e}')