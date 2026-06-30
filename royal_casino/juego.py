import pygame
import sys
import random
import os
import math
import array
import requests

os.environ['SDL_VIDEODRIVER'] = 'windib'

# =========================================================================
# 🔌 CONFIGURACIÓN DE CONEXIÓN CON EL SERVIDOR DE DJANGO
# =========================================================================
URL_BASE_API = "http://127.0.0.1:8000/api/"

# Pon aquí el usuario y contraseña que recuperaste o creaste en tu base de datos
USUARIO_WEB = "Mariana_prueba2"  
CONTRASENA_WEB = "Mariana_prueba2"  

sesion_web = requests.Session()
sesion_web.auth = (USUARIO_WEB, CONTRASENA_WEB)

def obtener_saldo_de_la_nube():
    try:
        respuesta = sesion_web.get(f"{URL_BASE_API}saldo/", timeout=3)
        if respuesta.status_code == 200:
            return float(respuesta.json()['creditos'])
    except:
        pass
    print("⚠️ Servidor web desconectado. Usando billetera de respaldo.")
    return 500.0

def reportar_giro_a_la_nube(apuesta_monto, ganancia_monto):
    try:
        datos = {'apuesta': apuesta_monto, 'ganancia': ganancia_monto}
        respuesta = sesion_web.post(f"{URL_BASE_API}apuesta/", json=datos, timeout=3)
        if respuesta.status_code == 200:
            return float(respuesta.json()['nuevo_saldo'])
    except:
        pass
    return None

# =========================================================================
# 🕹️ MOTOR GRÁFICO ULTRA FLUIDO DE PYGAME
# =========================================================================
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2)

ANCHO, ALTO = 950, 680
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("👑 MARIANA'S ROYAL CASINO: LIVE WEB CONNECT 👑")
reloj = pygame.time.Clock()

fuente_titulo = pygame.font.Font(None, 52)
fuente_hud = pygame.font.Font(None, 36)

FONDO_NORMAL = (10, 4, 15)       
FONDO_BONUS = (60, 8, 30)       
COLOR_ORO = (255, 215, 0)        
COLOR_ORO_SOMBRA = (120, 85, 0)  
COLOR_BOTON = (46, 204, 113)     
COLOR_WIN_NEON = (0, 255, 255)   

def generar_audio(tipo):
    duracion = 0.08 if tipo == "freno" else 0.5
    frec_base = 140 if tipo == "freno" else 523
    num_muestras = int(22050 * duracion)
    datos = array.array('h', [0] * num_muestras)
    for i in range(num_muestras):
        t = float(i) / 22050
        frecuencia = frec_base + (int(t * 30) * 50) if tipo == "ganar" else frec_base
        if math.sin(2 * math.pi * frecuencia * t) > 0: datos[i] = 4000
        else: datos[i] = -4000
    return pygame.mixer.Sound(buffer=datos)

snd_freno = generar_audio("freno")
snd_ganar = generar_audio("ganar")

# --- CARGA DE TEXTURAS DESDE RAM ---
SPRITES_ORIGINALES = {}
NOMBRES_POSIBLES = {
    0: ["cereza.png", "cereza.PNG", "cereza.png.png"],
    1: ["limon.png", "limon.PNG", "limon.png.png"],
    2: ["naranja.png", "naranja.PNG", "naranja.png.png"],
    3: ["sandia.png", "sandia.PNG", "sandia.png.png"],
    4: ["siete.png", "siete.PNG", "siete.png.png"],
    5: ["diamante.png", "diamante.PNG", "diamante.png.png"]
}

directorio_del_codigo = os.path.dirname(os.path.abspath(__file__))
ruta_imagenes_real = os.path.join(directorio_del_codigo, "imagenes")

for id_tipo, lista_nombres in NOMBRES_POSIBLES.items():
    cargada = False
    for nombre in lista_nombres:
        ruta_completa = os.path.join(ruta_imagenes_real, nombre)
        if os.path.exists(ruta_completa):
            try:
                img = pygame.image.load(ruta_completa).convert_alpha()
                SPRITES_ORIGINALES[id_tipo] = pygame.transform.smoothscale(img, (120, 120))
                cargada = True
                break
            except: pass
    if not cargada:
        superficie_respaldo = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.circle(superficie_respaldo, (230, 40, 120, 200), (60, 60), 50)
        SPRITES_ORIGINALES[id_tipo] = superficie_respaldo

CACHE_3D = {id_tipo: {} for id_tipo in range(6)}
ALTO_VENTANA_RODILLO = 290
ALTO_CASILLA = 96
centro_y_ventana = ALTO_VENTANA_RODILLO / 2

