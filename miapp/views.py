import json
import secrets
from django.shortcuts import render
from django.http import JsonResponse

# =====================================================================
# 🏠 VISTAS DE RENDERIZADO DE PLANTILLAS
# =====================================================================

def home_vista(request):
    return render(request, 'usuarios/lobby.html')

def slot_juego_vista(request):
    return render(request, 'usuarios/slot.html')

def ruleta_juego_vista(request):
    return render(request, 'usuarios/ruleta.html')

def buscaminas_vista(request):
    return render(request, 'usuarios/buscaminas.html')

def crypto_minds_vista(request):
    return render(request, 'usuarios/crypto_minds.html')


# =====================================================================
# 💰 APIS DE LA BILLETERA (CONTROL DE SALDO, DEPOSITAR Y RETIRAR)
# =====================================================================

def consultar_saldo_api(request):
    if 'wallet_saldo' not in request.session:
        request.session['wallet_saldo'] = 1000.00
    saldo = request.session.get('wallet_saldo', 1000.00)
    return JsonResponse({'creditos': saldo})


def depositar_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = float(data.get('monto', 0))
            if monto <= 0:
                return JsonResponse({'error': 'El monto a depositar debe ser mayor a 0.'}, status=400)
            
            saldo_actual = request.session.get('wallet_saldo', 1000.00) + monto
            request.session['wallet_saldo'] = saldo_actual
            request.session.modified = True
            return JsonResponse({'status': 'OK', 'nuevo_saldo': saldo_actual})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def retirar_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = float(data.get('monto', 0))
            saldo_actual = request.session.get('wallet_saldo', 1000.00)
            
            if monto <= 0:
                return JsonResponse({'error': 'El monto a retirar debe ser mayor a 0.'}, status=400)
            if monto > saldo_actual:
                return JsonResponse({'error': 'No tienes suficientes créditos para este retiro.'}, status=400)
            
            saldo_actual -= monto
            request.session['wallet_saldo'] = saldo_actual
            request.session.modified = True
            return JsonResponse({'status': 'OK', 'nuevo_saldo': saldo_actual})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def procesar_apuesta_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            apuesta = float(data.get('apuesta', 0))
            ganancia = float(data.get('ganancia', 0))
            saldo_actual = request.session.get('wallet_saldo', 1000.00)
            
            if apuesta > 0:
                if saldo_actual < apuesta:
                    return JsonResponse({'error': 'Saldo insuficiente'}, status=400)
                saldo_actual -= apuesta
                
            if ganancia > 0:
                saldo_actual += ganancia
                
            request.session['wallet_saldo'] = saldo_actual
            request.session.modified = True
            return JsonResponse({'status': 'OK', 'nuevo_saldo': saldo_actual})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


# =====================================================================
# 🛡️ APIS SEGURAS DEL BUSCAMINAS
# =====================================================================

def calcular_multiplicador_backend(aciertos, minas):
    def combinacion(n, k):
        if k > n or k < 0: return 0
        if k == 0 or n == k: return 1
        res = 1
        for i in range(1, k + 1):
            res = res * (n - k + i) // i
        return res

    combinacion_total = combinacion(25, aciertos)
    combinacion_seguras = combinacion(25 - minas, aciertos)
    if combinacion_seguras == 0: return 1.0
    multiplicador_teorico = combinacion_total / combinacion_seguras
    return round(multiplicador_teorico * 0.97, 2)


def iniciar_buscaminas_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            minas_configuradas = int(data.get('minas', 1))
            apuesta = int(data.get('apuesta', 10))
            
            saldo_actual = request.session.get('wallet_saldo', 1000.00)
            if saldo_actual < apuesta:
                return JsonResponse({'error': 'Saldo insuficiente.'}, status=400)
            
            saldo_actual -= apuesta
            request.session['wallet_saldo'] = saldo_actual
            
            tablero = [0] * 25
            colocadas = 0
            while colocadas < minas_configuradas:
                idx = secrets.randbelow(25)
                if tablero[idx] == 0:
                    tablero[idx] = 1
                    colocadas += 1
            
            request.session['buscaminas_tablero'] = tablero
            request.session['buscaminas_apuesta'] = apuesta
            request.session['buscaminas_minas'] = minas_configuradas
            request.session['buscaminas_aciertos'] = 0
            request.session['buscaminas_jugando'] = True
            request.session.modified = True
            
            return JsonResponse({'status': 'OK', 'nuevo_saldo': saldo_actual})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def verificar_celda_api(request):
    if request.method == 'POST':
        if not request.session.get('buscaminas_jugando', False):
            return JsonResponse({'error': 'No hay sesión activa.'}, status=400)
            
        try:
            data = json.loads(request.body)
            celda_seleccionada = int(data.get('indice'))
            
            tablero = request.session.get('buscaminas_tablero')
            apuesta = request.session.get('buscaminas_apuesta')
            minas = request.session.get('buscaminas_minas')
            
            if tablero[celda_seleccionada] == 1:
                request.session['buscaminas_jugando'] = False
                request.session.modified = True
                return JsonResponse({'resultado': 'BOMBA', 'tablero_completo': tablero})
            
            request.session['buscaminas_aciertos'] += 1
            request.session.modified = True
            
            aciertos = request.session['buscaminas_aciertos']
            mult_actual = calcular_multiplicador_backend(aciertos, minas)
            ganancia_estimada = int(apuesta * mult_actual)
            
            if aciertos >= (25 - minas):
                saldo_actual = request.session.get('wallet_saldo', 1000.00) + ganancia_estimada
                request.session['wallet_saldo'] = saldo_actual
                request.session['buscaminas_jugando'] = False
                request.session.modified = True
                return JsonResponse({
                    'resultado': 'COMPLETADO', 'aciertos': aciertos, 'mult': mult_actual,
                    'ganancia': ganancia_estimada, 'nuevo_saldo': saldo_actual, 'tablero_completo': tablero
                })
                
            return JsonResponse({
                'resultado': 'PANDA', 'aciertos': aciertos, 'mult': mult_actual, 'ganancia_estimada': ganancia_estimada
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def cashout_buscaminas_api(request):
    if request.method == 'POST':
        if not request.session.get('buscaminas_jugando', False):
            return JsonResponse({'error': 'No hay partida activa.'}, status=400)
            
        aciertos = request.session.get('buscaminas_aciertos', 0)
        if aciertos == 0:
            return JsonResponse({'error': 'Encuentra al menos un panda.'}, status=400)
            
        apuesta = request.session.get('buscaminas_apuesta')
        minas = request.session.get('buscaminas_minas')
        tablero = request.session.get('buscaminas_tablero')
        
        mult_final = calcular_multiplicador_backend(aciertos, minas)
        ganancia_final = int(apuesta * mult_final)
        
        saldo_actual = request.session.get('wallet_saldo', 1000.00) + ganancia_final
        request.session['wallet_saldo'] = saldo_actual
        request.session['buscaminas_jugando'] = False
        request.session.modified = True
        
        return JsonResponse({
            'status': 'OK', 'ganancia_transferida': ganancia_final, 'nuevo_saldo': saldo_actual, 'tablero_completo': tablero
        })
    return JsonResponse({'error': 'Método no permitido'}, status=405)