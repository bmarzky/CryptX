import base64




def encrypt(plaintext: bytes) -> str:
    return base64.b64encode(plaintext).decode('utf-8')




def decrypt(b64text: str) -> bytes:
    return base64.b64decode(b64text)