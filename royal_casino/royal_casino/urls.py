from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios import views  # 👈 1. IMPORTACIÓN MÁGICA: Conecta este archivo con tu views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Tu ruta original para el lobby y juegos
    
    # ==============================================================================
    # 🎯 2. PUENTES DE CONEXIÓN PARA QUE LOS JUEGOS LEAN TUS 6000 PESOS REALES
    # ==============================================================================
    path('api/saldo/', views.consultar_saldo_api, name='consultar_saldo_api'),
    path('usuarios/api/saldo/', views.consultar_saldo_api, name='api_saldo_buscaminas'),
    
    path('juego/apostar/', views.procesar_apuesta_api, name='api_apostar_buscaminas'),
    path('api/apostar/', views.procesar_apuesta_api, name='procesar_apuesta_global'),
    
    path('api/depositar/', views.depositar_api, name='api_depositar_global'),
    path('api/retirar/', views.retirar_api, name='api_retirar_global'),
]

# Tus rutas originales de archivos estáticos e imágenes del casino
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)