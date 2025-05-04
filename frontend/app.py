import streamlit as st
import requests
from PIL import Image
import io

st.title("🚦 Dynamic Traffic Management System")

# File uploader for user input
uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'png'])

if uploaded_file is not None:
    st.subheader("Processing...")

    # Send file to backend
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    
    try:
        response = requests.post("http://127.0.0.1:5008/upload", files=files)

        if response.status_code == 200:
            data = response.json()

            # Fetch the processed image
            img_url = f"http://127.0.0.1:5008{data['image_path']}"
            img_response = requests.get(img_url)

            if img_response.status_code == 200:
                img = Image.open(io.BytesIO(img_response.content))
                st.image(img, caption="Processed Image", use_column_width=True)

                # Display vehicle counts
                st.subheader("🚗 Detected Vehicles:")
                for vehicle, count in data["vehicle_counts"].items():
                    st.write(f"**{vehicle.capitalize()}:** {count}")

                # Show detection details
                st.subheader("🔍 Detection Details:")
                for det in data["detection_details"]:
                    st.write(f"**{det['label']}** - Confidence: {det['confidence']} - Coords: {det['coordinates']}")

                # Display estimated signal time
                if "signal_time" in data:
                    st.subheader("⏳ Estimated Signal Time:")
                    st.write(f"🚦 **{data['signal_time']} seconds**")
                else:
                    st.warning("🚦 Signal time not available.")

            else:
                st.error("Failed to load processed image. Check backend response.")

        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Error: Could not connect to backend. Ensure Flask server is running.")

    except Exception as e:
        st.error(f"⚠️ Unexpected error: {str(e)}")
