from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_message(message: str, password: str) -> str:
    key = generate_key(password)
    fernet = Fernet(key)
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message: str, password: str) -> str:
    try:
        key = generate_key(password)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_message.encode()).decode()
    except Exception:
        return "[Error] Incorrect password or corrupted data."
