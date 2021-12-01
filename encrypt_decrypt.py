import os
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

def encrypt(key, message, associated_data):
    iv = os.urandom(12)
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv),).encryptor()
    encryptor.authenticate_additional_data(associated_data)
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return (iv, ciphertext, encryptor.tag, associated_data)

def decrypt(key, associated_data, iv, ciphertext, tag):
    try:
        decryptor = Cipher(algorithms.AES(key),modes.GCM(iv, tag),).decryptor()
        decryptor.authenticate_additional_data(associated_data)
        return decryptor.update(ciphertext) + decryptor.finalize()
    except:
        return None
