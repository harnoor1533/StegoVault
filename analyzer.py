from PIL import Image
import numpy as np
import os
from scipy.stats import chi2
print("\n========== STEGOVAULT ANALYZER ==========")

image_path = input(
    "Enter stego image path: "
)

original_path = input(
    "Enter original image path: "
)

if not os.path.exists(image_path):
    print("❌ Stego image not found!")
    exit()

if not os.path.exists(original_path):
    print("❌ Original image not found!")
    exit()

image = Image.open(image_path).convert("RGB")
original = Image.open(original_path).convert("RGB")
if image.size != original.size:

    print("❌ Image dimensions do not match!")

    print("Stego image:", image.size)
    print("Original image:", original.size)

    exit()

pixels = image.load()

total_bits = image.width * image.height
ones = 0
zeros = 0

# =========================
# LSB ANALYSIS
# =========================
binary = ""
for y in range(image.height):

    for x in range(image.width):

        r, g, b = pixels[x, y]

        lsb = r & 1
        binary += str(lsb)

        if lsb == 1:
            ones += 1
        else:
            zeros += 1


print("\n========== STEGOVAULT ANALYZER ==========")

print("Stego Image:", image_path)
print("Resolution:", image.width, "x", image.height)

print("\n--- LSB Analysis ---")

print("Total LSBs:", total_bits)
print("0 bits:", zeros)
print("1 bits:", ones)

zero_percentage = (zeros / total_bits) * 100
one_percentage = (ones / total_bits) * 100

print("Percentage of 0s:",
      round(zero_percentage, 2), "%")

print("Percentage of 1s:",
      round(one_percentage, 2), "%")


# =========================
# BASIC LSB WARNING
# =========================

if 48 <= one_percentage <= 52:

    print("\n⚠️ LSB distribution is close to 50/50.")
    print("Possible hidden data may be present.")

else:

    print("\n✅ No strong LSB anomaly detected.")

# =========================
# LSB CHANGE ANALYSIS
# =========================
changed_lsb = 0

original_pixels = original.load()

for y in range(image.height):

    for x in range(image.width):

        original_r, _, _ = original_pixels[x, y]
        stego_r, _, _ = pixels[x, y]

        original_lsb = original_r & 1
        stego_lsb = stego_r & 1

        if original_lsb != stego_lsb:
            changed_lsb += 1

change_percentage = (
    changed_lsb / total_bits
) * 100

print("\n--- LSB Change Analysis ---")

print("Changed LSBs:", changed_lsb)

print(
    "LSB change percentage:",
    round(change_percentage, 4),
    "%"
)
# =========================
# CHI-SQUARE ANALYSIS
# =========================

print("\n--- Chi-Square Analysis ---")

histogram = [0] * 256

for y in range(image.height):
    for x in range(image.width):
        r, g, b = pixels[x, y]
        histogram[r] += 1

chi_square = 0

for i in range(0, 256, 2):
    observed_0 = histogram[i]
    observed_1 = histogram[i + 1]

    total = observed_0 + observed_1

    if total > 0:
        expected = total / 2

        chi_square += ((observed_0 - expected) ** 2) / expected
        chi_square += ((observed_1 - expected) ** 2) / expected

print("Chi-Square value:", round(chi_square, 2))
# Degrees of freedom
degrees_of_freedom = 127

# Calculate p-value
p_value = chi2.sf(chi_square, degrees_of_freedom)

print("Degrees of freedom:", degrees_of_freedom)
print("P-value:", p_value)
# =========================
# IMAGE QUALITY
# =========================

original_array = np.array(original, dtype=float)
stego_array = np.array(image, dtype=float)

mse = np.mean(
    (original_array - stego_array) ** 2
)

if mse == 0:

    psnr = float("inf")

else:

    psnr = 10 * np.log10(
        (255 ** 2) / mse
    )


print("\n--- Image Quality ---")

print("MSE:", mse)

if psnr == float("inf"):

    print("PSNR: Infinite")

else:

    print("PSNR:",
          round(psnr, 2),
          "dB")
    # =========================
# FINAL ANALYSIS
# =========================

print("\n========== FINAL ANALYSIS ==========")

if change_percentage < 1:
    print("✅ Very low LSB modification detected.")

elif change_percentage < 5:
    print("⚠️ Moderate LSB modification detected.")

else:
    print("🚨 High LSB modification detected.")

if psnr > 50:
    print("✅ Excellent image similarity.")

elif psnr > 40:
    print("✅ Good image similarity.")

else:
    print("⚠️ Significant image difference detected.")

print("\nAnalysis completed.")
# =========================
# STEGOVAULT PAYLOAD CHECK
# =========================

print("\n--- StegoVault Payload Check ---")
filename = None
file_size = 0
try:

    # Read filename length
    filename_length = int(
        binary[0:16],
        2
    )

    # Basic validation
    if filename_length <= 0 or filename_length > 255:
        raise ValueError("Invalid filename length")

    filename_start = 16

    filename_end = (
        filename_start
        + filename_length * 8
    )

    # Read filename
    filename_binary = binary[
        filename_start:filename_end
    ]

    filename = ""

    for i in range(
        0,
        len(filename_binary),
        8
    ):

        filename += chr(
            int(
                filename_binary[i:i+8],
                2
            )
        )

    # Read encrypted file size
    size_start = filename_end
    size_end = size_start + 32

    file_size = int(
        binary[size_start:size_end],
        2
    )

    # Check whether the claimed data fits
    required_bits = (
        size_end
        + file_size * 8
    )

    if required_bits > len(binary):
        raise ValueError(
            "Payload exceeds image capacity"
        )

    print("Possible StegoVault payload detected!")
    print("Filename:", filename)
    print("Encrypted data size:", file_size, "bytes")

