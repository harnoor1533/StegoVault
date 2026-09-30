from PIL import Image
import numpy as np

original = Image.open("moon.png").convert("RGB")
stego = Image.open("test_stego.png").convert("RGB")

original_array = np.array(original, dtype=float)
stego_array = np.array(stego, dtype=float)

mse = np.mean((original_array - stego_array) ** 2)

if mse == 0:
    psnr = float("inf")
else:
    psnr = 10 * np.log10((255 ** 2) / mse)

print("========== IMAGE QUALITY TEST ==========")

print("MSE:", mse)
print("PSNR:", psnr, "dB")