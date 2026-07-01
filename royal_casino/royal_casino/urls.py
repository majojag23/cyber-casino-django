from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 🎯 Importación estricta y absoluta para evitar desvíos en Render
import usuarios.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Tu lobby original
    
    # Endpoints universales de saldo y transacciones vinculados rígidamente
    path('api/saldo/', usuarios.views.consultar_saldo_api, name='consultar_saldo_api'),
    path('usuarios/api/saldo/', usuarios.views.consultar_saldo_api, name='api_saldo_buscaminas'),
    path('api/depositar/', usuarios.views.depositar_api, name='api_depositar'),
    path('api/retirar/', usuarios.views.retirar_api, name='api_retirar'),
    
    # Panda Cyber-Mines (Buscaminas)
    path('iniciar/', usuarios.views.iniciar_buscaminas_api, name='iniciar_buscaminas'),
    path('verificar/', usuarios.views.verificar_celda_api, name='verificar_celda'),
    path('api/apostar/', usuarios.views.procesar_apuesta_api, name='procesar_apuesta_global'),
    
    # Cyber Rolett (Ruleta)
    path('api/ruleta/girar/', usuarios.views.girar_ruleta_api, name='girar_ruleta_api_route'),
    
    # Neon Slots (Tragamonedas)
    path('api/slot/jugar/', usuarios.views.jugar_slot_api, name='jugar_slot_api_route'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)