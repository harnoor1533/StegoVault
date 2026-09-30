from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# Ask for password
password = input("Enter password: ").encode()

# Read encrypted file
with open("recovered_encrypted_file.bin", "rb") as file:
    salt = file.read(16)
    nonce = file.read(12)
    encrypted_data = file.read()

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

# Decrypt
try:
    decrypted_data = aes.decrypt(nonce, encrypted_data, None)

    with open("decrypted_test10.pdf", "wb") as file:
        file.write(decrypted_data)

    print("PDF decrypted successfully!")
    print("Created: decrypted_test10.pdf")

except Exception as e:
    print("ERROR:", type(e).__name__)
    print("DETAIL:", e)