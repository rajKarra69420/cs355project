# Security Analysis

## Security Goals
The security goals for this protocol are as follows:
- Prove Alice and Bob share the same file of passwords without either learning about what the other has in their file.
- No adversary can learn anything from communications between Alice and Bob
- Alice and Bob can prove that communication they recieve came from the other
- Alice and Bob can detect if the communication they recieve has been tampered with

## How the Security Goals are Achieved
We use AES-GCM to encrypt and sign messages between Alice and Bob.

The AES-GCM protocol allows us to ensure that adversaries cannot learn any information from the communications between Bob and Alice. It also ensures that Alice and Bob will know if their messages have been tampered with over the network. Source: AES-GCM Security Proof

The program takes the password text file as input. Using the text file is hashes the information using SHA256. Then the hash is sent via AES-GCM to the other user. Once both users have recieved a connection with the other, the program decrypts the message and compares the hash values generated from both user's password files. If they match the users are notified as such.

If the public key exchange is not sufficient to ensure that the messages came from Alice and Bob *ask about this*, we can sign the hashed messages to meet security goal 3.
