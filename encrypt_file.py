from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os

# Ask for password
password = input("Enter password: ").encode()

# Read the PDF
with open("test10.pdf", "rb") as file:
    data = file.read()

# Create random salt
salt = os.urandom(16)

# Create key
kdf = Scrypt(
    salt=salt,
    length=32,
    n=2**14,
    r=8,
    p=1
)

key = kdf.derive(password)

# Create AES
aes = AESGCM(key)

# Create random nonce
nonce = os.urandom(12)

# Encrypt PDF
encrypted_data = aes.encrypt(nonce, data, None)

# Save encrypted data
with open("encrypted_file.bin", "wb") as file:
    file.write(salt)
    file.write(nonce)
    file.write(encrypted_data)

print("PDF encrypted successfully!")
print("Created: encrypted_file.bin")