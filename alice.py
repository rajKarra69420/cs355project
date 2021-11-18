from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import time, socket, pickle, os

from encrypt_decrypt import encrypt, decrypt

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
alice_priv = ec.generate_private_key(ec.SECP384R1(), default_backend())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) #Connect to the socket

    s.sendall(alice_priv.public_key()) #Send over alice's public key
    print("Set alice's public key! Receiving bob's public key now")
    bob_public = s.recv(1024)

    alice_shared = alice_priv.exchange(ec.ECDH(), bob_public)
    alice_hkdf = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'',).derive(alice_shared)
    #Now we can encrypt alice's message and send it over
    print("Sleeping for a bit!")
    time.sleep(5)
    iv, ciphertext, tag = encrypt(alice_hkdf,digest.finalize(),b"lol")
    conn.send(pickle.dumps((iv,ciphertext,tag)))
    (iv, ciphertext, tag) = pickle.loads(conn.recv(102400))
    print("Decrypting the received data")
    print(decrypt(alice_hkdf, b"lol", iv, ciphertext,tag))


