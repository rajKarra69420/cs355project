import socket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import time, pickle, os, sys
import json
from encrypt_decrypt import encrypt, decrypt
from cryptography.hazmat.primitives import serialization

HOST = '127.0.0.1'
PORT = 65433
BOB_MESSAGE = b""
digest = hashes.Hash(hashes.SHA256())
#digest.update(BOB_MESSAGE)
bob_priv = ec.generate_private_key(ec.SECP384R1())
#get file contents
filename = sys.argv[1]
fileContents = open(filename, 'rb')
digest.update(fileContents.read())
fileHash = digest.finalize()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        alice_public = conn.recv(102400) #Receive alice's public key
        loaded_public_key = serialization.load_pem_public_key(alice_public)
        if not alice_public:
            exit()
        conn.sendall(bob_priv.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)) #Send over bob's public key
        bob_shared = bob_priv.exchange(ec.ECDH(), loaded_public_key)
        bob_hkdf = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'',).derive(bob_shared)
        iv, ciphertext, tag, associated_data = encrypt(bob_hkdf,fileHash,b"Bob's Hash")
        myCiphertext = ciphertext
        conn.send(pickle.dumps((iv,ciphertext,tag, associated_data)))
        (iv, ciphertext, tag, associated_data) = pickle.loads(conn.recv(102400))
        pText = decrypt(bob_hkdf, associated_data, iv, ciphertext,tag)
        isSame = b""
        if pText == fileHash:
            isSame = b"Success!"
        else:
            isSame = b"Failed!"
        
        iv, ciphertext, tag, associated_data = encrypt(bob_hkdf, isSame ,b"Bob's Result")
        conn.sendall(pickle.dumps((iv, ciphertext, tag, associated_data)))
        print("Our result: ", isSame.decode('utf-8'))
        (iv, ciphertext, tag, associated_data) = pickle.loads(conn.recv(102400))
        alice_result = decrypt(bob_hkdf, associated_data, iv, ciphertext, tag)
        print("Alice result:", alice_result.decode('utf-8'))

