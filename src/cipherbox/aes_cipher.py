from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import base64


# Format output (base64-encoded): b"Salted__" + salt(16) + iv(16) + ciphertext
# We will prefix with a simple header 'CBX' to identify tool output.
HEADER = b'CBX'
SALT_SIZE = 16
IV_SIZE = 16
KEY_LEN = 32 # AES-256
PBKDF2_ITERS = 100_000




def _pad(data: bytes) -> bytes:
    pad_len = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([pad_len]) * pad_len




def _unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > AES.block_size:
        raise ValueError("Invalid padding")
    return data[:-pad_len]




def encrypt(plaintext: bytes, password: str) -> str:
    salt = get_random_bytes(SALT_SIZE)
    key = PBKDF2(password, salt, dkLen=KEY_LEN, count=PBKDF2_ITERS)
    iv = get_random_bytes(IV_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(_pad(plaintext))
    out = HEADER + salt + iv + ct
    return base64.b64encode(out).decode('utf-8')




def decrypt(b64cipher: str, password: str) -> bytes:
    data = base64.b64decode(b64cipher)
    if not data.startswith(HEADER):
        raise ValueError("Ciphertext not produced by CipherBox or header missing")
    data = data[len(HEADER):]
    salt = data[:SALT_SIZE]
    iv = data[SALT_SIZE:SALT_SIZE+IV_SIZE]
    ct = data[SALT_SIZE+IV_SIZE:]
    key = PBKDF2(password, salt, dkLen=KEY_LEN, count=PBKDF2_ITERS)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt_padded = cipher.decrypt(ct)
    return _unpad(pt_padded)