import socket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import time, pickle, os

from encrypt_decrypt import encrypt, decrypt

HOST = '127.0.0.1'
PORT = 65432
BOB_MESSAGE = ""
digest = hashes.Hash(hashes.SHA256())
digest.update(BOB_MESSAGE)
bob_priv = ec.generate_private_key(ec.SECP384R1())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print ('Connected by', addr)
        while True:
            alice_public = conn.recv(102400) #Receive alice's public key
            if not alice_public:
                break
            print("Received alice's public key! Sending bob's public key over")
            conn.sendall(bob.public_key()) #Send over bob's public key
            bob_shared = bob_priv.exchange(ec.ECDH(), alice_public)
            bob_hkdf = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'',).derive(bob_shared)
            #Now we can encrypt bob's message and send it over
            time.sleep(5)
            iv, ciphertext, tag = encrypt(bob_hkdf,digest.finalize(),b"lol")
            conn.send(pickle.dumps((iv,ciphertext,tag)))
            (iv, ciphertext, tag) = pickle.loads(conn.recv(102400))
            print("Decrypting the received data")
            print(decrypt(bob_hkdf, b"lol", iv, ciphertext,tag))