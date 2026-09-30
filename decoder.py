from PIL import Image

image = Image.open("test_stego.png").convert("RGB")
pixels = image.load()

# Read hidden bits
binary = ""

for y in range(image.height):
    for x in range(image.width):

        r, g, b = pixels[x, y]

        binary += str(r & 1)

# -----------------------------
# Read filename length
# -----------------------------

filename_length = int(binary[0:16], 2)

print("Filename length:", filename_length)

# -----------------------------
# Read filename
# -----------------------------

filename_start = 16
filename_end = filename_start + (filename_length * 8)

filename_binary = binary[filename_start:filename_end]

filename = ""

for i in range(0, len(filename_binary), 8):
    byte = filename_binary[i:i+8]
    filename += chr(int(byte, 2))

print("Original filename:", filename)

# -----------------------------
# Read file size
# -----------------------------

size_start = filename_end
size_end = size_start + 32

file_size = int(binary[size_start:size_end], 2)

print("File size:", file_size, "bytes")

# -----------------------------
# Read actual file
# -----------------------------

data_start = size_end
data_end = data_start + (file_size * 8)

data_binary = binary[data_start:data_end]

recovered_data = bytearray()

for i in range(0, len(data_binary), 8):
    byte = data_binary[i:i+8]
    recovered_data.append(int(byte, 2))

# -----------------------------
# Save recovered file
# -----------------------------

with open("recovered_" + filename, "wb") as file:
    file.write(recovered_data)

print("File extracted successfully!")
print("Saved as:", "recovered_" + filename)