import socket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import time, pickle, os, sys

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
        print ('Connected by', addr)
        while True:
            alice_public = conn.recv(102400) #Receive alice's public key
            print(alice_public)
            loaded_public_key = serialization.load_pem_public_key(alice_public)
            if not alice_public:
                break
            print("Received alice's public key! Sending bob's public key over")
            conn.sendall(bob_priv.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)) #Send over bob's public key
            bob_shared = bob_priv.exchange(ec.ECDH(), loaded_public_key)
            bob_hkdf = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'',).derive(bob_shared)
            print(bob_hkdf)
            #Now we can encrypt bob's message and send it over
            time.sleep(5)
            iv, ciphertext, tag = encrypt(bob_hkdf,fileHash,b"lol")
            myCiphertext = ciphertext
            print("ctext", myCiphertext)
            conn.send(pickle.dumps((iv,ciphertext,tag)))
            (iv, ciphertext, tag) = pickle.loads(conn.recv(102400))
            conn.close()
            print("Decrypting the received data")
            pText = decrypt(bob_hkdf, b"lol", iv, ciphertext,tag)
            print(pText)
            print(fileHash)
            if pText == fileHash:
                print("Success!")
            else:
                print("Failed!")
