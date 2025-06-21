from PIL import Image
from crypto_utils import encrypt_message, decrypt_message

def encode_message(image: Image.Image, message: str, password: str) -> Image.Image:
    encrypted_message = encrypt_message(message, password)
    binary_message = ''.join([format(ord(char), '08b') for char in encrypted_message]) + '1111111111111110'
    img = image.copy()
    pixels = img.load()

    idx = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if idx >= len(binary_message):
                return img
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(binary_message[idx])
            idx += 1
            if idx < len(binary_message):
                g = (g & ~1) | int(binary_message[idx])
                idx += 1
            if idx < len(binary_message):
                b = (b & ~1) | int(binary_message[idx])
                idx += 1
            pixels[x, y] = (r, g, b)
    return img

def decode_message(image: Image.Image, password: str) -> str:
    pixels = image.load()
    binary_data = ''
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    encrypted_message = ''
    for byte in all_bytes:
        if byte == '11111110':
            break
        encrypted_message += chr(int(byte, 2))
    
    return decrypt_message(encrypted_message, password)
