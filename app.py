import streamlit as st
import tempfile
import os
from stego_engine import hide_file, extract_file
from analyzer_engine import analyze_images

st.set_page_config(
    page_title="StegoVault",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 StegoVault")
st.subheader("Secure Steganography & Steganalysis Platform")

st.write(
    "Hide, extract, encrypt and analyze files securely using "
    "image steganography."
)

st.divider()

col1, col2, col3 = st.columns(3)


# =========================
# HIDE FILE
# =========================

with col1:
    st.subheader("🔒 Hide File")

    secret_file = st.file_uploader(
        "Choose the file you want to hide",
        type=None,
        key="secret_file"
    )

    carrier_file = st.file_uploader(
        "Choose a carrier PNG image",
        type=["png"],
        key="carrier_file"
    )

    password = st.text_input(
        "Enter encryption password",
        type="password",
        key="hide_password"
    )

    if st.button("🔐 Encrypt & Hide", use_container_width=True):

        if secret_file is None:
            st.error("Please choose a file to hide.")

        elif carrier_file is None:
            st.error("Please choose a carrier image.")

        elif not password:
            st.error("Please enter a password.")

        else:
            try:
                with tempfile.TemporaryDirectory() as temp_dir:

                    secret_path = os.path.join(
                        temp_dir,
                        secret_file.name
                    )

                    carrier_path = os.path.join(
                        temp_dir,
                        carrier_file.name
                    )

                    output_path = os.path.join(
                        temp_dir,
                        "StegoVault_output.png"
                    )

                    with open(secret_path, "wb") as file:
                        file.write(secret_file.getbuffer())

                    with open(carrier_path, "wb") as file:
                        file.write(carrier_file.getbuffer())

                    hide_file(
                        secret_path,
                        carrier_path,
                        password,
                        output_path
                    )

                    with open(output_path, "rb") as file:
                        stego_data = file.read()

                st.success(
                    "✅ File encrypted and hidden successfully!"
                )

                st.download_button(
                    label="⬇️ Download Stego Image",
                    data=stego_data,
                    file_name="StegoVault_output.png",
                    mime="image/png",
                    use_container_width=True
                )

            except ValueError as error:
                st.error(f"❌ {error}")

            except Exception as error:
                st.error(f"❌ Something went wrong: {error}")


# =========================
# EXTRACT FILE
# =========================

with col2:
    st.subheader("🔓 Extract File")

    stego_file = st.file_uploader(
        "Upload StegoVault image",
        type=["png"],
        key="stego_file"
    )

    extract_password = st.text_input(
        "Enter decryption password",
        type="password",
        key="extract_password"
    )

    if st.button(
        "🔓 Extract & Decrypt",
        use_container_width=True
    ):

        if stego_file is None:
            st.error("Please upload a StegoVault image.")

        elif not extract_password:
            st.error("Please enter the password.")

        else:
            try:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".png"
                ) as temp_file:

                    temp_file.write(
                        stego_file.getbuffer()
                    )

                    stego_path = temp_file.name

                filename, recovered_data = extract_file(
                    stego_path,
                    extract_password
                )

                os.remove(stego_path)

                st.success(
                    f"✅ File extracted successfully: {filename}"
                )

                st.download_button(
                    label="⬇️ Download Recovered File",
                    data=recovered_data,
                    file_name=filename,
                    mime="application/octet-stream",
                    use_container_width=True
                )

            except ValueError as error:
                st.error(f"❌ {error}")

            except Exception as error:
                st.error(f"❌ Something went wrong: {error}")


# =========================
# ANALYZER
# =========================

with col3:
    st.subheader("🕵️ Analyze Image")

    st.write(
        "Perform steganalysis and generate a security report."
    )

    stego_image = st.file_uploader(
        "Upload Stego Image",
        type=["png"],
        key="analyzer_stego"
    )

    original_image = st.file_uploader(
        "Upload Original Image",
        type=["png"],
        key="analyzer_original"
    )

    if st.button(
        "🔍 Analyze Image",
        use_container_width=True
    ):

        if stego_image is None:
            st.warning("⚠️ Please upload the stego image.")

        elif original_image is None:
            st.warning("⚠️ Please upload the original image.")

        else:

            try:
                import tempfile
                import os

                with tempfile.TemporaryDirectory() as temp_dir:

                    stego_path = os.path.join(
                        temp_dir,
                        "stego.png"
                    )

                    original_path = os.path.join(
                        temp_dir,
                        "original.png"
                    )

                    with open(stego_path, "wb") as f:
                        f.write(stego_image.getbuffer())

                    with open(original_path, "wb") as f:
                        f.write(original_image.getbuffer())

                    results = analyze_images(
                        stego_path,
                        original_path
                    )

                st.success("✅ Analysis completed successfully!")

                st.markdown("#### 📊 LSB Analysis")

                metric1, metric2 = st.columns(2)

                metric1.metric(
                    "0 Bits",
                    f"{results['zero_percentage']:.2f}%"
                )

                metric2.metric(
                    "1 Bits",
                    f"{results['one_percentage']:.2f}%"
                )

                st.metric(
                    "LSB Changes",
                    f"{results['change_percentage']:.2f}%"
                )

                st.markdown("#### 📈 Image Quality")

                quality1, quality2 = st.columns(2)

                quality1.metric(
                    "MSE",
                    f"{results['mse']:.4f}"
                )

                quality2.metric(
                    "PSNR",
                    f"{results['psnr']:.2f} dB"
                )

                st.markdown("#### 🧮 Statistical Analysis")

                stat1, stat2 = st.columns(2)

                stat1.metric(
                    "Chi-Square",
                    f"{results['chi_square']:.2f}"
                )

                stat2.metric(
                    "P-Value",
                    f"{results['p_value']:.3e}"
                )

                st.markdown("#### 🔐 Payload Detection")

                if results["payload_detected"]:

                    st.success(
                        "🚨 StegoVault payload detected!"
                    )

                    st.write(
                        f"**Hidden file:** `{results['filename']}`"
                    )

                    st.write(
                        f"**Encrypted data:** "
                        f"{results['encrypted_size']:,} bytes"
                    )

                else:

                    st.info(
                        "No valid StegoVault payload detected."
                    )

            except ValueError as e:

                st.error(f"❌ {e}")

            except Exception as e:

                st.error(
                    f"❌ Analysis failed: {e}"
                )