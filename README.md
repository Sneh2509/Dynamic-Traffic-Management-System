🚦 Dynamic Traffic Management System
An AI-based system for detecting vehicles and calculating adaptive traffic signal timings using YOLOv8 and OpenCV. The interface is built using Streamlit for easy interaction.

🛠️ Tech Stack
Object Detection: YOLOv8
Image Processing: OpenCV
Interface & Deployment: Streamli
Programming Language: Python

🚗 Key Features
Vehicle detection and classification (car, bike, bus, truck) from uploaded images
Real-time traffic density estimation based on vehicle count
Adaptive signal timing calculation based on detected traffic load
Streamlit-powered web interface for easy image uploads and result visualization
Traffic category-wise vehicle count display (cars, bikes, buses, trucks)

⚙️ How It Works
User uploads a traffic image via the Streamlit web interface.
YOLOv8 processes the image and detects all visible vehicles.
Based on the number and type of vehicles detected, an adaptive traffic signal time is calculated using a predefined rule.
Output includes total vehicle count, category-wise distribution, and the recommended signal time.