except Exception:

    print("No valid StegoVault payload detected.")
    # =========================
# DETAILED REPORT
# =========================

description_choice = input(
    "\nDo you want a detailed analysis description and report? (yes/no): "
).strip().lower()

if description_choice in ["yes", "y"]:

    print("\n")
    print("=" * 60)
    print("       STEGOVAULT DETAILED SECURITY REPORT")
    print("=" * 60)

    report = []

    # IMAGE INFORMATION
    report.append("1. IMAGE INFORMATION")
    report.append("-" * 40)
    report.append(f"Stego Image: {image_path}")
    report.append(f"Resolution: {image.width} x {image.height}")
    report.append(f"Total Pixels: {image.width * image.height}")
    report.append("")

    # LSB ANALYSIS
    report.append("2. LSB ANALYSIS")
    report.append("-" * 40)
    report.append(f"Total LSBs: {total_bits}")
    report.append(f"0 bits: {zeros}")
    report.append(f"1 bits: {ones}")
    report.append(f"Percentage of 0s: {round((zeros / total_bits) * 100, 2)}%")
    report.append(f"Percentage of 1s: {round((ones / total_bits) * 100, 2)}%")
    report.append("")

    report.append(
        "Description: LSB stands for Least Significant Bit. "
        "Steganography can modify LSBs to hide information inside image pixels. "
        "A distribution close to 50/50 can occur naturally, but encrypted "
        "payloads can also produce a highly random-looking LSB sequence."
    )
    report.append("")

    # LSB CHANGE
    report.append("3. LSB CHANGE ANALYSIS")
    report.append("-" * 40)
    report.append(f"Changed LSBs: {changed_lsb}")
    report.append(f"LSB Change Percentage: {round(change_percentage, 4)}%")
    report.append("")

    report.append(
        "Description: This compares the original carrier image with the "
        "stego image and counts how many red-channel LSBs were changed. "
        "A higher percentage means more pixels were modified. In this "
        "StegoVault implementation, the encrypted payload occupies a large "
        "portion of the available carrier capacity, so a high modification "
        "percentage is expected."
    )
    report.append("")

    # CHI-SQUARE
    report.append("4. CHI-SQUARE ANALYSIS")
    report.append("-" * 40)
    report.append(f"Chi-Square Value: {round(chi_square, 2)}")
    report.append(f"Degrees of Freedom: {degrees_of_freedom}")
    report.append(f"P-Value: {p_value:.6e}")
    report.append("")

    report.append(
        "Description: The chi-square test compares the observed distribution "
        "of paired pixel intensity values with an expected distribution. "
        "The p-value indicates how compatible the observed distribution is "
        "with the statistical model used by this test. A very small p-value "
        "indicates a statistically significant deviation from that model. "
        "However, this result alone does not prove that steganography is present."
    )
    report.append("")

    # IMAGE QUALITY
    report.append("5. IMAGE QUALITY ANALYSIS")
    report.append("-" * 40)
    report.append(f"MSE: {mse}")
    report.append(f"PSNR: {psnr:.2f} dB")
    report.append("")

    report.append(
        "Description: MSE (Mean Squared Error) measures the average squared "
        "difference between the original and stego images. Lower MSE means "
        "smaller pixel-level differences. PSNR (Peak Signal-to-Noise Ratio) "
        "measures similarity between the two images. A higher PSNR generally "
        "indicates greater similarity."
    )
    report.append("")

    # PAYLOAD
    report.append("6. STEGOVAULT PAYLOAD ANALYSIS")
    report.append("-" * 40)

    if filename:
        report.append("Payload Status: DETECTED")
        report.append(f"Hidden Filename: {filename}")
        report.append(f"Encrypted Data Size: {file_size} bytes")

        report.append("")
        report.append(
            "Description: A valid StegoVault payload structure was detected "
            "inside the image. The payload contains metadata describing the "
            "hidden filename and the size of the encrypted data."
        )
    else:
        report.append("Payload Status: NOT DETECTED")

    report.append("")

    # FINAL SUMMARY
    report.append("7. FINAL SECURITY SUMMARY")
    report.append("-" * 40)

    if filename:
        report.append("StegoVault Payload: DETECTED")
    else:
        report.append("StegoVault Payload: NOT DETECTED")

    if change_percentage >= 5:
        report.append("LSB Modification: HIGH")
    elif change_percentage >= 1:
        report.append("LSB Modification: MODERATE")
    else:
        report.append("LSB Modification: LOW")

    if psnr > 50:
        report.append("Image Similarity: EXCELLENT")
    elif psnr > 40:
        report.append("Image Similarity: GOOD")
    else:
        report.append("Image Similarity: SIGNIFICANT DIFFERENCE")

    if p_value < 0.05:
        report.append("Chi-Square Test: STATISTICALLY SIGNIFICANT")
    else:
        report.append("Chi-Square Test: NOT STATISTICALLY SIGNIFICANT")

    report.append("")
    report.append(
        "IMPORTANT: Statistical steganalysis results are indicators, not "
        "absolute proof of hidden information. In this case, the strongest "
        "evidence is the successful detection of a valid StegoVault payload."
    )

    # PRINT REPORT
    for line in report:
        print(line)

    # SAVE REPORT
    report_filename = "StegoVault_Report.txt"

    with open(report_filename, "w", encoding="utf-8") as file:
        file.write("\n".join(report))

    print("\n" + "=" * 60)
    print(f"✅ Detailed report saved as: {report_filename}")
    print("=" * 60)

else:
    print("\nDetailed description skipped.")