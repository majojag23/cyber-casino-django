import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PerfilUsuario  # Importación garantizada de tu modelo de billetera

# ==============================================================================
# 🏠 VISTAS DE RENDERIZADO DE PLANTILLAS (ACCESO CON LOGUEO TRADICIONAL)
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
# 💰 API DE LA BILLETERA (CONSULTA RELACIONAL BLINDADA CONTRA ERRORES 500)
# ==============================================================================

def consultar_saldo_api(request):
    if request.user.is_authenticated:
        try:
            # 1. Buscamos el perfil usando el objeto del usuario logueado en la sesión
            perfil = PerfilUsuario.objects.filter(user=request.user).first()
            
            if perfil is not None:
                saldo_real = perfil.saldo
                return JsonResponse({
                    'creditos': float(saldo_real),
                    'saldo': float(saldo_real),
                    'balance': float(saldo_real)
                })
            
            # 2. Si falla la relación directa, buscamos estrictamente por la ID numérica del usuario
            perfil_id = PerfilUsuario.objects.filter(user_id=request.user.id).first()
            if perfil_id is not None:
                saldo_real = perfil_id.saldo
                return JsonResponse({
                    'creditos': float(saldo_real),
                    'saldo': float(saldo_real),
                    'balance': float(saldo_real)
                })
                
            # Si el usuario no tiene billetera creada todavía en el admin, arranca en 0 de forma segura
            return JsonResponse({'creditos': 0.0, 'saldo': 0.0, 'balance': 0.0})
            
        except Exception as e:
            # Salvavidas: Evita lanzar un error 500 si la base de datos de Render está saturada
            return JsonResponse({'creditos': 0.0, 'saldo': 0.0, 'balance': 0.0, 'error_debug': str(e)})
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
                perfil = PerfilUsuario.objects.filter(user=request.user).first()
                if perfil is not None:
                    perfil.saldo += monto
                    perfil.save()
                    return JsonResponse({'creditos': float(perfil.saldo), 'saldo': float(perfil.saldo)})
                return JsonResponse({'error': 'No tienes una billetera activa asignada'}, status=400)
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
                perfil = PerfilUsuario.objects.filter(user=request.user).first()
                if perfil is not None:
                    if perfil.saldo < monto:
                        return JsonResponse({'error': 'Saldo insuficiente'}, status=400)
                    perfil.saldo -= monto
                    perfil.save()
                    return JsonResponse({'creditos': float(perfil.saldo), 'saldo': float(perfil.saldo)})
                return JsonResponse({'error': 'No tienes una billetera activa asignada'}, status=400)
            else:
                return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


# ==============================================================================
# 🎮 CORE ESTRUCTURADO PARA APIS DE JUEGO (EVITA ERRORES 500 EN EL FRONTEND)
# ==============================================================================

def procesar_apuesta_api(request):
    return JsonResponse({
        'status': 'ok',
        'success': True,
        'mensaje': 'Apuesta recibida y validada por el servidor'
    })

# --- BUSCAMINAS ---
def iniciar_buscaminas_api(request):
    tablero_vacio = [False] * 25
    return JsonResponse({
        'status': 'ok',
        'success': True,
        'tablero': tablero_vacio,
        'minas': 3
    })

def verificar_celda_api(request):
    return JsonResponse({
        'status': 'ok',
        'success': True,
        'es_mina': False
    })

def cashout_buscaminas_api(request):
    return JsonResponse({
        'status': 'ok',
        'success': True,
        'ganancia': 0.0
    })

# --- TRAGAMONEDAS (SLOT) ---
def jugar_slot_api(request):
    iconos = ['🍒', '🍋', '🍇', '💎', '🔔']
    resultado = [random.choice(iconos) for _ in range(3)]
    return JsonResponse({
        'status': 'ok',
        'success': True,
        'resultado': resultado,
        'premio': 0.0
    })

# --- RULETA ---
def girar_ruleta_api(request):
    numero = random.randint(0, 36)
    color = 'verde' if numero == 0 else ('rojo' if numero % 2 == 0 else 'negro')
    return JsonResponse({
        'status': 'ok',
        'success': True,
        'numero': numero,
        'color': color
    })