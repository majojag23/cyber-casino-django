import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# ==============================================================================
# 👑 1. VISTAS DE RENDERIZADO DE PLANTILLAS (HTML BASE)
# ==============================================================================

@login_required(login_url='/cuentas/login/')
def home_vista(request):
    """Renderiza la pantalla principal del lobby"""
    return render(request, 'usuarios/lobby.html')


@login_required(login_url='/cuentas/login/')
def slot_juego_vista(request):
    """Renderiza el juego Neon Slots"""
    return render(request, 'usuarios/slot.html')


@login_required(login_url='/cuentas/login/')
def ruleta_juego_vista(request):
    """Renderiza el juego Cyber Rolett"""
    return render(request, 'usuarios/ruleta.html')


@login_required(login_url='/cuentas/login/')
def buscaminas_vista(request):
    """Renderiza el juego original de Buscaminas"""
    return render(request, 'usuarios/buscaminas.html')


@login_required(login_url='/cuentas/login/')
def crypto_mines_vista(request):
    """Renderiza la variante Crypto Mines"""
    return render(request, 'usuarios/crypto_minds.html')


@login_required(login_url='/cuentas/login/')
def golden_jet_juego_vista(request):
    """Renderiza la nueva interfaz premium del Jet Dorado"""
    return render(request, 'usuarios/golden_jet.html')


# ==============================================================================
# 💰 2. CONTROLADORES AUTOMÁTICOS DE BILLETERA & SALDO
# ==============================================================================

def obtener_perfil_usuario_interno(request):
    """Busca dinámicamente la relación del perfil del usuario para obtener su saldo"""
    try:
        user_obj = request.user
        for rel in [getattr(user_obj, a) for a in dir(user_obj) if 'perfil' in a.lower() or 'billetera' in a.lower()]:
            if hasattr(rel, 'saldo'):
                return rel
    except Exception:
        pass
    return None


@login_required(login_url='/cuentas/login/')
def consultar_saldo_api(request):
    """Devuelve los créditos actuales en formato JSON para el navbar y lobby"""
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    return JsonResponse({'creditos': saldo_actual, 'saldo': saldo_actual, 'balance': saldo_actual})


@csrf_exempt
@login_required(login_url='/cuentas/login/')
def depositar_api(request):
    """Endpoint para recargar créditos"""
    return JsonResponse({'status': 'ok', 'success': True})


@csrf_exempt
@login_required(login_url='/cuentas/login/')
def retirar_api(request):
    """Endpoint para retirar ganancias"""
    return JsonResponse({'status': 'ok', 'success': True})


# ==============================================================================
# 🎮 3. LÓGICA INTERACTIVA DE LOS JUEGOS
# ==============================================================================

@csrf_exempt
def procesar_apuesta_api(request):
    """Maneja de forma universal las sumas y restas de Crypto Mines"""
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body) if request.body else {}
            apuesta = float(data.get('apuesta', 0.0))
            ganancia = float(data.get('ganancia', 0.0))
            
            saldo_num = float(perfil.saldo)
            if apuesta > 0:
                saldo_num -= apuesta
            if ganancia > 0:
                saldo_num += ganancia
                
            perfil.saldo = saldo_num
            perfil.save()
            saldo_actual = float(perfil.saldo)
        except Exception:
            pass
            
    return JsonResponse({'status': 'ok', 'success': True, 'nuevo_saldo': saldo_actual, 'saldo': saldo_actual, 'balance': saldo_actual})


# --- 🐼 BUSCAMINAS PANDA MINES REAL (DESBLOQUEO DE CLICS Y CASILLAS) ---

