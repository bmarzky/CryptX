import base64

def encrypt(data):
    return base64.b64encode(data).decode()

def decrypt(text):
    return base64.b64decode(text).decode()
