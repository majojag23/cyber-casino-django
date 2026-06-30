import json
import secrets
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# IMPORTANTE: Aquí está la pieza que le faltaba a Python arriba:
from django.core.exceptions import ObjectDoesNotExist
# ==============================================================================
# 🏠 VISTAS DE RENDERIZADO DE PLANTILLAS (CON CANDADO DIGITAL)
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


# ==============================================================================
# 💰 APIS DE LA BILLETERA REAL (CONECTADAS AL PANEL DE ADMINISTRACIÓN)
# ==============================================================================

def consultar_saldo_api(request):
    if request.user.is_authenticated:
        try:
            # Saca el saldo real directamente del PerfilUsuario del panel administrativo
            saldo_real = request.user.perfilusuario.saldo
            return JsonResponse({'creditos': float(saldo_real)})
        except (AttributeError, ObjectDoesNotExist):
            # Si el usuario es nuevo y no tiene billetera en el admin, muestra 0 de forma segura
            return JsonResponse({'creditos': 0.0})
    else:
        return JsonResponse({'error': 'Usuario no autenticado', 'creditos': 0.0}, status=401)


def depositar_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = float(data.get('monto', 0))
            if monto <= 0:
                return JsonResponse({'error': 'El monto debe ser mayor a 0'}, status=400)
            
            if request.user.is_authenticated:
                try:
                    # Modifica directamente el saldo en la base de datos real
                    perfil = request.user.perfilusuario
                    perfil.saldo += monto
                    perfil.save() # Guarda el cambio para que se actualice en el panel admin
                    return JsonResponse({'creditos': float(perfil.saldo)})
                except (AttributeError, ObjectDoesNotExist):
                    return JsonResponse({'error': 'El usuario no tiene una billetera activa'}, status=400)
            else:
                return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def retirar_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            monto = float(data.get('monto', 0))
            if monto <= 0:
                return JsonResponse({'error': 'El monto debe ser mayor a 0'}, status=400)
            
            if request.user.is_authenticated:
                try:
                    # Descuenta directamente de la base de datos real
                    perfil = request.user.perfilusuario
                    if perfil.saldo < monto:
                        return JsonResponse({'error': 'Saldo insuficiente para el retiro'}, status=400)
                    perfil.saldo -= monto
                    perfil.save() # Guarda el cambio en el panel admin
                    return JsonResponse({'creditos': float(perfil.saldo)})
                except (AttributeError, ObjectDoesNotExist):
                    return JsonResponse({'error': 'El usuario no tiene una billetera activa'}, status=400)
            else:
                return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)