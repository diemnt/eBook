import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASES = {
    'default': {
        'NAME': 'ebook_dev',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'PASSWORD': 'tiendang',
        'HOST': 'localhost',
        'PORT': 5432
    }
}
MINIO_SERVER = "172.16.12.23:9000"
MINIO_ACCESSKEY = "ttx8h7pizqbwsyoaul03q0mx9"
MINIO_SECRET = "cjjdp7l2893a3btct4z6hej1c"
MINIO_BUCKET = "ebook"
MINIO_SECURE = False

print MINIO_SERVER
print "DATABASES ",DATABASES