from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import time, socket, pickle, os, sys

from encrypt_decrypt import encrypt, decrypt
from cryptography.hazmat.primitives import serialization

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65433        # The port used by the server
alice_priv = ec.generate_private_key(ec.SECP384R1())

digest = hashes.Hash(hashes.SHA256())
filename = sys.argv[1]
fileContents = open(filename, 'rb')
fileStuff = fileContents.read()
digest.update(fileStuff)
fileHash = digest.finalize()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    s.connect((HOST, PORT))

    serialKey = alice_priv.public_key().public_bytes(encoding=serialization.Encoding.PEM,format=serialization.PublicFormat.SubjectPublicKeyInfo)
    s.sendall(serialKey)
    bob_public = s.recv(1024)
    loaded_public_key = serialization.load_pem_public_key(bob_public)
    alice_shared = alice_priv.exchange(ec.ECDH(), loaded_public_key)
    alice_hkdf = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=b'',).derive(alice_shared)
    
    iv, ciphertext, tag, associated_data = encrypt(alice_hkdf,fileHash,b"Alice's Hash")
    myCiphertext = ciphertext
    s.sendall(pickle.dumps((iv,ciphertext,tag, associated_data)))
    (iv, ciphertext, tag, associated_data) = pickle.loads(s.recv(102400))
    results = decrypt(alice_hkdf, associated_data, iv, ciphertext,tag)
    isSame = b""
    if results == fileHash:
        isSame = b"Success!"
    else:
        isSame = b"Failed!"

    iv, ciphertext, tag, associated_data = encrypt(alice_hkdf, isSame ,b"Alice's Result")
    s.sendall(pickle.dumps((iv, ciphertext, tag, associated_data)))
    print("Our result: ", isSame.decode('utf-8'))
    (iv, ciphertext, tag, associated_data) = pickle.loads(s.recv(102400))
    bob_result = decrypt(alice_hkdf, associated_data, iv, ciphertext, tag)
    print("Bob result:", bob_result.decode('utf-8'))
    
