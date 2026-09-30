from PIL import Image
import numpy as np
from scipy.stats import chi2


def analyze_images(stego_path, original_path):
    # Load images
    stego = Image.open(stego_path).convert("RGB")
    original = Image.open(original_path).convert("RGB")

    # Check dimensions
    if stego.size != original.size:
        raise ValueError("Original and stego images must have the same dimensions.")

    width, height = stego.size
    total_pixels = width * height

    # -------------------------
    # LSB ANALYSIS
    # -------------------------

    stego_pixels = stego.load()
    original_pixels = original.load()

    binary = []
    changed_lsb = 0

    for y in range(height):
        for x in range(width):
            stego_r = stego_pixels[x, y][0]
            original_r = original_pixels[x, y][0]

            # Stego LSB
            binary.append(stego_r & 1)

            # Compare original vs stego LSB
            if (original_r & 1) != (stego_r & 1):
                changed_lsb += 1

    zeros = binary.count(0)
    ones = binary.count(1)

    zero_percentage = (zeros / len(binary)) * 100
    one_percentage = (ones / len(binary)) * 100
    change_percentage = (changed_lsb / len(binary)) * 100

    # -------------------------
    # IMAGE QUALITY
    # -------------------------

    stego_array = np.array(stego, dtype=np.float64)
    original_array = np.array(original, dtype=np.float64)

    mse = np.mean((original_array - stego_array) ** 2)

    if mse == 0:
        psnr = float("inf")
    else:
        psnr = 10 * np.log10((255 ** 2) / mse)

    # -------------------------
    # CHI-SQUARE
    # -------------------------

    histogram = [0] * 256

    for y in range(height):
        for x in range(width):
            r, g, b = stego_pixels[x, y]
            histogram[r] += 1

    chi_square = 0

    for i in range(0, 256, 2):
        observed_0 = histogram[i]
        observed_1 = histogram[i + 1]

        total = observed_0 + observed_1

        if total > 0:
            expected = total / 2

            chi_square += (
                ((observed_0 - expected) ** 2) / expected
            )

            chi_square += (
                ((observed_1 - expected) ** 2) / expected
            )

    degrees_of_freedom = 127
    p_value = chi2.sf(chi_square, degrees_of_freedom)

    # -------------------------
    # PAYLOAD DETECTION
    # -------------------------

    payload_detected = False
    filename = None
    encrypted_size = None

    binary_string = "".join(map(str, binary))

    try:
        # Filename length
        filename_length = int(binary_string[:16], 2)

        if 0 < filename_length <= 255:

            filename_end = 16 + filename_length * 8

            filename_bytes = bytes(
                int(binary_string[i:i + 8], 2)
                for i in range(16, filename_end, 8)
            )

            filename = filename_bytes.decode("utf-8")

            # Encrypted data size
            size_end = filename_end + 32

            encrypted_size = int(
                binary_string[filename_end:size_end],
                2
            )

            payload_end = size_end + encrypted_size * 8

            if (
                encrypted_size >= 28
                and payload_end <= len(binary_string)
            ):
                payload_detected = True

    except Exception:
        payload_detected = False

    # -------------------------
    # RETURN RESULTS
    # -------------------------

    return {
        "width": width,
        "height": height,
        "total_pixels": total_pixels,

        "total_lsbs": len(binary),
        "zeros": zeros,
        "ones": ones,
        "zero_percentage": zero_percentage,
        "one_percentage": one_percentage,

        "changed_lsb": changed_lsb,
        "change_percentage": change_percentage,

        "mse": mse,
        "psnr": psnr,

        "chi_square": chi_square,
        "degrees_of_freedom": degrees_of_freedom,
        "p_value": p_value,

        "payload_detected": payload_detected,
        "filename": filename,
        "encrypted_size": encrypted_size
    }