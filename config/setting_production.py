import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEBUG = False

DATABASES = {
    'default': {
        'NAME': 'ebook_db',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '172.16.12.27',
        'PORT': 5432,
        'USER': 'postgres',
        'PASSWORD': 'postgres'
    }

}

# Default Email Contact
SYSTEM_ADMIN_CINEMA_EMAIL = "ngochang@khoiphat.vn, khaivo@metiz.vn, lamnguyen@helio.vn"
SYSTEM_ADMIN_CINEMA_EMAIL_CC = ["vietthang@khoiphat.vn", "nguyenhien@helio.vn"]
POS_ADMIN_EMAIL = "vietthang@khoiphat.vn, khaivo@metiz.vn"

SYSTEM_ADMIN_CINEMA_PHONE = ""
DEFAULT_TO_ADMIN_EMAIL = "contact@metiz.vn"

# VNPAY CONFIG
VNPAY_RETURN_URL = 'http://metiz.vn/payment_return'  # get from config
VNPAY_PAYMENT_URL = 'http://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # get from config
VNPAY_API_URL = 'http://sandbox.vnpayment.vn/merchant_webapi/merchant.html'
VNPAY_TMN_CODE = 'HELIOKP1'  # Website ID in VNPAY System, get from config
VNPAY_HASH_SECRET_KEY = 'YTDBTUZONRERICMBLYIRTRTEJDPCZDFK'  # Secret key for create checksum,get from config


# POS Cinestar config
CINESTAR_SERECT_KEY = '5ba90f1cc2d540edbb01e3ffc85bc7f2'
BASE_URL_CINESTAR = 'http://113.176.107.20:8080/helio.asmx'

# SMS Config
SMS_BRAND = "MetizCinema"
SMS_USER = "metizcinema"
SMS_PASSWORD = "metizcinema123"
SMS_KEY = "VNFPT123BLUESEA1"
SMS_KEY_IV = "154dxc1scfzzad21"
SMS_URL = "http://ws.ctnet.vn/servicectnet.asmx?op=sendsms"

FB_APP_ID = '328570110956197'

RECAPTCHA_PUBLIC_KEY = '6LfW2zoUAAAAAANgpuK2Yw5-z7P8S6TeODY2qNsS'
RECAPTCHA_PRIVATE_KEY = '6LfW2zoUAAAAANhdyvbJnq9Hg4jxOFKFR3T2yU9A'


# POS API config
AUTH_PREFIX = "Bearer "
BASE_URL_POS_API = #"http://127.0.0.1:8009/api/"
POS_API_TOKEN = #"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImRpZW1uZ3V5ZW5Adm9vYy52biIsIm9yaWdfaWF0IjoxNTI4MTY5NjU5LCJ1c2VyX2lkIjoxLCJlbWFpbCI6ImRpZW1uZ3V5ZW5Adm9vYy52biIsImV4cCI6MTUyODE2OTk1OX0.lA1TK_OAQSMN-wpXK4ej0lCchbEC8eqNZaHswFrvsTo"
POS_API_AUTH_HEADER = AUTH_PREFIX + POS_API_TOKEN