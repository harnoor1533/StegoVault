from PIL import Image
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def derive_key(password, salt):
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1
    )

    return kdf.derive(password.encode())


def hide_file(secret_file, carrier_image, password, output_path):
    # Read secret file
    with open(secret_file, "rb") as file:
        file_data = file.read()

    # Generate salt and nonce
    salt = os.urandom(16)
    nonce = os.urandom(12)

    # Derive encryption key
    key = derive_key(password, salt)

    # Encrypt file
    aes = AESGCM(key)
    encrypted_data = aes.encrypt(
        nonce,
        file_data,
        None
    )

    # Read filename
    filename = os.path.basename(secret_file)
    filename_bytes = filename.encode()

    # Build payload
    payload = (
        len(filename_bytes).to_bytes(2, "big")
        + filename_bytes
        + len(salt + nonce + encrypted_data).to_bytes(4, "big")
        + salt
        + nonce
        + encrypted_data
    )

    # Convert payload to bits
    binary = ""

    for byte in payload:
        binary += format(byte, "08b")

    # Open carrier
    image = Image.open(carrier_image).convert("RGB")

    width, height = image.size

    capacity = width * height

    if len(binary) > capacity:
        raise ValueError(
            f"File too large. Required: {len(binary)} bits, "
            f"available: {capacity} bits."
        )

    pixels = image.load()

    bit_index = 0

    for y in range(height):
        for x in range(width):

            if bit_index >= len(binary):
                break

            r, g, b = pixels[x, y]

            new_r = (r & 254) | int(binary[bit_index])

            pixels[x, y] = (new_r, g, b)

            bit_index += 1

        if bit_index >= len(binary):
            break

    image.save(output_path, "PNG")

    return output_path

def extract_file(stego_image, password):
    # Read the stego image
    image = Image.open(stego_image).convert("RGB")
    pixels = image.load()
    width, height = image.size

    # Extract red-channel LSBs
    binary = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary += str(r & 1)

    # Convert bits to bytes
    def bits_to_bytes(bits):
        if len(bits) % 8 != 0:
            raise ValueError("Invalid payload data.")

        return bytes(
            int(bits[i:i + 8], 2)
            for i in range(0, len(bits), 8)
        )

    # Read filename length (16 bits)
    if len(binary) < 16:
        raise ValueError("Image is too small to contain a payload.")

    filename_length = int(binary[:16], 2)

    if filename_length == 0 or filename_length > 255:
        raise ValueError("No valid StegoVault payload found.")

    # Read filename
    filename_end = 16 + filename_length * 8

    if len(binary) < filename_end + 32:
        raise ValueError("Incomplete payload.")

    filename_bytes = bits_to_bytes(binary[16:filename_end])

    try:
        filename = filename_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("Invalid filename in payload.")

    # Read encrypted data size
    size_end = filename_end + 32
    encrypted_size = int(binary[filename_end:size_end], 2)

    if encrypted_size < 28:
        raise ValueError("Invalid encrypted payload size.")

    payload_end = size_end + encrypted_size * 8

    if payload_end > len(binary):
        raise ValueError("Payload is incomplete or image is corrupted.")

    # Extract encrypted bytes
    encrypted_blob = bits_to_bytes(binary[size_end:payload_end])

    # Split salt, nonce and ciphertext
    salt = encrypted_blob[:16]
    nonce = encrypted_blob[16:28]
    ciphertext = encrypted_blob[28:]

    # Derive key and decrypt
    key = derive_key(password, salt)

    try:
        original_data = AESGCM(key).decrypt(
            nonce,
            ciphertext,
            None
        )
    except Exception:
        raise ValueError(
            "Decryption failed. Check your password or image."
        )

    return filename, original_data