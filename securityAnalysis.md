# Security Analysis

## Security Goals
The security goals for this protocol are as follows:
- Prove Alice and Bob share the same file of passwords without either learning about what the other has in their file.
- No adversary can learn anything from communications between Alice and Bob
- Alice and Bob can prove that communication they recieve came from the other
- Alice and Bob can detect if the communication they recieve has been tampered with

## How the Security Goals are Achieved
Hash and Sign paradigm
Alice and Bob hash their files with SHA256
Alice and Bob each send an encyrpted hash to the other via an encryption + hash and sign paradigm
