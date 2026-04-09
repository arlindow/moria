from django.urls import path
from versiculos.views import versiculo_unico

urlpatterns = [
    path('', versiculo_unico),
]
