from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os

password = b"moon123"

# Create salt
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

# Create nonce
nonce = os.urandom(12)

# Test data
message = b"Hello StegoVault!"

# Encrypt
encrypted = aes.encrypt(nonce, message, None)

# Decrypt immediately
decrypted = aes.decrypt(nonce, encrypted, None)

print("Original:", message)
print("Decrypted:", decrypted)

if message == decrypted:
    print("AES TEST PASSED!")