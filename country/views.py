from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from analysis.models import Country

def country_view(request):
    countries = Country.objects.all()

    selected_country_id = request.GET.get('selected_country')
    selected_country = get_object_or_404(Country, id=selected_country_id) if selected_country_id else None

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Jeśli to jest żądanie AJAX, zwróć dane w formacie JSON
        data = {
            'id': selected_country.id if selected_country else None,
            'country': selected_country.country if selected_country else None,
            'capital': selected_country.capital if selected_country else None,
            'area': selected_country.area if selected_country else None,
            'population': selected_country.population if selected_country else None,
            'phone_code': selected_country.phone_code if selected_country else None,
            'continent': selected_country.continent if selected_country else None,
            'flag_path': selected_country.flag_path if selected_country else None,
        }
        return JsonResponse(data)

    return render(request, 'country_page.html', {
        'countries': countries,
        'selected_country': selected_country,
    })
