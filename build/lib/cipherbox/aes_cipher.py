from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64
import os

def encrypt(data, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(data)

    return base64.b64encode(salt + cipher.nonce + tag + ct).decode()

def decrypt(data, password):
    raw = base64.b64decode(data)
    salt, nonce, tag, ct = raw[:16], raw[16:32], raw[32:48], raw[48:]

    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    return cipher.decrypt_and_verify(ct, tag)
