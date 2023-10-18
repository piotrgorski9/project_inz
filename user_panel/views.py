from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def userpanelaction(request):
    return render(request, 'user_panel.html')
