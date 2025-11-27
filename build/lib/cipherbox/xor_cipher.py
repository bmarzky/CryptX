def encrypt(data: bytes, key: str) -> str:
    key_bytes = key.encode("utf-8")
    out = bytearray()

    for i, b in enumerate(data):
        out.append(b ^ key_bytes[i % len(key_bytes)])

    # hasil XOR → ubah ke hex string supaya aman disimpan
    return out.hex()


def decrypt(hex_string: str, key: str) -> bytes:
    key_bytes = key.encode("utf-8")
    data = bytes.fromhex(hex_string)
    out = bytearray()

    for i, b in enumerate(data):
        out.append(b ^ key_bytes[i % len(key_bytes)])

    return bytes(out)
