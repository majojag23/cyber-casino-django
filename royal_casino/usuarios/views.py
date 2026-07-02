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
def home_vista(request): return render(request, 'usuarios/lobby.html')

@login_required(login_url='/cuentas/login/')
def slot_juego_vista(request): return render(request, 'usuarios/slot.html')

@login_required(login_url='/cuentas/login/')
def ruleta_juego_vista(request): return render(request, 'usuarios/ruleta.html')

@login_required(login_url='/cuentas/login/')
def golden_jet_juego_vista(request):
    return render(request, 'usuarios/golden_jet.html')

@login_required(login_url='/cuentas/login/')
def buscaminas_vista(request): return render(request, 'usuarios/buscaminas.html')

@login_required(login_url='/cuentas/login/')
def crypto_minds_vista(request): return render(request, 'usuarios/crypto_minds.html')


# ==============================================================================
# 💰 2. CONTROLADORES AUTOMÁTICOS DE BILLETERA
# ==============================================================================

def obtener_perfil_usuario_interno(request):
    try:
        user_obj = request.user
        for rel in [getattr(user_obj, a) for a in dir(user_obj) if 'perfil' in a.lower() or 'billetera' in a.lower()]:
            if hasattr(rel, 'saldo'): return rel
    except Exception: pass
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
# 🎮 3. LÓGICA INTERACTIVA DE LOS JUEGOS SINCRONIZADA CON TUS SCRIPTS
# ==============================================================================

@csrf_exempt
def procesar_apuesta_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    if request.method == 'POST' and request.user.is_authenticated and perfil:
        try:
            data = json.loads(request.body) if request.body else {}
            apuesta = float(data.get('apuesta', 0.0))
            ganancia = float(data.get('ganancia', 0.0))
            saldo_num = float(perfil.saldo)
            if apuesta > 0: saldo_num -= apuesta
            if ganancia > 0: saldo_num += ganancia
            perfil.saldo = saldo_num
            perfil.save()
            saldo_actual = float(perfil.saldo)
        except Exception: pass
    return JsonResponse({'status': 'ok', 'success': True, 'nuevo_saldo': saldo_actual})


# --- 🐼 PANDA CYBER-MINES (SINCRONIZACIÓN DE CLICS DE CASILLAS REAL) ---

@csrf_exempt
def iniciar_buscaminas_api(request):
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
        except Exception: pass
    return JsonResponse({'status': 'ok', 'success': True, 'nuevo_saldo': saldo_actual})


@csrf_exempt
def verificar_celda_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    try: saldo_actual = float(perfil.saldo) if perfil else 8750.00
    except Exception: saldo_actual = 8750.00
    
    # Tablero simulado con un 1 para representar la bomba en una posición fija (ej: la celda 12)
    # y 0 para representar a los pandas en el resto de la matriz.
    tablero_completo_revelado = [0] * 25
    tablero_completo_revelado[12] = 1 
    
    try:
        data = json.loads(request.body) if request.body else {}
        indice_cliqueado = int(data.get('indice', 0))
    except Exception:
        indice_cliqueado = 0

    # Si hace clic en la celda oculta de la bomba (la 12), explota
    if indice_cliqueado == 12:
        return JsonResponse({
            'resultado': 'BOMBA',
            'tablero_completo': tablero_completo_revelado,
            'nuevo_saldo': saldo_actual
        })
    
    # Si hace clic en cualquier otra casilla, encuentra un tierno Panda
    return JsonResponse({
        'resultado': 'PANDA',
        'aciertos': 1,
        'mult': 1.45,
        'ganancia_estimada': 14,
        'nuevo_saldo': saldo_actual
    })


@csrf_exempt
def cashout_buscaminas_api(request):
    perfil = obtener_perfil_usuario_interno(request)
    saldo_actual = float(perfil.saldo) if perfil else 8750.00
    
    tablero_completo_revelado = [0] * 25
    tablero_completo_revelado[12] = 1
    
    if perfil:
        try:
            saldo_num = float(perfil.saldo) + 14.00
            perfil.saldo = saldo_num
            perfil.save()
            saldo_actual = float(perfil.saldo)
        except Exception: pass
        
    return JsonResponse({
        'nuevo_saldo': saldo_actual,
        'ganancia_transferida': 14,
        'tablero_completo': tablero_completo_revelado
    })


# --- 🎰 TRAGAMONEDAS VELOZ (EMOJIS DIRECTOS ANTILENTITUD) ---

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
            saldo_num = (float(perfil.saldo) - 10.00) + premio
            perfil.saldo = saldo_num
            perfil.save()
            saldo_actual = float(perfil.saldo)
        except Exception: pass

    return JsonResponse({
        'status': 'ok', 'success': True, 'resultado': reels, 'reels': reels,
        'premio': premio, 'nuevo_saldo': saldo_actual
    })


# --- 🎡 RULETA INTELIGENTE (MATEMÁTICA COINCIDENTE REAL) ---

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
    # ==============================================================================
# 🛩️ NUEVO JUEGO DESDE 0: GOLDEN JET (ESTILO WIN CASINO)
# ==============================================================================

@csrf_exempt
def golden_jet_vista(request):
    """Renderiza la plantilla HTML limpia del Jet Dorado"""
    return render(request, 'usuarios/golden_jet.html')


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
                
                # Algoritmo profesional: calcula el punto secreto donde el Jet desaparecerá (Crash)
                if random.random() < 0.15:
                    punto_perdida = 1.00  # 15% de probabilidad de perder al instante
                else:
                    punto_perdida = round(1.02 + random.expovariate(0.5), 2)
                    if punto_perdida > 30.00: punto_perdida = 30.00 # Límite máximo de premio

                # Descontar apuesta de la base de datos
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

                # Validación de seguridad: verificamos que no se haya cobrado después del límite real
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
                    # Busted: El usuario intentó cobrar pero el Jet ya se había ido en el servidor
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