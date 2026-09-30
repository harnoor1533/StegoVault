from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from PIL import Image
import os

print("========================")
print("       STEGOVAULT")
print("========================")

print("1. Hide a file")
print("2. Extract a file")
print("3. Exit")

choice = input("Choose an option: ")

# =========================
# HIDE FILE
# =========================

if choice == "1":

    print("\n--- Hide File ---")

    secret_file = input("Enter file to hide: ")
    carrier_image = input("Enter carrier image: ")
    password = input("Enter password: ").encode()

    # Read original file
    with open(secret_file, "rb") as file:
        original_data = file.read()

    # -------------------------
    # ENCRYPTION
    # -------------------------

    salt = os.urandom(16)

    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1
    )

    key = kdf.derive(password)

    aes = AESGCM(key)

    nonce = os.urandom(12)

    encrypted_data = aes.encrypt(
        nonce,
        original_data,
        None
    )

    print("\n✅ File encrypted successfully!")

    # -------------------------
    # PREPARE DATA FOR HIDING
    # -------------------------

    filename = os.path.basename(secret_file)

    filename_binary = ""

    for char in filename:
        filename_binary += format(ord(char), "08b")

    filename_length_binary = format(
        len(filename),
        "016b"
    )

    # IMPORTANT:
    # Store salt + nonce + encrypted data

    encrypted_file_data = (
        salt +
        nonce +
        encrypted_data
    )

    file_size = len(encrypted_file_data)

    size_binary = format(
        file_size,
        "032b"
    )

    data_binary = ""

    for byte in encrypted_file_data:
        data_binary += format(byte, "08b")

    # -------------------------
    # COMBINE ALL DATA
    # -------------------------

    data = (
        filename_length_binary
        + filename_binary
        + size_binary
        + data_binary
    )

    print("File name:", filename)
    print("Encrypted file size:", file_size, "bytes")
    print("Total data:", len(data), "bits")

    # -------------------------
    # OPEN IMAGE
    # -------------------------

    image = Image.open(carrier_image).convert("RGB")

    pixels = image.load()

    # -------------------------
    # CAPACITY CHECK
    # -------------------------

    capacity = image.width * image.height

    if len(data) > capacity:

        print("\n❌ File is too large for this image.")

        exit()

    # -------------------------
    # HIDE DATA
    # -------------------------

    index = 0

    for y in range(image.height):

        for x in range(image.width):

            if index >= len(data):
                break

            r, g, b = pixels[x, y]

            r = (r & 254) | int(data[index])

            pixels[x, y] = (r, g, b)

            index += 1

        if index >= len(data):
            break

    # -------------------------
    # SAVE STEGO IMAGE
    # -------------------------

    output_image = "test_stego.png"

    image.save(output_image)

    print("\n🎉 File hidden successfully!")
    print("Created:", output_image)


# =========================
# EXTRACT FILE
# =========================

elif choice == "2":

    print("\n--- Extract File ---")

    stego_image = input("Enter stego image: ")
    password = input("Enter password: ").encode()

    # -------------------------
    # OPEN STEGO IMAGE
    # -------------------------

    image = Image.open(stego_image).convert("RGB")

    pixels = image.load()

    # -------------------------
    # READ HIDDEN BITS
    # -------------------------

    binary = ""

    for y in range(image.height):

        for x in range(image.width):

            r, g, b = pixels[x, y]

            binary += str(r & 1)

    # -------------------------
    # READ FILENAME
    # -------------------------

    filename_length = int(
        binary[0:16],
        2
    )

    filename_start = 16

    filename_end = (
        filename_start
        + filename_length * 8
    )

    filename_binary = binary[
        filename_start:filename_end
    ]

    filename = ""

    for i in range(
        0,
        len(filename_binary),
        8
    ):

        byte = filename_binary[i:i+8]

        filename += chr(
            int(byte, 2)
        )

    print(
        "Original filename:",
        filename
    )

    # -------------------------
    # READ FILE SIZE
    # -------------------------

    size_start = filename_end

    size_end = size_start + 32

    file_size = int(
        binary[size_start:size_end],
        2
    )

    print(
        "Encrypted file size:",
        file_size,
        "bytes"
    )

    # -------------------------
    # EXTRACT ENCRYPTED DATA
    # -------------------------

    data_start = size_end

    data_end = (
        data_start
        + file_size * 8
    )

    data_binary = binary[
        data_start:data_end
    ]

    encrypted_file_data = bytearray()

    for i in range(
        0,
        len(data_binary),
        8
    ):

        byte = data_binary[i:i+8]

        encrypted_file_data.append(
            int(byte, 2)
        )

    # -------------------------
    # SEPARATE SALT
    # -------------------------

    salt = bytes(
        encrypted_file_data[:16]
    )

    # -------------------------
    # SEPARATE NONCE
    # -------------------------

    nonce = bytes(
        encrypted_file_data[16:28]
    )

    # -------------------------
    # SEPARATE CIPHERTEXT
    # -------------------------

    ciphertext = bytes(
        encrypted_file_data[28:]
    )

    # -------------------------
    # CREATE KEY
    # -------------------------

    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1
    )

    key = kdf.derive(password)

    # -------------------------
    # DECRYPT
    # -------------------------

    try:

        aes = AESGCM(key)

        decrypted_data = aes.decrypt(
            nonce,
            ciphertext,
            None
        )

        output_file = (
            "recovered_"
            + filename
        )

        with open(
            output_file,
            "wb"
        ) as file:

            file.write(
                decrypted_data
            )

        print(
            "\n🎉 File extracted successfully!"
        )

        print(
            "Saved as:",
            output_file
        )

    except Exception as e:

        print(
            "\n❌ Decryption failed!"
        )

        print(
            "Error type:",
            type(e).__name__
        )

        print(
            "Error:",
            e
        )


# =========================
# EXIT
# =========================

elif choice == "3":

    print("Goodbye!")


# =========================
# INVALID OPTION
# =========================

else:

    print("Invalid choice")