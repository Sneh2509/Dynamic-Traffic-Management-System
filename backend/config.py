import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "upload")
DATABASE_PATH = os.path.join(BASE_DIR, "traffic_data.db")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
