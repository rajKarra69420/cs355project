# Security Analysis

## Security Goals
The security goals for this protocol are as follows:
- Alice and Bob can learn whether their files are identical without either Alice, Bob, nor the Adversary learning any additional information about the files
- No adversary can learn anything from communications between Alice and Bob
- Alice and Bob can prove that communication they recieve came from the other
- Alice and Bob can detect if the communication they recieve has been tampered with

## Threat Model 

For Alice and Bob, we use a honest-but-curious threat model. This means that Alice and Bob will follow the protocol honestly but they will try to learn extra information. For example, Alice and Bob can analyze, store, and perform any opoerations on the messages they receive. However, Alice and Bob are unable to perform active attacks (e.g if the protocol says hash the file, they are unable to lie about the hash of their file). 

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
