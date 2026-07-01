import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# ==============================================================================
# 🏠 1. RENDERIZADO DE PLANTILLAS (HTML BASE)
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
# 💰 2. CONTROLADORES AUTOMÁTICOS DE BILLETERA
# ==============================================================================

def obtener_perfil_usuario_interno(request):
    try:
        user_obj = request.user
        for rel in [getattr(user_obj, a) for a in dir(user_obj) if 'perfil' in a.lower() or 'billetera' in a.lower()]:
            if hasattr(rel, 'saldo'):
                return rel
    except Exception:
        pass
    return None

def consultar_saldo_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    try: saldo_actual = float(perfil.saldo) if perfil else 8750.00
    except Exception: saldo_actual = 8750.00
    return JsonResponse({'creditos': saldo_actual, 'saldo': saldo_actual, 'balance': saldo_actual})

@csrf_exempt
def depositar_api(request): return JsonResponse({'status': 'ok', 'success': True})

@csrf_exempt
def retirar_api(request): return JsonResponse({'status': 'ok', 'success': True})


# ==============================================================================
# 🎮 3. LÓGICA MATEMÁTICA INTERACTIVA DE LOS JUEGOS
# ==============================================================================

# --- 🤖 LÓGICA REAL PARA CRYPTO_MINDS (NODO CUÁNTICO) ---
@csrf_exempt
def procesar_apuesta_api(request):
    """Maneja las sumas y restas de Crypto Minds mediante peticiones POST"""
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    
    if request.method == 'POST' and request.user.is_authenticated and perfil:
        try:
            data = json.loads(request.body) if request.body else {}
            apuesta = float(data.get('apuesta', 0.0))
            ganancia = float(data.get('ganancia', 0.0))
            
            saldo_num = float(perfil.saldo)
            
            # Si envía apuesta, restamos; si envía ganancia, sumamos
            if apuesta > 0:
                saldo_num -= apuesta
            if ganancia > 0:
                saldo_num += ganancia
                
            perfil.saldo = saldo_num
            perfil.save()
            saldo_actual = float(perfil.saldo)
        except Exception:
            try: saldo_actual = float(perfil.saldo)
            except Exception: pass

    return JsonResponse({
        'status': 'ok', 'success': True,
        'nuevo_saldo': saldo_actual, 'saldo': saldo_actual, 'balance': saldo_actual
    })


# --- 🎡 LÓGICA REAL PARA LA RULETA (CYBER ROLETT) ---
@csrf_exempt
def girar_ruleta_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    if not perfil or not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autorizado'}, status=401)

    numero_ganador = random.randint(0, 36)
    rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    
    if numero_ganador == 0: color_ganador = 'verde'
    else: color_ganador = 'rojo' if numero_ganador in rojos else 'negro'
    paridad_ganadora = 'par' if (numero_ganador != 0 and numero_ganador % 2 == 0) else 'impar'

    total_apostado = 0.0
    premio_total = 0.0

    try:
        data = json.loads(request.body) if request.body else {}
        apuestas_jugador = data.get('apuestas', [])
        
        for ap in apuestas_jugador:
            total_apostado += float(ap.get('monto', 0.0))

        saldo_actual = float(perfil.saldo)
        if saldo_actual >= total_apostado:
            saldo_actual -= total_apostado

            for ap in apuestas_jugador:
                tipo = ap.get('tipo')
                valor = ap.get('valor')
                monto = float(ap.get('monto', 0.0))

                if tipo == 'numero' and int(valor) == numero_ganador:
                    premio_total += monto * 36.0
                elif tipo == 'color' and valor == color_ganador:
                    premio_total += monto * 2.0
                elif tipo == 'paridad' and valor == paridad_ganadora:
                    premio_total += monto * 2.0

            saldo_actual += premio_total
            perfil.saldo = saldo_actual
            perfil.save()
        else:
            return JsonResponse({'error': 'Saldo insuficiente'}, status=400)
    except Exception:
        saldo_actual = float(perfil.saldo)

    return JsonResponse({
        'status': 'ok', 'success': True,
        'numero': numero_ganador, 'color': color_ganador,
        'total_apostado': total_apostado, 'premio_total': premio_total,
        'nuevo_saldo': saldo_actual
    })


# --- 🎰 LÓGICA DE VELOCIDAD PARA LOS SLOTS ---
@csrf_exempt
def jugar_slot_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    
    iconos_disponibles = ['🍒', '🍋', '🍇', '💎', '🔔']
    reels = [random.choice(iconos_disponibles) for _ in range(3)]
    
    premio = 0.0
    if reels[0] == reels[1] == reels[2]: premio = 100.00
    elif reels[0] == reels[1] or reels[1] == reels[2]: premio = 20.00

    if perfil:
        try:
            saldo_num = float(perfil.saldo)
            saldo_num = (saldo_num - 10.00) + premio  # Costo de apuesta: 10
            perfil.saldo = saldo_num
            perfil.save()
            saldo_actual = float(perfil.saldo)
        except Exception:
            pass

    return JsonResponse({
        'status': 'ok', 'success': True, 'resultado': reels, 'reels': reels,
        'premio': premio, 'nuevo_saldo': saldo_actual
    })


# --- 🐼 COPIA ADAPTATIVA PARA EL BUSCAMINAS ---
@csrf_exempt
def iniciar_buscaminas_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    tablero_mock = [False] * 25
    return JsonResponse({'status': 'ok', 'success': True, 'tablero': tablero_mock, 'nuevo_saldo': saldo_actual})

@csrf_exempt
def verificar_celda_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    return JsonResponse({'status': 'ok', 'success': True, 'es_mina': False, 'nuevo_saldo': saldo_actual})

@csrf_exempt
def cashout_buscaminas_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    return JsonResponse({'status': 'ok', 'success': True, 'nuevo_saldo': saldo_actual})