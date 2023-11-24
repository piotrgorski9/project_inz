from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from .models import UserProfile

def signaction(request):
    if request.method == "POST":
        em = request.POST.get("email")
        pwd = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        sex = request.POST.get("sex")

        if not em or not pwd or not first_name or not last_name or not sex:
            # Komunikat o błędzie, jeśli nie wszystkie pola są wypełnione
            return render(request, 'signup_page.html', {'error_message': 'Wszystkie pola formularza są wymagane.'})

        try:
            # Użyj make_password do haszowania hasła przed zapisaniem
            hashed_pwd = make_password(pwd)
            
            # Utworzenie obiektu UserProfile
            user_profile = UserProfile(
                email=em,
                password=hashed_pwd,
                first_name=first_name,
                last_name=last_name,
                sex=sex
            )
            # Zapisanie obiektu w bazie danych
            user_profile.save()

            # Przekazanie komunikatu o sukcesie do szablonu
            return render(request, 'signup_page.html', {'success_message': 'Registration successful!'})

        except Exception as e:
            print(f"Błąd podczas rejestracji: {e}")
            # Przekazanie komunikatu o błędzie do szablonu
            return render(request, 'signup_page.html', {'error_message': 'Wystąpił błąd podczas rejestracji. Spróbuj ponownie później.'})

    return render(request, 'signup_page.html')