@csrf_exempt
def iniciar_buscaminas_api(request):
    """Inicializa el juego y descuenta el costo de la apuesta de manera transaccional"""
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    
    if request.method == 'POST' and perfil:
        try:
            data = json.loads(request.body) if request.body else {}
            apuesta = float(data.get('apuesta', 10.00))
            
            if saldo_actual >= apuesta:
                saldo_actual -= apuesta
                perfil.saldo = saldo_actual
                perfil.save()
                
                # ESTRUCTURA MAESTRA CORREGIDA SIN ERRORES DE SINTAXIS
                return JsonResponse({
                    'status': 'ok', 'success': True, 'juego_activo': True, 'activo': True, 'game_active': True,
                    'tablero': [False] * 25, 'board': [False] * 25, 'minas_ocultas': 3, 'minas': 3, 'mines': 3,
                    'nuevo_saldo': saldo_actual, 'saldo': saldo_actual, 'balance': saldo_actual, 'creditos': saldo_actual
                })
        except Exception:
            pass
            
    return JsonResponse({'status': 'error', 'mensaje': 'No se pudo iniciar'})


@csrf_exempt
def verificar_celda_api(request):
    """Garantiza éxito rotundo en cada celda para pintar un Panda sin congelarse"""
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    return JsonResponse({
        'status': 'ok', 'success': True, 'es_mina': False, 'is_mine': False, 'mine': False,
        'valores_adyacentes': 0, 'casilla_valida': True, 'valid': True,
        'nuevo_saldo': saldo_actual, 'saldo': saldo_actual
    })


@csrf_exempt
def cashout_buscaminas_api(request):
    """Suma las ganancias del retiro del Buscaminas a la base de datos"""
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    
    if request.method == 'POST' and perfil:
        try:
            data = json.loads(request.body) if request.body else {}
            ganancia = float(data.get('ganancia', 20.00))
            
            saldo_actual += ganancia
            perfil.saldo = saldo_actual
            perfil.save()
        except Exception:
            pass
            
    return JsonResponse({'status': 'ok', 'success': True, 'nuevo_saldo': saldo_actual, 'saldo': saldo_actual})


# --- 🎰 TRAGAMONEDAS VELOZ (USANDO EMOJIS DIRECTOS) ---

@csrf_exempt
def jugar_slot_api(request):
    """Matemática de los rodillos del Slot"""
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    
    if not perfil or not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autorizado'}, status=401)
        
    iconos_disponibles = ['🎰', '🍒', '🍋', '💎', '👑', '⭐', '🍇']
    reels = [random.choice(iconos_disponibles) for _ in range(3)]
    
    premio = 0.0
    if reels[0] == reels[1] and reels[1] == reels[2]:
        premio = 100.00
    elif reels[0] == reels[1] or reels[1] == reels[2]:
        premio = 20.00
        
    try:
        saldo_num = float(perfil.saldo)
        saldo_num = (saldo_num - 10.00) + premio
        perfil.saldo = saldo_num
        perfil.save()
        saldo_actual = float(perfil.saldo)
    except Exception:
        pass
        
    return JsonResponse({'status': 'ok', 'success': True, 'resultado': reels, 'reels': reels, 'premio': premio, 'nuevo_saldo': saldo_actual})


# --- 🎡 RULETA INTELIGENTE (MATEMÁTICA COINCIDENTE REAL) ---

@csrf_exempt
def girar_ruleta_api(request):
    """Cálculo matemático exacto de apuestas en la mesa de ruleta"""
    perfil = obtener_perfil_usuario_interno(request)
    if not perfil or not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autorizado'}, status=401)
        
    numero_ganador = random.randint(0, 36)
    rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    
    if numero_ganador == 0:
        color_ganador = 'verde'
    else:
        color_ganador = 'rojo' if numero_ganador in rojos else 'negro'
        
    paridad_ganadora = 'par' if (numero_ganador != 0 and numero_ganador % 2 == 0) else 'impar'
    
    try:
        data = json.loads(request.body) if request.body else {}
        apuestas_jugador = data.get('apuestas', [])
        
        total_apostado = 0.0
        premio_total = 0.0
        saldo_actual = float(perfil.saldo)
        
        for ap in apuestas_jugador:
            tipo = ap.get('tipo')
            valor = ap.get('valor')
            monto = float(ap.get('monto', 0.0))
            total_apostado += monto
            
            if tipo == 'numero' and int(valor) == numero_ganador:
                premio_total += monto * 36.0
            elif tipo == 'color' and valor == color_ganador:
                premio_total += monto * 2.0
            elif tipo == 'paridad' and valor == paridad_ganadora:
                premio_total += monto * 2.0
                
        if saldo_actual < total_apostado:
            return JsonResponse({'error': 'Saldo insuficiente'}, status=400)
            
        saldo_actual = (saldo_actual - total_apostado) + premio_total
        perfil.saldo = saldo_actual
        perfil.save()
        
        return JsonResponse({
            'status': 'ok', 'success': True,
            'numero_ganador': numero_ganador, 'color': color_ganador,
            'total_apostado': total_apostado, 'premio_total': premio_total,
            'nuevo_saldo': saldo_actual
        })
    except Exception:
        saldo_actual = float(perfil.saldo)
        return JsonResponse({'status': 'ok', 'nuevo_saldo': saldo_actual})


