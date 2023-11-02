from django.shortcuts import render
from django.db.models import Avg
from .models import Country, OtherModel



def analysisaction(request):
    countries = Country.objects.all()
    other_data = OtherModel.objects.all()

    # Oblicz średnią liczbę emigrantów z tabeli Country
    average_emigration = countries.aggregate(Avg('emigration'))['emigration__avg']

    return render(request, 'analysis.html', {
        'countries': countries,
        'other_data': other_data,
        'average_emigration': average_emigration,
    })
