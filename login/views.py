from django.shortcuts import render
import mysql.connector as sql
import bcrypt

def loginaction(request):
    cursor = None

    try:
        if request.method == "POST":
            em = request.POST.get("email")
            pwd = request.POST.get("password")

            with sql.connect(host="localhost", user="root", passwd="bazahaslo", database='website') as m:
                cursor = m.cursor()
                c = "select password from users where email=%s"
                cursor.execute(c, (em,))
                hashed_password = cursor.fetchone()

                if hashed_password and bcrypt.checkpw(pwd.encode('utf-8'), hashed_password[0].encode('utf-8')):
                    # Pobierz rzeczywiste dane użytkownika z bazy danych
                    cursor.execute("SELECT first_name FROM users WHERE email = %s", (em,))
                    user_info = cursor.fetchone()

                    # Przekazujesz rzeczywiste dane użytkownika do szablonu
                    return render(request, 'user_panel.html', {'user_info': {'first_name': user_info[0]}})
                else:
                    error_message = 'Invalid email or password.'
                    return render(request, 'login_page.html', {'error_message': error_message, 'email': em})

        return render(request, 'login_page.html')

    except sql.Error as e:
        print(f"Błąd połączenia z bazą danych: {e}")
        return render(request, 'error.html')
    finally:
        if cursor:
            cursor.close()