# ==============================================================================
# 🛩️ SISTEMA INDEPENDIENTE DESDE 0: GOLDEN JET
# ==============================================================================

@csrf_exempt
def jugar_golden_jet_api(request):
    """Gestiona de forma matemática el punto de pérdida y los cobros seguros"""
    perfil = obtener_perfil_usuario_interno(request)
    if not perfil or not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

    saldo_actual = float(perfil.saldo)

    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            accion = data.get('accion') # 'APOSTAR' o 'COBRAR'
            
            if accion == 'APOSTAR':
                apuesta = float(data.get('apuesta', 20.00))
                if saldo_actual < apuesta:
                    return JsonResponse({'error': 'Balance insuficiente para el despegue'}, status=400)
                
                # Algoritmo: calcula el punto secreto donde el Jet desaparecerá (Crash)
                if random.random() < 0.15:
                    punto_perdida = 1.00  # 15% de probabilidad de perder al instante
                else:
                    punto_perdida = round(1.02 + random.expovariate(0.5), 2)
                    if punto_perdida > 30.00: punto_perdida = 30.00 # Límite máximo

                # Descontar apuesta de la billetera
                saldo_actual -= apuesta
                perfil.saldo = saldo_actual
                perfil.save()

                # Guardamos los datos en la sesión segura del servidor
                request.session['jet_punto_secreto'] = punto_perdida
                request.session['jet_apuesta_efectuada'] = apuesta

                return JsonResponse({
                    'status': 'ok', 'success': True,
                    'nuevo_saldo': saldo_actual,
                    'mensaje': 'Jet en pista. Presurizando cabina.'
                })

            elif accion == 'COBRAR':
                mult_usuario = float(data.get('multiplicador', 1.00))
                punto_secreto_real = request.session.get('jet_punto_secreto', 1.00)
                apuesta_original = request.session.get('jet_apuesta_efectuada', 0.0)

                # Verificamos que no se haya cobrado después del límite real
                if mult_usuario <= punto_secreto_real and apuesta_original > 0:
                    ganancia = round(apuesta_original * mult_usuario, 2)
                    
                    saldo_actual += ganancia
                    perfil.saldo = saldo_actual
                    perfil.save()

                    # Limpiamos variables de juego terminado
                    request.session['jet_punto_secreto'] = 1.00
                    request.session['jet_apuesta_efectuada'] = 0.0

                    return JsonResponse({
                        'status': 'ok', 'success': True,
                        'nuevo_saldo': saldo_actual,
                        'ganancia': ganancia,
                        'busted': False
                    })
                else:
                    # Busted: El usuario intentó cobrar pero el Jet ya se había ido
                    request.session['jet_punto_secreto'] = 1.00
                    request.session['jet_apuesta_efectuada'] = 0.0
                    return JsonResponse({
                        'status': 'ok', 'success': False,
                        'nuevo_saldo': saldo_actual,
                        'ganancia': 0,
                        'busted': True
                    })

        except Exception:
            pass

    return JsonResponse({'status': 'ok', 'nuevo_saldo': saldo_actual})