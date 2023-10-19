# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def userpanelaction(request):
    # Przykładowe dane użytkownika
    user_data = {
        'first_name': request.user.first_name,
        # inne dane...
    }
    return render(request, 'user_panel.html', {'user': user_data})