from django.shortcuts import render
import mysql.connector as sql
import bcrypt

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

        hashed_password = hash_password(pwd)

        try:
            with sql.connect(host="localhost", user="root", passwd="bazahaslo", database='website') as m:
                cursor = m.cursor()
                c = "INSERT INTO users (email, password, First_Name, Last_Name, Sex) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(c, (em, hashed_password, first_name, last_name, sex))
                m.commit()

                # Przekazanie komunikatu o sukcesie do szablonu
                return render(request, 'signup_page.html', {'success_message': 'Registration successful!'})

        except sql.Error as e:
            print(f"Błąd połączenia z bazą danych: {e}")
            # Przekazanie komunikatu o błędzie do szablonu
            return render(request, 'signup_page.html', {'error_message': 'Wystąpił błąd podczas rejestracji. Spróbuj ponownie później.'})

    return render(request, 'signup_page.html')

# Funkcja do haszowania hasła
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
