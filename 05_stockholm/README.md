# stockholm

Harmless malware

usage: stockholm.py [-h] [-v] [-r KEY_FILE] [-s]

options:
  -h, --help                        show this help message and exit
  -v, --version                     show the version of the program.
  -r KEY_FILE, --reverse KEY_FILE   path to the key file to reverse the infection.
  -s, --silent                      run the program without producing any output..



Here’s a breakdown of how WannaCry handled the encryption and decryption process:

1. Encryption with AES:

    WannaCry used AES (Advanced Encryption Standard) in CBC mode (Cipher Block Chaining) to encrypt the files on the victim’s machine.
    AES is a symmetric encryption algorithm, meaning it uses the same key for both encryption and decryption.
    The AES key (a secret symmetric key) was generated randomly for each victim.

2. Encrypting the AES Key with RSA:

    The AES key, which was used to encrypt the victim's files, was then encrypted using the attacker’s RSA public key.
    RSA is an asymmetric encryption algorithm, which means it uses two keys: a public key (for encryption) and a private key (for decryption). The public key is typically shared, while the private key is kept secret by the attacker.
    The RSA public key was hardcoded into the WannaCry ransomware, and when a victim’s files were encrypted, the AES key used for that encryption was then encrypted with the attacker’s RSA public key.

3. Encrypted AES Key Sent to Victim:

    After the victim's files were encrypted, the encrypted AES key was stored along with the encrypted files. This means the victim has:
        The encrypted files (AES-encrypted).
        The encrypted AES key (RSA-encrypted).

Since the victim only has the RSA-encrypted AES key, they cannot decrypt it because they don’t have the attacker’s RSA private key.

4. Pay the Ransom:

    The victim was instructed to pay the ransom (in Bitcoin), and once the payment was made, the attacker would send the victim the RSA private key (or a decryption key) that would allow them to decrypt the AES key.
    Once the victim gets the RSA private key, they can decrypt the AES key (because only the RSA private key can decrypt the AES-encrypted AES key).
    After recovering the AES key, the victim could then use it to decrypt their files (since the AES key is what was used to encrypt the files in the first place).
