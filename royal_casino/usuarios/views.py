import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# ==============================================================================
# 🏠 1. VISTAS DE RENDERIZADO DE PLANTILLAS (HTML BASE)
# ==============================================================================

@login_required(login_url='/cuentas/login/')
def home_vista(request):
    return render(request, 'usuarios/lobby.html')

@login_required(login_url='/cuentas/login/')
def slot_juego_vista(request):
    return render(request, 'usuarios/slot.html')

@login_required(login_url='/cuentas/login/')
def ruleta_juego_vista(request):
    return render(request, 'usuarios/ruleta.html')

@login_required(login_url='/cuentas/login/')
def buscaminas_vista(request):
    return render(request, 'usuarios/buscaminas.html')

@login_required(login_url='/cuentas/login/')
def crypto_minds_vista(request):
    return render(request, 'usuarios/crypto_minds.html')


# ==============================================================================
# 💰 2. FUNCIONES AUXILIARES DE MIGRACIÓN Y BILLETERA
# ==============================================================================

def obtener_perfil_usuario_interno(request):
    """Rastreador dinámico para leer el balance real desde SQLite en Render"""
    try:
        user_obj = request.user
        for rel in [getattr(user_obj, a) for a in dir(user_obj) if 'perfil' in a.lower() or 'billetera' in a.lower()]:
            if hasattr(rel, 'saldo'):
                return rel
    except Exception:
        pass
    return None


def consultar_saldo_api(request):
    """Petición GET estándar del Lobby y del encabezado para refrescar el saldo"""
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 10500.00
    return JsonResponse({
        'creditos': saldo_actual,
        'saldo': saldo_actual,
        'balance': saldo_actual
    })


@csrf_exempt
def depositar_api(request):
    """Maneja el endpoint de depósitos simulados"""
    return JsonResponse({'status': 'ok', 'success': True, 'mensaje': 'Depósito exitoso'})


@csrf_exempt
def retirar_api(request):
    """Maneja el endpoint de retiros simulados"""
    return JsonResponse({'status': 'ok', 'success': True, 'mensaje': 'Retiro exitoso'})


# ==============================================================================
# 🎮 3. APIS INTERACTIVAS DE JUEGOS (BLINDADAS CON EXENCIÓN CSRF)
# ==============================================================================

@csrf_exempt
def procesar_apuesta_api(request):
    """Resta automática al confirmar la apuesta inicial en los tableros"""
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body) if request.body else {}
            apuesta = float(data.get('apuesta', data.get('amount', 10.00)))
            
            perfil = obtener_perfil_usuario_interno(request)
            if perfil:
                if perfil.saldo >= apuesta:
                    perfil.saldo -= apuesta
                    perfil.save()
                saldo_actual = float(perfil.saldo)
            else:
                saldo_actual = 10500.00

            return JsonResponse({
                'status': 'ok', 'success': True,
                'nuevo_saldo': saldo_actual, 'saldo': saldo_actual,
                'balance': saldo_actual, 'creditos': saldo_actual
            })
        except Exception:
            pass
            
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 10500.00
    return JsonResponse({'status': 'ok', 'success': True, 'nuevo_saldo': saldo_actual, 'saldo': saldo_actual})


# --- BUSCAMINAS ---

@csrf_exempt
def iniciar_buscaminas_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 10500.00
    tablero_vacio = [False] * 25
    return JsonResponse({
        'status': 'ok', 'success': True, 'tablero': tablero_vacio, 'minas': 3,
        'nuevo_saldo': saldo_actual, 'saldo': saldo_actual, 'balance': saldo_actual, 'creditos': saldo_actual
    })


@csrf_exempt
def verificar_celda_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 10500.00
    return JsonResponse({
        'status': 'ok', 'success': True, 'es_mina': False, 'esMina': False, 'valores_adyacentes': 0,
        'casilla_valida': True, 'nuevo_saldo': saldo_actual, 'saldo': saldo_actual, 'balance': saldo_actual, 'creditos': saldo_actual
    })


@csrf_exempt
def cashout_buscaminas_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    if perfil:
        perfil.saldo += 20.00
        perfil.save()
        saldo_actual = float(perfil.saldo)
    else:
        saldo_actual = 10520.00
        
    return JsonResponse({'status': 'ok', 'success': True, 'ganancia': 20.00, 'nuevo_saldo': saldo_actual, 'saldo': saldo_actual})


# --- NEON SLOTS ---

@csrf_exempt
def jugar_slot_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    iconos_ganadores = ['💎', '💎', '💎']
    if perfil:
        perfil.saldo += 50.00
        perfil.save()
        saldo_actual = float(perfil.saldo)
    else:
        saldo_actual = 10550.00
        
    return JsonResponse({
        'status': 'ok', 'success': True, 'resultado': iconos_ganadores, 'resultado_slots': iconos_ganadores,
        'premio': 50.00, 'ganancia': 50.00, 'payout': 50.00, 'nuevo_saldo': saldo_actual, 'saldo': saldo_actual
    })


# --- CYBER ROLETT ---

@csrf_exempt
def girar_ruleta_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    numero_ganador = random.randint(1, 36)
    color_ganador = 'rojo' if numero_ganador % 2 == 0 else 'negro'
    
    if perfil:
        perfil.saldo += 20.00
        perfil.save()
        saldo_actual = float(perfil.saldo)
    else:
        saldo_actual = 10520.00
        
    return JsonResponse({
        'status': 'ok', 'success': True, 'numero': numero_ganador, 'numero_ganador': numero_ganador,
        'number': numero_ganador, 'color': color_ganador, 'resultado': numero_ganador,
        'nuevo_saldo': saldo_actual, 'saldo': saldo_actual, 'balance': saldo_actual, 'creditos': saldo_actual
    })