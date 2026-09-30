# 🔐 StegoVault

StegoVault is a secure file steganography and steganalysis platform that allows users to hide files inside PNG images while protecting the hidden data using modern authenticated encryption.

The project combines **LSB steganography**, **AES-GCM encryption**, **Scrypt key derivation**, and **statistical steganalysis** into a Streamlit-based web application.

---

## ✨ Features

### 🔒 Secure File Hiding
- Hide arbitrary files inside PNG images.
- Supports files such as:
  - PDF
  - TXT
  - ZIP
  - Images
  - Other binary files

### 🔑 Encryption
- AES-256-GCM authenticated encryption
- Password-based key derivation using Scrypt
- Random salt and nonce for every encryption operation
- Authentication tag provided by AES-GCM

### 🖼️ LSB Steganography
- Uses Least Significant Bit (LSB) steganography.
- Hidden data is embedded into the red channel of the carrier image.
- Stores filename and encrypted payload metadata inside the image.

### 🔓 File Extraction
- Extract hidden encrypted data from a stego image.
- Decrypt the recovered data using the original password.
- Wrong passwords are rejected through AES-GCM authentication.

### 🕵️ Steganalysis
StegoVault analyzes images using:

- LSB distribution
- LSB modification percentage
- Mean Squared Error (MSE)
- Peak Signal-to-Noise Ratio (PSNR)
- Chi-square analysis
- P-value
- Hidden payload detection

### 🌐 Web Interface
Built using Streamlit with three main modules:

- 🔒 Hide File
- 🔓 Extract File
- 🕵️ Analyze Image

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web interface |
| Pillow | Image processing |
| NumPy | Numerical analysis |
| SciPy | Statistical analysis |
| Cryptography | AES-GCM and Scrypt |
| Git & GitHub | Version control |

---

## 🔐 Security Architecture

The encryption process follows:

```text
Password
   ↓
Scrypt
   ↓
256-bit Encryption Key
   ↓
AES-256-GCM
   ↓
Encrypted File
   ↓
LSB Steganography
   ↓
Stego Image
