from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

def generate_key():
    """Generate a secure random AES-256 key (base64-encoded)."""
    return base64.urlsafe_b64encode(os.urandom(32)).decode()

def encrypt_data(key: str, plaintext: str) -> str:
    key_bytes = base64.urlsafe_b64decode(key.encode())
    aesgcm = AESGCM(key_bytes)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return base64.urlsafe_b64encode(nonce + ciphertext).decode()

def decrypt_data(key: str, encrypted_data: str) -> str:
    key_bytes = base64.urlsafe_b64decode(key.encode())
    data = base64.urlsafe_b64decode(encrypted_data.encode())
    nonce = data[:12]
    ciphertext = data[12:]
    aesgcm = AESGCM(key_bytes)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()