from itertools import cycle
import base64




def _apply_xor(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ k for b, k in zip(data, cycle(key))])




def encrypt(plaintext: bytes, key: str) -> str:
    keyb = key.encode('utf-8')
    ct = _apply_xor(plaintext, keyb)
    return base64.b64encode(ct).decode('utf-8')




def decrypt(b64text: str, key: str) -> bytes:
    keyb = key.encode('utf-8')
    ct = base64.b64decode(b64text)
    pt = _apply_xor(ct, keyb)
    return pt