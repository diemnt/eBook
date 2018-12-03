import base64

from Crypto.Cipher import AES

def encrypt(payload, salt, key):
    return AES.new(key, AES.MODE_CBC, salt).encrypt(r_pad(payload))


def decrypt(payload, salt, key, length):
    return AES.new(key, AES.MODE_CBC, salt).decrypt(payload)[:length]


def r_pad(payload, block_size=16):
    length = block_size - (len(payload) % block_size)
    return payload + chr(length) * length




import hashlib
secretKey = "1234567890"
m = hashlib.sha256()

# Get string and put into givenString.

m.update(givenString + secretKey)
m.digest()