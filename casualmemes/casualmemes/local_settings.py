# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "casualmemes",
        "HOST": "localhost",
        "PASSWORD": "coderslab",
        "USER": "postgres",
        "PORT": 5432,
    }
}
