"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from signup.views import signaction
from login.views import loginaction
from start.views import startaction
from logout.views import logoutaction
from user_panel.views import userpanelaction
from analysis.views import analysisaction, calculate_average_for_selected_year, calculate_percentage_for_selected_country_and_year, calculate_max_emigration_for_year, calculate_min_for_year, calculate_standard_deviation_for_year, generate_pie_chart, generate_emigration_chart, calculate_standard_deviation_for_country, generate_emigration_chart_for_two_countries, calculate_sum_for_year
from admin_page.views import admin_page
from country.views import country_view
from demo.views import demoaction
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='start_page.html'), name='home'),
    path('admin/', admin.site.urls),
    path('signup/',signaction),
    path('login/',loginaction),
    path('start/',startaction),
    path('logout/', logoutaction),
    path('user_panel/', userpanelaction, name='user_panel'),
    path('analysis/', analysisaction, name='analysisaction'),
    path('calculate_average_for_year/', calculate_average_for_selected_year, name='calculate_average_for_year'),
    path('calculate_percentage_for_country_and_year/', calculate_percentage_for_selected_country_and_year, name='calculate_percentage_for_country_and_year'),
    path('calculate_max_emigration_for_year/', calculate_max_emigration_for_year, name='calculate_max_emigration_for_year'),
    path('calculate_min_for_year/', calculate_min_for_year, name='calculate_min_for_year'),
    path('calculate_standard_deviation_for_year/', calculate_standard_deviation_for_year, name='calculate_standard_deviation_for_year'),
    path('generate_pie_chart/<str:selected_year>/', generate_pie_chart, name='generate_pie_chart'),
    path('generate_emigration_chart/<str:selected_country>/', generate_emigration_chart, name='generate_emigration_chart'),
    path('calculate_standard_deviation_for_country/', calculate_standard_deviation_for_country, name='calculate_standard_deviation_for_country'),
    path('generate_emigration_chart_for_two_countries/', generate_emigration_chart_for_two_countries, name='generate_emigration_chart_for_two_countries'),
    path('calculate_sum_for_year/', calculate_sum_for_year, name='calculate_sum_for_year'),
    path('admin_page/', admin_page, name='admin_page'),
    path('country/', country_view, name='country'),
    path('demo/', demoaction, name='demo'),
    
    
]
