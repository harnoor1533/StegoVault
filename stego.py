from PIL import Image

image = Image.open("moon.png").convert("RGB")
pixels = image.load()

# Read the secret file
import os

secret_file = input("Enter secret file name: ")

with open(secret_file, "rb") as file:
    secret_data = file.read()

filename = os.path.basename(secret_file)

print("File name:", filename)

# Convert each byte into binary
data_binary = ""

for byte in secret_data:
    data_binary += format(byte, "08b")

# Store file size in first 32 bits
# Convert filename to binary
filename_binary = ""

for char in filename:
    filename_binary += format(ord(char), "08b")

# Store filename length in 16 bits
filename_length = len(filename)
filename_length_binary = format(filename_length, "016b")

# Store file size in 32 bits
file_size = len(secret_data)
size_binary = format(file_size, "032b")

# Combine:
# filename length + filename + file size + file data
data = filename_length_binary + filename_binary + size_binary + data_binary

print("File name:", filename)
print("File size:", file_size, "bytes")
print("Total data:", len(data), "bits")

print("Secret file size:", file_size, "bytes")
print("Total data:", len(data), "bits")

# Check capacity
capacity = image.width * image.height

if len(data) > capacity:
    print("ERROR: File is too large for this image.")
    exit()

index = 0

for y in range(image.height):
    for x in range(image.width):

        if index >= len(data):
            break

        r, g, b = pixels[x, y]

        # Hide one bit in Red channel
        r = (r & 254) | int(data[index])

        pixels[x, y] = (r, g, b)

        index += 1

    if index >= len(data):
        break

image.save("test_stego.png")

print("File hidden successfully!")