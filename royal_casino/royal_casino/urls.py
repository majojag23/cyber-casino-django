from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.apps import apps

# 🎯 CARGA DINÁMICA DE VIEWS (Esto jamás fallará en el build de Render)
def get_usuarios_view(view_name):
    return apps.get_app_config('usuarios').module.views.__dict__[view_name]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Carga tus juegos y lobby originales
    
    # ==============================================================================
    # 🎰 PUENTES DE CONEXIÓN PARA EL SALDO REAL DE TUS JUEGOS
    # ==============================================================================
    path('api/saldo/', lambda req: get_usuarios_view('consultar_saldo_api')(req), name='consultar_saldo_api'),
    path('usuarios/api/saldo/', lambda req: get_usuarios_view('consultar_saldo_api')(req), name='api_saldo_buscaminas'),
    
    path('juego/apostar/', lambda req: get_usuarios_view('procesar_apuesta_api')(req), name='api_apostar_buscaminas'),
    path('api/apostar/', lambda req: get_usuarios_view('procesar_apuesta_api')(req), name='procesar_apuesta_global'),
    
    path('api/depositar/', lambda req: get_usuarios_view('depositar_api')(req), name='api_depositar_global'),
    path('api/retirar/', lambda req: get_usuarios_view('retirar_api')(req), name='api_retirar_global'),
]

# Servidor de archivos estáticos original
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)