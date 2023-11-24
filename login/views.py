from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from signup.models import UserProfile

def loginaction(request):
    em = None

    try:
        if request.method == "POST":
            em = request.POST.get("email")
            pwd = request.POST.get("password")

            # Pobierz obiekt użytkownika z bazy danych
            user_profile = UserProfile.objects.get(email=em)
            stored_password = user_profile.password

            if stored_password is not None:
                # Sprawdź poprawność hasła za pomocą check_password
                if check_password(pwd, stored_password):
                    # Sprawdź typ użytkownika
                    user_type = user_profile.user_type

                    # W zależności od typu użytkownika przekieruj na odpowiednią stronę
                    if user_type == 'admin':

                        user_info = {
                            'first_name': user_profile.first_name,
                            'last_name': user_profile.last_name,
                            # Dodaj inne pola profilu, które chcesz przekazać do szablonu
                        }

                        return render(request, 'admin_page.html', {'user_info': user_info})
                    elif user_type == 'normal':
                        # Pobierz rzeczywiste dane użytkownika z bazy danych
                        user_info = {
                            'first_name': user_profile.first_name,
                            'last_name': user_profile.last_name,
                            # Dodaj inne pola profilu, które chcesz przekazać do szablonu
                        }

                        # Przekazujesz rzeczywiste dane użytkownika do szablonu
                        return render(request, 'user_panel.html', {'user_info': user_info})
                    else:
                        return render(request, 'error.html')  # Obsługa innych typów użytkowników

                else:
                    error_message = 'Nieprawidłowy adres email lub hasło.'
                    return render(request, 'login_page.html', {'error_message': error_message, 'email': em})
            else:
                error_message = 'Brak hasła dla użytkownika.'
                return render(request, 'login_page.html', {'error_message': error_message, 'email': em})
        else:
            # Obsługa przypadku, gdy żądanie nie jest typu POST
            return render(request, 'login_page.html')

    except UserProfile.DoesNotExist:
        error_message = 'Nieprawidłowy adres email lub hasło.'
        return render(request, 'login_page.html', {'error_message': error_message, 'email': em})
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return render(request, 'error.html')
