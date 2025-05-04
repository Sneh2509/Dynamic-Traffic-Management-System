import cv2
import numpy as np
import os

def generate_heatmap(image_path, results):
    """Generates a heatmap based on detected vehicle locations."""
    img = cv2.imread(image_path)
    heatmap = np.zeros_like(img[:, :, 0], dtype=np.float32)

    for r in results:
        for box in r.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            heatmap[y1:y2, x1:x2] += 1

    heatmap = (heatmap / np.max(heatmap) * 255).astype(np.uint8)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
    heatmap_path = image_path.replace(".jpg", "_heatmap.jpg")
    cv2.imwrite(heatmap_path, overlay)

    return heatmap_path
