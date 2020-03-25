"""ActiveOSS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url,include
from app import views

urlpatterns = [
               path('app/', include('app.urls')),
               path('index/', views.index, name='index'),
               path('login/', views.login, name='login'),
               path('show_data/', views.show_data, name='show_data'),
               path('delete_a_person/', views.delete_a_person, name='delete-person'),
               path('request_approval/', views.request_approval, name='request-approval'),
               path('update_person/', views.update_person, name='update-person'),
               path('table_test/', views.table_test, name='table-test'),
               path('data_visualization/', views.data_visualization, name='data-visualization'),
               path('home/', views.home, name='home'),
               path('add_person/', views.add_person, name='add_person'),
               path('register_crime_record/', views.register_crime_record, name='register-crime-record'),
               path('request_crime_record/', views.request_crime_record, name='request_crime_record'),

               ]