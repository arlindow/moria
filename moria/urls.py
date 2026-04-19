from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('oracao/', views.oracao, name='oracao'),
    path('reunioes/', views.reunioes, name='reunioes'),

    # Jogo
    path('jogo/', views.jogo_home, name='jogo_home'),
    path('jogo/criar/', views.jogo_criar, name='jogo_criar'),
    path('jogo/entrar/', views.jogo_entrar, name='jogo_entrar'),
    path('jogo/sala/<str:codigo>/lider/', views.jogo_sala_lider, name='jogo_sala_lider'),

    # API
    path('api/sala/<str:codigo>/', views.api_sala_status, name='api_sala_status'),
]