print("⚡ Conectando cilindros gráficos a la red... Por favor espera.")
for y_pos in range(-100, 400):
    distancia_al_centro = abs((y_pos + ALTO_CASILLA/2) - centro_y_ventana)
    factor_3d = math.cos((distancia_al_centro / centro_y_ventana) * (math.pi / 2.4))
    factor_3d = max(0.25, min(1.0, factor_3d))
    ancho_dinamico = max(4, int(75 * factor_3d))
    alto_dinamico = max(4, int(75 * factor_3d))
    
    for id_fruta, img_base in SPRITES_ORIGINALES.items():
        sprite_escalado = pygame.transform.scale(img_base, (ancho_dinamico, alto_dinamico)) # <-- ¡AQUÍ ESTÁ LA CORRECCIÓN!
        if factor_3d < 0.85:
            capa_oscuridad = pygame.Surface((sprite_escalado.get_width(), sprite_escalado.get_height()), pygame.SRCALPHA)
            capa_oscuridad.fill((0, 0, 0, min(180, int(255 * (1.0 - factor_3d)))))
            sprite_escalado.blit(capa_oscuridad, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        CACHE_3D[id_fruta][y_pos] = sprite_escalado

LINEAS_DE_PAGO = [
    (1, 1, 1), (0, 0, 0), (2, 2, 2), (0, 1, 2), (2, 1, 0),
    (0, 0, 1), (2, 2, 1), (0, 1, 1), (2, 1, 1), (1, 0, 0),
    (1, 2, 2), (1, 0, 1), (1, 2, 1), (0, 2, 0), (2, 0, 2),
    (0, 2, 1), (2, 0, 1), (1, 1, 0), (1, 1, 2), (0, 0, 2)
]

X_RODILLOS = [240, 410, 580]
ANCHO_RODILLO = 130
Y_VENTANA_RODILLO = 170

tablero = [[random.randint(0, 5) for _ in range(3)] for _ in range(3)]
velocidades_rodillos = [0.0, 0.0, 0.0]
posiciones_y_rodillos = [0.0, 0.0, 0.0] 
estado_giro = [0, 0, 0] 
tiras_ocultas = [[random.randint(0, 5) for _ in range(100)] for _ in range(3)]

# --- BILLETERA REAL CONECTADA ---
creditos = obtener_saldo_de_la_nube()
apuesta = 20 
modo_bonus_activo = False
giros_gratis_restantes = 0
esta_girando = False
tiempo_maquina = 0
mensaje_premio = "BILLETERA DE DJANGO SINCRONIZADA CON EXITO"
color_mensaje = (255, 255, 255)

coordenadas_ganadoras = set()
particulas_monedas = []     
intensidad_sacudida = 0     
ganancia_ultimo_giro = 0  

def crear_explosion_monedas(cantidad):
    for _ in range(cantidad):
        particulas_monedas.append({
            "x": ANCHO // 2 + random.randint(-60, 60), "y": ALTO // 2,
            "vx": random.uniform(-6, 6), "vy": random.uniform(-10, -3),
            "radio": random.randint(6, 10), "vida": random.randint(50, 90)
        })

def calcular_matematica_giro():
    global ganancia_ultimo_giro, modo_bonus_activo, giros_gratis_restantes, intensidad_sacudida, mensaje_premio, color_mensaje, creditos
    ganancia_ultimo_giro = 0
    multiplicador = 5 if modo_bonus_activo else 1

    scatters_totales = sum(fila.count(5) for fila in tablero)
    if scatters_totales >= 3 and not modo_bonus_activo:
        modo_bonus_activo = True
        giros_gratis_restantes = 5
        mensaje_premio = "🔥 ¡SUPER BONUS ACTIVADO! 5 FREE SPINS (X5) 🔥"
        color_mensaje = COLOR_ORO
        intensidad_sacudida = 25
        crear_explosion_monedas(80)
        nuevo_saldo = reportar_giro_a_la_nube(0, 0)
        if nuevo_saldo is not None: creditos = nuevo_saldo
        snd_ganar.play()
        return

    for f1, f2, f3 in LINEAS_DE_PAGO:
        if tablero[f1][0] == tablero[f2][1] == tablero[f3][2]:
            coordenadas_ganadoras.update([(f1, 0), (f2, 1), (f3, 2)])
            ganancia_ultimo_giro += (apuesta // 2) * (tablero[f1][0] + 2) * multiplicador

    costo_giro = 0 if (modo_bonus_activo or giros_gratis_restantes > 0) else apuesta
    nuevo_saldo = reportar_giro_a_la_nube(costo_giro, ganancia_ultimo_giro)
    
    if nuevo_saldo is not None:
        creditos = nuevo_saldo  
    else:
        creditos = creditos - costo_giro + ganancia_ultimo_giro

    if ganancia_ultimo_giro > 0:
        mensaje_premio = f"💥 WIN EN NUBE!! +${ganancia_ultimo_giro} 💥"
        color_mensaje = COLOR_ORO if not modo_bonus_activo else (255, 80, 80)
        intensidad_sacudida = 12 if ganancia_ultimo_giro > 100 else 6
        crear_explosion_monedas(min(60, int(ganancia_ultimo_giro // 2)))
        snd_ganar.play()
    else:
        if modo_bonus_activo:
            mensaje_premio = f"MODO BONUS RUN: {giros_gratis_restantes} FREE SPINS"
            color_mensaje = COLOR_ORO
        else:
            mensaje_premio = "SUERTE EN TU PRÓXIMO GIRO"
            color_mensaje = (200, 200, 200)

    if modo_bonus_activo and giros_gratis_restantes <= 0:
        modo_bonus_activo = False

# --- BUCLE PRINCIPAL ---
while True:
    tiempo_maquina += 1
    desfase_shake_x = 0
    desfase_shake_y = 0
    if intensidad_sacudida > 0:
        desfase_shake_x = random.randint(-int(intensidad_sacudida), int(intensidad_sacudida))
        desfase_shake_y = random.randint(-int(intensidad_sacudida), int(intensidad_sacudida))
        intensidad_sacudida -= 0.6

    superficie_fondo = pygame.Surface((ANCHO, ALTO))
    superficie_fondo.fill(FONDO_BONUS if modo_bonus_activo else FONDO_NORMAL)
    pos_mouse = pygame.mouse.get_pos()

    for i in range(3):
        if estado_giro[i] > 0:
            posiciones_y_rodillos[i] += velocidades_rodillos[i]
            if posiciones_y_rodillos[i] >= ALTO_CASILLA:
                posiciones_y_rodillos[i] -= ALTO_CASILLA
                tablero[2][i] = tablero[1][i]
                tablero[1][i] = tablero[0][i]
                tablero[0][i] = tiras_ocultas[i].pop(0)
                tiras_ocultas[i].append(random.randint(0, 5))
        
        if estado_giro[i] == 2:
            velocidades_rodillos[i] -= 0.5
            if velocidades_rodillos[i] <= 4:
                velocidades_rodillos[i] = 0
                posiciones_y_rodillos[i] = 0
                estado_giro[i] = 0
                snd_freno.play()
                if i == 2:
                    esta_girando = False
                    calcular_matematica_giro()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            rect_boton = pygame.Rect(400 + desfase_shake_x, 495 + desfase_shake_y, 150, 55)
            if rect_boton.collidepoint(pos_mouse) and not esta_girando:
                
                costo_giro = 0 if modo_bonus_activo else apuesta
                if (modo_bonus_activo and giros_gratis_restantes > 0) or creditos >= costo_giro:
                    if modo_bonus_activo: giros_gratis_restantes -= 1
                    
                    esta_girando = True
                    coordenadas_ganadoras.clear()
                    mensaje_premio = "¡TRANSMITIENDO TRANSACCIÓN WEB EN VIVO!"
                    for r in range(3):
                        velocidades_rodillos[r] = 24.0
                        estado_giro[r] = 1
                    pygame.time.set_timer(pygame.USEREVENT + 1, 900)
                    pygame.time.set_timer(pygame.USEREVENT + 2, 1500)
                    pygame.time.set_timer(pygame.USEREVENT + 3, 2100)

        if evento.type == pygame.USEREVENT + 1: estado_giro[0] = 2; pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        if evento.type == pygame.USEREVENT + 2: estado_giro[1] = 2; pygame.time.set_timer(pygame.USEREVENT + 2, 0)
        if evento.type == pygame.USEREVENT + 3: estado_giro[2] = 2; pygame.time.set_timer(pygame.USEREVENT + 3, 0)

    # Dibujar gabinete
    borde_gabinete = COLOR_ORO if not modo_bonus_activo else (255, 60, 110)
    pygame.draw.rect(superficie_fondo, (5, 2, 8), (195, 145, 560, 330), border_radius=20) 
    pygame.draw.rect(superficie_fondo, COLOR_ORO_SOMBRA if not modo_bonus_activo else (140, 20, 50), (200, 140, 550, 325), 12, border_radius=18) 
    pygame.draw.rect(superficie_fondo, borde_gabinete, (208, 148, 534, 309), 4, border_radius=12) 
    pygame.draw.rect(superficie_fondo, (22, 13, 30), (212, 152, 526, 301), border_radius=10) 

    # Renderizado desde Caché
    for i, x_pos in enumerate(X_RODILLOS):
        caja_rodillo = pygame.Surface((ANCHO_RODILLO, ALTO_VENTANA_RODILLO))
        caja_rodillo.fill((242, 242, 248)) 
        offset_y = int(posiciones_y_rodillos[i])
        for fila in range(4):
            y_pos_fruta = (fila - 1) * ALTO_CASILLA + offset_y + 5
            idx_fila = max(0, min(2, fila - 1))
            id_fruta = tablero[idx_fila][i]
            y_clave = max(-100, min(399, int(y_pos_fruta)))
            sprite_final = CACHE_3D[id_fruta][y_clave]
            
            if (idx_fila, i) in coordenadas_ganadoras and not esta_girando:
                pulsacion = int(math.sin(tiempo_maquina * 0.25) * 5)
                if pulsacion != 0:
                    sprite_final = pygame.transform.scale(sprite_final, (max(4, sprite_final.get_width() + pulsacion), max(4, sprite_final.get_height() + pulsacion)))

            x_centrada = (ANCHO_RODILLO - sprite_final.get_width()) // 2
            y_centrada = y_pos_fruta + (ALTO_CASILLA - sprite_final.get_height()) // 2
            caja_rodillo.blit(sprite_final, (x_centrada, int(y_centrada)))

        for s_y in range(32):
            alfa = int(255 * (1.0 - (s_y / 32.0)))
            sombra_barra = pygame.Surface((ANCHO_RODILLO, 1), pygame.SRCALPHA)
            sombra_barra.fill((0, 0, 0, alfa))
            caja_rodillo.blit(sombra_barra, (0, s_y))
            caja_rodillo.blit(sombra_barra, (0, ALTO_VENTANA_RODILLO - 1 - s_y))

        pygame.draw.rect(caja_rodillo, (85, 75, 95), (0, 0, ANCHO_RODILLO, ALTO_VENTANA_RODILLO), 4, border_radius=4)
        superficie_fondo.blit(caja_rodillo, (x_pos, Y_VENTANA_RODILLO))

    if not esta_girando:
        for f, c in coordenadas_ganadoras:
            posX = X_RODILLOS[c]
            posY = Y_VENTANA_RODILLO + (f * ALTO_CASILLA)
            pygame.draw.rect(superficie_fondo, COLOR_WIN_NEON, (posX, posY, ANCHO_RODILLO, ALTO_CASILLA), 4, border_radius=8)

    for p in particulas_monedas[:]:
        p["x"] += p["vx"]; p["y"] += p["vy"]; p["vy"] += 0.45; p["vida"] -= 1
        if p["y"] >= ALTO - 40:
            p["y"] = ALTO - 40; p["vy"] = -p["vy"] * 0.6; p["vx"] *= 0.8
        pygame.draw.circle(superficie_fondo, COLOR_ORO, (int(p["x"]), int(p["y"])), p["radio"])
        if p["vida"] <= 0: particulas_monedas.remove(p)

    # Botón SPIN
    rect_boton = pygame.Rect(400, 495, 150, 55)
    color_btn = (70, 90, 80) if esta_girando else (COLOR_BOTON if not modo_bonus_activo else (255, 65, 65))
    pygame.draw.rect(superficie_fondo, color_btn, rect_boton, border_radius=15)
    
    label_btn = "SPIN!" if not modo_bonus_activo else f"FREE: {giros_gratis_restantes}"
    txt_spin = fuente_hud.render(label_btn, True, (255, 255, 255))
    superficie_fondo.blit(txt_spin, (rect_boton.x + (150 - txt_spin.get_width())//2, rect_boton.y + 14))

    # HUD LIVE
    titulo_texto = "👑 LIVE CASINO CONNECT PRO 👑" if not modo_bonus_activo else "🔥 LIVE BONUS MULTIPLIER X5 🔥"
    txt_titulo = fuente_titulo.render(titulo_texto, True, COLOR_ORO)
    txt_creditos = fuente_hud.render(f"WEB WALLET: ${creditos:.2f}", True, (46, 204, 113))
    
    bet_label = f"BET: ${apuesta}" if not modo_bonus_activo else "BONUS ACTIVE: MULTI X5"
    txt_bet = fuente_hud.render(bet_label, True, (230, 126, 34))
    txt_msg = fuente_hud.render(mensaje_premio, True, color_mensaje)

    superficie_fondo.blit(txt_titulo, (ANCHO // 2 - txt_titulo.get_width() // 2, 45))
    superficie_fondo.blit(txt_creditos, (240, 110))
    superficie_fondo.blit(txt_bet, (ANCHO - 380, 110))
    superficie_fondo.blit(txt_msg, (ANCHO // 2 - txt_msg.get_width() // 2, 580))

    pantalla.fill((0, 0, 0))
    pantalla.blit(superficie_fondo, (desfase_shake_x, desfase_shake_y))
    pygame.display.flip()
    reloj.tick(60)