import os
import sys
from flask import Flask, request, jsonify, send_file
import cv2
import torch
from ultralytics import YOLO
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import utilities
from backend.utils.heatmap import generate_heatmap
from backend.utils.tracking import track_vehicles
from backend.utils.signal_timing import predict_signal_time
from backend import database

# Directories
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "upload")
PROCESSED_FOLDER = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Load Pretrained YOLOv8 Model
model_path = os.path.join(os.path.dirname(__file__), "..", "models", "yolov8n.pt")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")
model = YOLO(model_path)

# Define vehicle weight factors for timing calculation
VEHICLE_WEIGHTS = {
    "car": 1,
    "bike": 0.5,
    "bus": 2,
    "truck": 2.5
}

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles image uploads, processes with YOLO, and returns the processed image and results."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Process Image using YOLO
    result_path, vehicle_counts, detection_details = process_image(file_path)

    # Calculate signal timing based on vehicle types
    signal_time = calculate_signal_time(vehicle_counts)

    # Save results to the database
    database.save_results(vehicle_counts, signal_time)

    # Create response
    response = {
        "image_path": f"/processed/{os.path.basename(result_path)}",
        "vehicle_counts": vehicle_counts,
        "detection_details": detection_details,
        "signal_time": signal_time  # Ensure signal timing is included
    }

    print("🚦 API Response:", response)  # Debugging: Check if signal_time is in response

    return jsonify(response)

@app.route('/processed/<filename>')
def get_processed_image(filename):
    """Serves the processed image to the frontend."""
    processed_path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(processed_path):
        return send_file(processed_path, mimetype='image/jpeg')
    return jsonify({"error": "Processed image not found"}), 404


def process_image(image_path):
    """Runs YOLOv8 on an image and returns processed image & detection details."""
    img = cv2.imread(image_path)
    results = model(img)

    # Initialize vehicle counts
    vehicle_counts = {"car": 0, "bus": 0, "truck": 0, "bike": 0}

    detection_details = []
    for r in results:
        for box, cls, conf in zip(r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
            label = model.names[int(cls)]
            if label in vehicle_counts:
                vehicle_counts[label] += 1

            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Save detected object info
            detection_details.append({
                "label": label,
                "coordinates": [x1, y1, x2, y2],
                "confidence": round(float(conf), 2)
            })

    # Save processed image
    processed_image_path = os.path.join(PROCESSED_FOLDER, os.path.basename(image_path))
    cv2.imwrite(processed_image_path, img)

    return processed_image_path, vehicle_counts, detection_details


def calculate_signal_time(vehicle_counts):
    """Calculates traffic signal timing based on detected vehicles and weights."""
    effective_count = sum(VEHICLE_WEIGHTS.get(v_type, 1) * count for v_type, count in vehicle_counts.items())

    # Assign green signal time based on effective vehicle count
    if effective_count <= 10:
        return 30
    elif effective_count <= 25:
        return 45
    else:
        return 60


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5008)
