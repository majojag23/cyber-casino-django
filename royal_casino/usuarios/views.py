import json
import secrets
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# =====================================================================
# 🏠 VISTAS DE RENDERIZADO DE PLANTILLAS
# =====================================================================

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


# =====================================================================
# 💰 APIS DE LA BILLETERA (SALDO, DEPOSITAR Y RETIRAR)
# =====================================================================

def consultar_saldo_api(request):
    if request.user.is_authenticated:
        try:
            # Intentamos sacar el saldo real de su perfilusuario
            saldo_real = request.user.perfilusuario.saldo
            return JsonResponse({'creditos': float(saldo_real)})
        except AttributeError:
            # Si el usuario es nuevo y el puente aún no se genera visualmente, devolvemos 0 en paz
            return JsonResponse({'creditos': 0.0})
    else:
        return JsonResponse({'error': 'Usuario no autenticado', 'creditos': 0.0}, status=401)

def depositar_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = float(data.get('monto', 0))
            if monto <= 0:
                return JsonResponse({'error': 'El monto debe ser mayor a 0.'}, status=400)
            
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
                return JsonResponse({'error': 'El monto debe ser mayor a 0.'}, status=400)
            if monto > saldo_actual:
                return JsonResponse({'error': 'Saldo insuficiente.'}, status=400)
            
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
# 🛡️ APIS DEL BUSCAMINAS (PANDAS)
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


# =====================================================================
# 🎡 API MULTI-APUESTA DE LA CYBER ROLETT 
# =====================================================================

def girar_ruleta_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            apuestas_recibidas = data.get('apuestas', [])

            if not apuestas_recibidas:
                return JsonResponse({'error': 'No hay apuestas en el tablero.'}, status=400)

            costo_total = sum(float(apuesta['monto']) for apuesta in apuestas_recibidas)

            saldo_actual = request.session.get('wallet_saldo', 1000.00)
            if saldo_actual < costo_total:
                return JsonResponse({'error': 'Saldo insuficiente para cubrir todas las fichas.'}, status=400)

            saldo_actual -= costo_total

            numero_ganador = random.randint(0, 36)
            rojos = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
            color_ganador = 'verde' if numero_ganador == 0 else ('rojo' if numero_ganador in rojos else 'negro')
            es_par = numero_ganador % 2 == 0 if numero_ganador != 0 else None

            total_premiado = 0

            for ap in apuestas_recibidas:
                tipo = ap.get('tipo')
                valor = ap.get('valor')
                monto_ficha = float(ap.get('monto'))

                gano_ficha = False
                mult = 0

                if tipo == 'color' and valor == color_ganador:
                    gano_ficha = True
                    mult = 2
                elif tipo == 'paridad':
                    if valor == 'par' and es_par is True: gano_ficha = True
                    if valor == 'impar' and es_par is False: gano_ficha = True
                    if gano_ficha: mult = 2
                elif tipo == 'numero' and str(valor) == str(numero_ganador):
                    gano_ficha = True
                    mult = 35

                if gano_ficha:
                    total_premiado += (monto_ficha * mult)

            saldo_actual += total_premiado
            request.session['wallet_saldo'] = saldo_actual
            request.session.modified = True

            return JsonResponse({
                'status': 'OK',
                'numero': numero_ganador,
                'color': color_ganador,
                'total_apostado': costo_total,
                'premio_total': total_premiado,
                'nuevo_saldo': saldo_actual
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Método no permitido'}, status=405)