from django.shortcuts import render

def startaction(request):
    return render(request, 'start.html')
