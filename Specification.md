# CS 355 Team 8

Github URL: https://github.com/rajKarra69420/cs355project

# Protocol Specification

## Communication

- Bob will create a BSD socket to listen for communcation from Alice
- Alice will create her own BSD socket and connect to Bob 

## Protocol
1. Alice and Bob will perform an ECDH key exchange to arrive at a shared secret
2. Using the shared secret above, Alice and Bob will input their shared secret into a HKDF fucntion using the sha 256 hash function. This will serve as a key to be used for the AES GCM cipher
3. Alice and Bob will both hash their file using the sha 256 hash function and store the hash
4. Bob will follow the specifications for AES GCM to encrypt his file hash and send the IV, ciphertext, tag, and associated data (this is used to let the other party know who's hash is who's and is supposed to be sent unencrypted) to Alice 
5. Alice will follow the specifications for AES GCM to encrypt her file hash and send the IV, ciphertext, tag, and associated data (this is used to let the other party know who's hash is who's and is supposed to be sent unencrypted) to Bob
6. Bob will then follow the specification for AES GCM to decrypt the file hash with the data he received 
7. Alice will then follow the specification for AES GCM to decrypt the file hash with the data she received
8. Bob will output Success if the hash he receives is the same as his hash and Failure otherwise. 
9. Alice will output Success if the hash she receives is the same as her hash and Failure otherwise. 
10. Bob will follow the specifications for AES GCM to encrypt his result from step 8 and send the IV, ciphertext, tag, and associated data (this is used to let the other party know who's result is who's and is supposed to be sent unencrypted) to Alice 
11. Alice will follow the specifications for AES GCM to encrypt her result from step 9 and send the IV, ciphertext, tag, and associated data (this is used to let the other party know who's result is who's and is supposed to be sent unencrypted) to Bob
12. Bob will then follow the specification for AES GCM to decrypt the result from step 9 with the data he received, and print out Alice's result
13. Alice will then follow the specification for AES GCM to decrypt the result from step 8 with the data she received, and print out Bob's result

# Code Specifications

## Communication Channel

For our communication channel we used the python socket library. The python socket library provides access to the BSD socket interface and uses TCP/IP for communication. This channel by itself is an insecure and unauthenticated channel.

## Cryptography

We use python's crypography library (https://cryptography.io/en/latest/) and the cryptographic primitives in this library transfrom the communication channel mentioned above into a secure and authenticated channel. From this library we use the elliptic curve module to perform an Elliptic Curve Diffie Hellman key exchange. We choose to use the NIST P-384 curve in our code. We then use the HKDF class from this library to derive a key to be used with a symmteric cipher from the shared secret from the key exchange mentioned previously. We also use the hashes module from this library to use the sha256 hash function as both part of the HKDF and to hash the password file. Finally, we use the modes and algorithms modules and the Cipher class to use AES for symmetric encryption. We use the GCM mode of AES to provide both encryption and authentication of data.

# Security Analysis

## Security Goals
The security goals for this protocol are as follows:
- Alice and Bob can learn whether their files are identical without either Alice, Bob, nor the Adversary learning any additional information about the files
- No adversary can learn anything from communications between Alice and Bob
- Alice and Bob can prove that communication they recieve came from the other
- Alice and Bob can detect if the communication they recieve has been tampered with

## Threat Model 

For Alice and Bob, we use a honest-but-curious threat model. This means that Alice and Bob will follow the protocol honestly but they will try to learn extra information. For example, Alice and Bob can analyze, store, and perform any operations on the messages they receive. However, Alice and Bob are unable to perform active attacks (e.g if the protocol says hash the file, they are unable to lie about the hash of their file). 

For any adversary, we consider a dynamic adversary. This means that an adversary is able manipulate messages, perform mitm attacks, and attempt to subvert the protocol however they desire. 


## Assumptions 

Our assumptions are as follows:
- We assume that the sha 256 hash function is collision resistant 
- We assuem that the sha 256 hash function is a random oracle (for the hkdf)
- We assume that the GCM mode of AES is IND-CCA3 secure (the definition of IND-CCA3 security can be seen here: https://eprint.iacr.org/2004/272.pdf. This is eqivalent to authenticated encryption) 
- We assume that Alice and Bob have already exchanged public keys and they can identify each others public key 

## How the Security Goals are Achieved

- Alice and Bob can learn whether their files are identical without either Alice, Bob, nor the Adversary learning any additional information about the files

In our protocol, Alice and Bob both hash the contents of their file and send the encrypted hashes over the network. Because we assume that AES GCM is IND-CCA3 secure, the adversary can not learn anything about the ciphertext even when performing chosen ciphertext attacks

- No adversary can learn anything from communications between Alice and Bob

In our protocol, we make use of AES GCM which we assume to be IND CCA3 secure. Because we assume that AES GCM is IND-CCA3 secure, the adversary can not learn anything about the ciphertext even when performing chosen ciphertext attacks

- Alice and Bob can prove that communication they recieve came from the other

In our protocol, we make use of AES GCM which we assume to be IND CCA3 secure. Because we assume that AES GCM is IND-CCA3 secure, we know that AES GCM has the following property: existential unforgeability of messages against adaptive chosen ciphertext attacks (this is stronger than any of the security garuntees we went over in class).

- Alice and Bob can detect if the communication they recieve has been tampered with
In our protocol, we make use of AES GCM which we assume to be IND CCA3 secure. Because we assume that AES GCM is IND-CCA3 secure, we know that AES GCM has the following property: existential unforgeability of messages against adaptive chosen ciphertext attacks (this is stronger than any of the security garuntees we went over in class).

## Out of Scope

We do not consider vulnerabilities that exist in the python packages that we use (e.g vulnerabilities in the pickle package are out of scope for our threat model) nor the vulnerabilities that exist in implementations of cryptographic primitives (e.g a side channel for AES is out of scope).
