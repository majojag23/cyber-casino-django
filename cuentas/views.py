from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import FormularioRegistroVIP

# Vista para registrar nuevos jugadores
def registro(request):
    if request.method == 'POST':
        formulario = FormularioRegistroVIP(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            # Inicia sesión automáticamente al registrarse
            login(request, usuario)
            return redirect('home') # <-- ¡Aquí usamos el nombre interno de Django!
    else:
        formulario = FormularioRegistroVIP()
    
    return render(request, 'cuentas/registro.html', {'formulario': formulario})

# Vista para iniciar sesión
def iniciar_sesion(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            return redirect('home') # <-- ¡Y aquí también!
    else:
        formulario = AuthenticationForm()
    
    return render(request, 'cuentas/login.html', {'formulario': formulario})

# Vista para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')