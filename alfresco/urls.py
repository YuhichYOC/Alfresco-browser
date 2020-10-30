from django.urls import path

from . import views

app_name = 'alfresco'
urlpatterns = [
    path('', views.browse),
]
