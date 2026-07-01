from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios import views  # Importación de tus vistas unificadas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Tu lobby y pantallas base
    
    # ==============================================================================
    # 🎯 ENDPOINTS DE JUEGO (APUNTANDO CORRECTAMENTE A VIEWS)
    # ==============================================================================
    path('api/saldo/', views.consultar_saldo_api, name='consultar_saldo_api'),
    path('usuarios/api/saldo/', views.consultar_saldo_api, name='api_saldo_buscaminas'),
    
    # Rutas para Buscaminas (Panda Cyber-Mines)
    path('iniciar/', views.iniciar_buscaminas_api, name='iniciar_buscaminas'),
    path('verificar/', views.verificar_celda_api, name='verificar_celda'),
    path('api/apostar/', views.procesar_apuesta_api, name='procesar_apuesta_global'),
    
    # Ruta para Ruleta (Cyber Rolett)
    path('api/ruleta/girar/', views.girar_ruleta_api, name='girar_ruleta_api_route'),
    
    # Ruta para Slots (Neon Slots)
    path('api/slot/jugar/', views.jugar_slot_api, name='jugar_slot_api_route'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)