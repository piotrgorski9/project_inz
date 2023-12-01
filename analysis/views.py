# views.py

import matplotlib
matplotlib.use('agg')  # Ustaw backend na 'agg' przed imporotem Matplotlib

from django.shortcuts import render
from django.db.models import Avg, Sum, Max, Min, StdDev
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
    

# Dodaj nową funkcję do obliczania odchylenia standardowego dla danego kraju
def calculate_standard_deviation_for_country(request):
    if request.method == 'GET':
        selected_country = request.GET.get('selected_country')
        start_year = request.GET.get('start_year')
        end_year = request.GET.get('end_year')

        # Sprawdź, czy początkowy rok nie jest większy niż końcowy rok
        if start_year and end_year and start_year == end_year:
            return JsonResponse({'error': 'Rok początkowy nie może być taki sam jak rok końcowy.'}, status=400)


        # Sprawdź, czy początkowy rok jest mniejszy od końcowego roku
        if start_year and end_year and int(start_year) > int(end_year):
            return JsonResponse({'error': 'Rok początkowy musi być mniejszy niż rok końcowy.'}, status=400)


        try:
            emigration_data = Emigration.objects.filter(country__country=selected_country, year__range=(start_year, end_year))
            standard_deviation = emigration_data.aggregate(std_dev=StdDev('number_of_emigrants'))['std_dev']

            return JsonResponse({'standard_deviation': standard_deviation})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})


def calculate_sum_for_year(request):
    selected_year = request.GET.get('selected_year')

    try:
        # Pobierz sumę emigracji dla danego roku
        total_emigration_for_year = Emigration.objects.filter(year=selected_year).aggregate(Sum('number_of_emigrants'))['number_of_emigrants__sum']

        if total_emigration_for_year is not None:
            return JsonResponse({'total_emigration_for_year': total_emigration_for_year})
        else:
            return JsonResponse({'error': 'Brak danych o emigracji dla wybranego roku.'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
# wykres kołowy
def generate_pie_chart(request, selected_year):
    emigration_data = get_emigration_data_for_year(selected_year)

    if emigration_data is None:
        return JsonResponse({'error': 'Brak danych o emigracji dla wybranego roku.'}, status=400)

    country_names = Country.objects.values_list('country', flat=True)

    # Użyj tego
    countries = [Country.objects.get(id=entry['country']).country for entry in emigration_data]
    emigrants = [entry['number_of_emigrants'] for entry in emigration_data]

    # Próg udziału procentowego, poniżej którego kraje są grupowane
    threshold_percentage = 2

    # Znajdź indeksy krajów, których udział jest mniejszy niż próg
    below_threshold_indices = [i for i, percentage in enumerate(emigrants) if percentage / sum(emigrants) * 100 < threshold_percentage]

    # Grupuj kraje poniżej progu jako "Inne"
    grouped_emigrants = [emigrants[i] for i in range(len(emigrants)) if i not in below_threshold_indices]
    grouped_countries = [countries[i] for i in range(len(countries)) if i not in below_threshold_indices]
    grouped_emigrants.append(sum([emigrants[i] for i in below_threshold_indices]))
    grouped_countries.append('Inne')

    # Tworzenie wykresu kołowego
    plt.figure(figsize=(7, 7), dpi=100)

    set3_colors = list(plt.cm.Set3.colors)
    colors = set3_colors + ['coral', 'khaki', 'lightgreen', 'lightblue', 'orchid', 'lightcoral', 'palegoldenrod', 'palegreen', 'skyblue', 'thistle']

    plt.pie(grouped_emigrants, labels=grouped_countries, autopct='%1.1f%%', startangle=100, colors=colors)
    plt.title(f'Rozkład emigrantów dla roku {selected_year}')


    # Przygotowanie etykiet dla legendy
    legend_labels = [f"{grouped_countries[i]}: {grouped_emigrants[i]}" for i in range(len(grouped_countries))]

    # Dodanie legendy
    plt.legend(legend_labels, title='Kraje', loc='center left', bbox_to_anchor=(-0.4, 0.5), prop={'size': 7})


    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', dpi=90, bbox_inches='tight', pad_inches=0)
    image_stream.seek(0)

    image_base64 = base64.b64encode(image_stream.read()).decode('utf-8')

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
        plt.plot(years, emigrants, marker='o', linestyle='-', color='#006400')
        plt.title(f'Trend emigracji dla kraju {selected_country}')
        plt.xlabel('Rok')
        plt.ylabel('Liczba emigrantów')
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
    

# Funkcja do generowania wykresu dla dwóch wybranych krajów
def generate_emigration_chart_for_two_countries(request):
    try:
        start_year = int(request.GET.get('start_year', 2005))
        end_year = int(request.GET.get('end_year', 2022))
        country1 = request.GET.get('country1')
        country2 = request.GET.get('country2')

        # Pobierz dane o emigracji dla dwóch wybranych krajów i zakresu lat
        emigration_data_country1 = (
            Emigration.objects
            .filter(country__country=country1, year__gte=start_year, year__lte=end_year)
            .order_by('year')
        )

        emigration_data_country2 = (
            Emigration.objects
            .filter(country__country=country2, year__gte=start_year, year__lte=end_year)
            .order_by('year')
        )

        # Przygotuj dane do wykresu
        years_country1 = [entry.year for entry in emigration_data_country1]
        emigrants_country1 = [entry.number_of_emigrants for entry in emigration_data_country1]

        years_country2 = [entry.year for entry in emigration_data_country2]
        emigrants_country2 = [entry.number_of_emigrants for entry in emigration_data_country2]

        # Stwórz wykres liniowy
        plt.figure(figsize=(10, 6))
        plt.plot(years_country1, emigrants_country1, marker='o', linestyle='-', color='#006400', label=country1)
        plt.plot(years_country2, emigrants_country2, marker='o', linestyle='-', color='#FF4500', label=country2)
        plt.title(f'Trend emigracji dla krajów {country1} i {country2}')
        plt.xlabel('Rok')
        plt.ylabel('Liczba emigrantów')
        plt.xticks(np.arange(min(min(years_country1), min(years_country2)), max(max(years_country1), max(years_country2)) + 1, 1))
        plt.legend()
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