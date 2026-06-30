import os
from pathlib import Path

# 1. RUTAS BASE
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. CONFIGURACIÓN DE DESARROLLO
SECRET_KEY = 'django-insecure-casino-royal-key-pruebas-locales'
DEBUG = True
ALLOWED_HOSTS = ['*']

# 3. APLICACIONES INSTALADAS (Tu app original 'usuarios')
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'royal_casino.usuarios',  # 👈 ¡Le agregamos 'royal_casino.' antes de usuarios!
]

# 4. MIDDLEWARES
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- VERIFICA ESTA LÍNEA EXACTA
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'miproyecto.urls'

# 5. EL BUSCADOR DE PLANTILLAS CORREGIDO
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'royal_casino', 'usuarios', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'miproyecto.wsgi.application'

# 6. BASE DE DATOS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. IDIOMA Y HORARIOS
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 8. ARCHIVOS ESTÁTICOS
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 🔑 EVITA EL ERROR DE REDIRECCIÓN CUANDO NO HAY LOGINS ACTIVOS
LOGIN_URL = '/'

# 👥 CONFIGURACIÓN DEL MODELO DE JUGADOR PERSONALIZADO
AUTH_USER_MODEL = 'usuarios.Jugador'