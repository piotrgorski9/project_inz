from django.shortcuts import redirect

from django.contrib.auth import logout

def logoutaction(request):
    # Przeprowadź proces wylogowania, np. używając funkcji logout() z modułu auth
    logout(request)
    
    # Teraz możesz przekierować użytkownika na inną stronę lub zrobić cokolwiek innego
    return redirect('home')

