from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
import os

bob_priv = ec.generate_private_key(ec.SECP384R1())
alice_priv = ec.generate_private_key(ec.SECP384R1())

bob_shared = bob_priv.exchange(ec.ECDH(), alice_priv.public_key())

bob_hkdf = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'',).derive(bob_shared)

alice_shared = alice_priv.exchange(ec.ECDH(), bob_priv.public_key())

alice_hkdf = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'',).derive(alice_shared)

assert(bob_hkdf == alice_hkdf)

alice_text = b"Hello"
bob_text = b"Hello"

def encrypt(key, message, associated_data):
    iv = os.urandom(12)
    encryptor = Cipher(algorithms.AES(key), modes.GCM(iv),).encryptor()
    encryptor.authenticate_additional_data(associated_data)
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return (iv, ciphertext, encryptor.tag)

def decrypt(key, associated_data, iv, ciphertext, tag):
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
    ).decryptor()
    decryptor.authenticate_additional_data(associated_data)
    return decryptor.update(ciphertext) + decryptor.finalize()

iv, ciphertext, tag = encrypt(bob_hkdf,bob_text,b"lol")

print(decrypt(bob_hkdf, b"lol", iv, ciphertext,tag))


