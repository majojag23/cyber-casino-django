from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Tu lobby base
    
    # Endpoints universales de saldo y Crypto Minds
    path('api/saldo/', views.consultar_saldo_api, name='consultar_saldo_api'),
    path('usuarios/api/saldo/', views.consultar_saldo_api, name='api_saldo_buscaminas'),
    path('api/apuesta/', views.procesar_apuesta_api, name='api_apuesta_crypto_minds'),
    path('api/depositar/', views.depositar_api, name='api_depositar'),
    path('api/retirar/', views.retirar_api, name='api_retirar'),
    
    # 🐼 ENDPOINTS CORREGIDOS PARA LOS PANDAS (PANDA CYBER-MINES)
    path('api/buscaminas/iniciar/', views.iniciar_buscaminas_api, name='iniciar_buscaminas_real'),
    path('api/buscaminas/verificar/', views.verificar_celda_api, name='verificar_celda_real'),
    path('api/buscaminas/cashout/', views.cashout_buscaminas_api, name='cashout_buscaminas_real'),
    
    # Cyber Rolett y Slots
    path('api/ruleta/girar/', views.girar_ruleta_api, name='girar_ruleta_api_route'),
    path('api/slot/jugar/', views.jugar_slot_api, name='jugar_slot_api_route'),

    # golden jet
    path('juego/golden-jet/', views.golden_jet_juego_vista, name='golden_jet_juego'),
    path('api/golden-jet/accion/', views.jugar_golden_jet_api, name='golden_jet_api_accion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)