import os
import environ
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

THIRD_PARTY_APPS = [
    "rest_framework",
    # "rest_framework.authtoken",
    'rest_framework_simplejwt',
    "corsheaders",
    "colorfield",
]

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "caketables.apps.CaketablesConfig"
    # "accounts.apps.AccountsConfig",
    # "common.apps.CommonConfig",
]

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # 사이트 정보를 설정하기 위해 필요
    "allauth",
    "allauth.account",  # 가입한 계정을 관리하기 위한 것.
    "allauth.socialaccount",  # 소셜 계정을 관리하기 위한 것.
    "allauth.socialaccount.providers.kakao",
    # "allauth.socialaccount.providers.google",
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': "newcake",
        'USER': "newcake",
        'PASSWORD': "cake123!",
        'HOST': "pg-g4pkb.vpc-pub-cdb-kr.ntruss.com",
        'PORT': "5432",
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

DATE_INPUT_FORMATS = ["%Y-%m-%d"]

DATE_FORMAT = "F j"


USE_I18N = False

USE_TZ = False


AUTH_USER_MODEL = "users.User"


CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "jwt",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW = True


# 리액트와 연결 시 필요한 설정
CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3000"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:3000"]

# # 리액트와 도메인 연결 시 필요한 설정 (도메인 구매 후 이 부분 주석 해제)
# if DEBUG:
#     CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3000"]
#     CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:3000"]

# else:
#     CSRF_TRUSTED_ORIGINS = ["http://neokkukae.shop"]
#     CORS_ALLOWED_ORIGINS = ["http://neokkukae.shop"]


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "config.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


# # JWT settings
REST_USE_JWT = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # 토큰 유효 시간
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # 리프레시 토큰 유효 시간
    "ROTATE_REFRESH_TOKENS": False,  # 새로고침 토큰 사용 여부
    "BLACKLIST_AFTER_ROTATION": True,  # 블랙리스트 사용 여부
    "SIGNING_KEY": SECRET_KEY,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_CLAIM": "email",  # 사용자의 아이디 JWT 토큰에 저장할 필드
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.UntypedToken",),
    "TOKEN_TYPE_CLAIM": "token_type",  # 토큰 타입 필드
    "JTI_CLAIM": "jti",  # JWT ID 필드
    "TOKEN_USER_CLASS": "users.User",
}


ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
ACCOUNT_SESSION_REMEMBER = True
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
