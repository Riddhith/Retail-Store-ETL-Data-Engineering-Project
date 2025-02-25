# import base64
# from Cryptodome.Cipher import AES
# from Cryptodome.Protocol.KDF import PBKDF2
# import os, sys
# from resources.dev import config
# from logging_config import logger

# try:
#     key = config.key
#     iv = config.iv
#     salt = config.salt
#
#     if not (key and iv and salt):
#         raise Exception(F"Error while fetching details for key/iv/salt")
# except Exception as e:
#     print(f"Error occured. Details : {e}")
#     # logger.error("Error occurred. Details: %s", e)
#     sys.exit(0)
#
# BS = 16
# pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
# unpad = lambda s: s[0:-ord(s[-1:])]
#
# def get_private_key():
#     Salt = salt.encode('utf-8')
#     kdf = PBKDF2(key, Salt, 64, 1000)
#     key32 = kdf[:32]
#     return key32
#
#
# def encrypt(raw):
#     raw = pad(raw)
#     cipher = AES.new(get_private_key(), AES.MODE_CBC, iv.encode('utf-8'))
#     return base64.b64encode(cipher.encrypt(raw))
#
#
# def decrypt(enc):
#     cipher = AES.new(get_private_key(), AES.MODE_CBC, iv.encode('utf-8'))
#     return unpad(cipher.decrypt(base64.b64decode(enc))).decode('utf8')

import base64
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Util.Padding import pad, unpad
import os, sys
from resources.dev import config

try:
    key = config.key
    iv = config.iv[:16].encode('utf-8')
    salt = config.salt

    if not (key and iv and salt):
        raise Exception("Error while fetching details for key/iv/salt")
except Exception as e:
    print(f"Error occurred. Details: {e}")
    sys.exit(0)


def get_private_key():
    Salt = salt.encode('utf-8')
    kdf = PBKDF2(key, Salt, 64, 1000)
    key32 = kdf[:32]
    return key32


def encrypt(raw):
    raw = pad(raw.encode('utf-8'), AES.block_size)
    cipher = AES.new(get_private_key(), AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(raw)).decode('utf-8')


def decrypt(enc):
    cipher = AES.new(get_private_key(), AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(base64.b64decode(enc))
    return unpad(decrypted, AES.block_size).decode('utf-8')

print(encrypt([your aws_access_key]))
print(decrypt([your encrypted_aws_access_key]))
print(encrypt([your aws_secret_key]))
print(decrypt([your encrypted_aws_secret_key])