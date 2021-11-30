# Code Specifications

## Communication Channel

For our communication channel we used the python socket library. The python socket library provides access to the BSD socket interface and uses TCP/IP for communication. This channel by itself is an insecure and unauthenticated channel.

## Cryptography

We use python's crypography library (https://cryptography.io/en/latest/) and the cryptographic primitives in this library transfrom the communication channel mentioned above into a secure and authenticated channel. From this library we use the elliptic curve module to perform an Elliptic Curve Diffie Hellman key exchange. We choose to use the NIST P-384 curve in our code. We then use the HKDF class from this library to derive a key to be used with a symmteric cipher from the shared secret from the key exchange mentioned previously. We also use the hashes module from this library to use the sha256 hash function as both part of the HKDF and to hash the password file. Finally, we use the modes and algorithms modules and the Cipher class to use AES for symmetric encryption. We use the GCM mode of AES to provide both encryption and authentication of data.

