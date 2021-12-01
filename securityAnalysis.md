# Security Analysis

## Security Goals
The security goals for this protocol are as follows:
- Prove Alice and Bob share the same file of passwords without either learning about what the other has in their file.
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
- We assume that the GCM mode of AES is IND-CCA2 secure 
- We assume that Alice and Bob have already exchanged public keys and they can identify each others public key 

## Protocol 

- Alice and Bob will perform an ECDH key exchange to arrive at a shared secret
- Using the shared secret above, Alice and Bob will input their shared secret into a HKDF fucntion using the sha 256 hash function. This will serve as a key to be used for the AES GCM cipher
- Alice and Bob will both hash their file and store the hash
- Alice will encrypt her file hash and send it to Bob
- Bob will encrypt his file hash and send it to Alice
- Alice will output Success if the hash she receives is the same as her hash and Failure otherwise
- Bob will output Success if the hash he receives is the same as his hash and Failure otherwise

## How the Security Goals are Achieved
We use AES-GCM to encrypt and sign messages between Alice and Bob.

The AES-GCM protocol allows us to ensure that adversaries cannot learn any information from the communications between Bob and Alice. It also ensures that Alice and Bob will know if their messages have been tampered with over the network. Source: AES-GCM Security Proof

The program takes the password text file as input. Using the text file is hashes the information using SHA256. Then the hash is sent via AES-GCM to the other user. Once both users have recieved a connection with the other, the program decrypts the message and compares the hash values generated from both user's password files. If they match the users are notified as such.

## Out of Scope

We do not consider vulnerabilities that exist in the python packages that we use (e.g vulnerabilities in the pickle package are out of scope for our threat model) nor the vulnerabilities that exist in implementations of cryptographic primitives (e.g a side channel for AES is out of scope).
