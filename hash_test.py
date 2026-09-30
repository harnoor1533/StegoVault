import hashlib

filename = input("Enter file name: ")

with open(filename, "rb") as file:
    data = file.read()

sha256 = hashlib.sha256(data).hexdigest()

print("SHA-256:")
print(sha256)