import cv2

def preprocess_image(image_path):
    """Resize and enhance image for better YOLO detection."""
    img = cv2.imread(image_path)
    img_resized = cv2.resize(img, (640, 640))  # Resize to YOLOv8 input size
    return img_resized
