# views.py

import matplotlib
matplotlib.use('agg')  # Ustaw backend na 'agg' przed imporotem Matplotlib

from django.shortcuts import render
from django.db.models import Avg, Sum, Max, Min
from django.http import JsonResponse
from .models import Country, Emigration
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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
    

# Tworzenie wykresów
def generate_pie_chart(request, selected_year):
    # Tutaj pobierasz dane z bazy danych lub skąd chcesz
    emigration_data = get_emigration_data_for_year(selected_year)

    if emigration_data is None:
        return JsonResponse({'error': 'Brak danych o emigracji dla wybranego roku.'}, status=400)

    # Pobierz nazwy krajów z tabeli Country
    country_names = Country.objects.values_list('country', flat=True)

    countries = [entry['country'] for entry in emigration_data]
    emigrants = [entry['number_of_emigrants'] for entry in emigration_data]

    # Tworzenie wykresu kołowego
    plt.figure(figsize=(8, 8))

    # Zamień krotkę na listę
    set3_colors = list(plt.cm.Set3.colors)

    # Użyj większej liczby kolorów z mapy Set3 i dodaj własne kolory
    colors = set3_colors + ['coral', 'khaki', 'lightgreen', 'lightblue', 'orchid', 'lightcoral', 'palegoldenrod', 'palegreen', 'skyblue', 'thistle']

    plt.pie(emigrants, labels=country_names, autopct='%1.1f%%', startangle=100, colors=colors)
    pie_chart = plt.pie(emigrants, labels=country_names, autopct='%1.1f%%', startangle=100, colors=colors)

    plt.title(f'Emigrants distribution for year {selected_year}')
    
    # Przygotowanie etykiet dla legendy
    legend_labels = [f"{country_names[i]}: {emigrants[i]}" for i in range(len(country_names))]

    # Dodanie legendy
    plt.legend(pie_chart[0], legend_labels, title='Countries', loc='center left', bbox_to_anchor=(-0.4, 0.5), prop={'size': 7})

    # Zapisz wykres do pamięci
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight', pad_inches=0)

    image_stream.seek(0)

    # Zamień obraz na base64
    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

    # Zwróć dane jako JsonResponse
    return JsonResponse({'image_base64': image_base64})

def get_emigration_data_for_year(selected_year):
    try:
        emigration_data = (
            Emigration.objects
            .filter(year=selected_year)
            .values('country', 'number_of_emigrants')  # Zmiana klucza na 'country'
        )
        return emigration_data
    except Exception as e:
        raise ValueError(f'Błąd pobierania danych o emigracji: {e}')
    

# WYKRES DLA EMIGRANTÓW W WYBRANYM KRAJU

def generate_emigration_chart(request, selected_country):
    try:
        start_year = int(request.GET.get('start_year', 2005))
        end_year = int(request.GET.get('end_year', 2022))

        # Pobierz dane o emigracji dla wybranego kraju i zakresu lat
        emigration_data = (
            Emigration.objects
            .filter(country__country=selected_country, year__gte=start_year, year__lte=end_year)
            .order_by('year')
        )

        # Przygotuj dane do wykresu
        years = [entry.year for entry in emigration_data]
        emigrants = [entry.number_of_emigrants for entry in emigration_data]

        # Stwórz wykres liniowy
        plt.figure(figsize=(10, 6))
        plt.plot(years, emigrants, marker='o', linestyle='-', color='blue')
        plt.title(f'Emigration trend for {selected_country}')
        plt.xlabel('Year')
        plt.ylabel('Number of Emigrants')
        plt.xticks(np.arange(min(years), max(years) + 1, 1))  # Ustaw oś X co roku
        plt.grid(True)

        # Zapisz wykres do pamięci
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)

        # Zamień obraz na base64
        image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

        # Zwróć dane jako JsonResponse
        return JsonResponse({'image_base64': image_base64, 'start_year': start_year, 'end_year': end_year})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)