from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 🎯 IMPORTACIÓN RELATIVA LOCAL (Esto evita el fallo de compilación en Render)
from usuarios import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Carga tus juegos y lobby originales
    
    # ==============================================================================
    # 🎰 PUENTES DE CONEXIÓN PARA EL SALDO REAL DE TUS JUEGOS
    # ==============================================================================
    path('api/saldo/', views.consultar_saldo_api, name='consultar_saldo_api'),
    path('usuarios/api/saldo/', views.consultar_saldo_api, name='api_saldo_buscaminas'),
    
    path('juego/apostar/', views.procesar_apuesta_api, name='api_apostar_buscaminas'),
    path('api/apostar/', views.procesar_apuesta_api, name='procesar_apuesta_global'),
    
    path('api/depositar/', views.depositar_api, name='api_depositar_global'),
    path('api/retirar/', views.retirar_api, name='api_retirar_global'),
]

# Servidor de archivos estáticos original
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)