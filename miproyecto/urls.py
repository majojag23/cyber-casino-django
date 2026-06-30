from django.contrib import admin
from django.urls import path, include
from royal_casino.usuarios import views  # 👈 Importamos directo desde tu app real

urlpatterns = [
    # 🔑 PANEL DE ADMIN Y SISTEMA DE CUENTAS (Las nuevas conexiones)
    path('admin/', admin.site.urls),
    path('cuentas/', include('cuentas.urls')),
   
    # 🏠 LOBBY PRINCIPAL
    path('', views.home_vista, name='home'),

    # 🎮 JUEGOS ACTIVOS
    path('juego/slot/', views.slot_juego_vista, name='slot_juego'),
    path('juego/ruleta/', views.ruleta_juego_vista, name='ruleta_juego'),
    path('juego/buscaminas/', views.buscaminas_vista, name='buscaminas_juego'),
    path('juego/crypto-minds/', views.crypto_minds_vista, name='crypto_minds'),
    
    # 💰 ENDPOINTS DE LA BILLETERA (Historial de créditos)
    path('api/saldo/', views.consultar_saldo_api, name='api_saldo'),
    path('api/depositar/', views.depositar_api, name='api_depositar'),
    path('api/retirar/', views.retirar_api, name='api_retirar'),
    path('api/apuesta/', views.procesar_apuesta_api, name='api_apuesta'),

    # 🚀 ENDPOINTS DEL BUSCAMINAS (Módulo seguro)
    path('api/buscaminas/iniciar/', views.iniciar_buscaminas_api, name='buscaminas_iniciar_api'),
    path('api/buscaminas/verificar/', views.verificar_celda_api, name='buscaminas_verificar_api'),
    path('api/buscaminas/cashout/', views.cashout_buscaminas_api, name='buscaminas_cashout_api'),

    # 🎡 NUEVO ENDPOINT DE LA CYBER ROLETT (Matemáticas del servidor)
    path('api/ruleta/girar/', views.girar_ruleta_api, name='api_ruleta_girar'),

    # 🛠️ PANEL DE ADMINISTRACIÓN GENERAL
    path('admin/', admin.site.urls),
]