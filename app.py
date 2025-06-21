import streamlit as st
from PIL import Image
from io import BytesIO
from steganography import encode_message, decode_message

# --- Page Config ---
st.set_page_config(
    page_title="🔐 Steganography App",
    page_icon="🕵️‍♂️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Sidebar Info ---
with st.sidebar:
    st.title("🔧 App Options")
    st.markdown("""
    This app allows you to **hide secret messages** inside images using **AES encryption + steganography**.

    🔹 **Encode**: Embed a secret message into an image using a password.  
    🔹 **Decode**: Extract and decrypt the message from a previously encoded image.

    ---
    Made with ❤️ using Streamlit
    """)

# --- Title ---
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>🕵️ Image Steganography with Password</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Mode Selection ---
option = st.radio("Choose what you want to do:", ("📝 Encode Message", "🔍 Decode Message"))

# --- Encode Section ---
if option == "📝 Encode Message":
    st.subheader("🔐 Hide a Secret Message Inside an Image")
    uploaded_image = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"], help="Recommended: PNG format")
    message = st.text_area("✉️ Enter your secret message:")
    password = st.text_input("🔑 Create a strong password", type="password")

    if uploaded_image and message and password:
        try:
            image = Image.open(uploaded_image).convert("RGB")
            encoded_image = encode_message(image, message, password)

            st.success("✅ Message encoded successfully!")
            st.image(encoded_image, caption="🔎 Preview: Encoded Image", use_column_width=True)

            # Save and download
            img_bytes = BytesIO()
            encoded_image.save(img_bytes, format="PNG")
            st.download_button(
                label="⬇️ Download Encoded Image",
                data=img_bytes.getvalue(),
                file_name="encoded_image.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"❌ An error occurred while encoding: {str(e)}")

# --- Decode Section ---
elif option == "🔍 Decode Message":
    st.subheader("🔓 Extract a Hidden Message from an Image")
    uploaded_image = st.file_uploader("📤 Upload an encoded image", type=["png", "jpg", "jpeg"])
    password = st.text_input("🔑 Enter decryption password", type="password")

    if uploaded_image and password:
        try:
            image = Image.open(uploaded_image).convert("RGB")
            decoded_text = decode_message(image, password)

            if decoded_text.startswith("[Error]"):
                st.error("❌ Decryption failed. The password may be incorrect or the image may not contain a valid message.")
            else:
                st.success("✅ Message decoded successfully!")
                st.code(decoded_text, language='text')
        except Exception as e:
            st.error(f"❌ An error occurred while decoding: {str(e)}")

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🔐 Secure. Simple. Steganography. | © 2025 Cyber Security | By Roni Seikh")
