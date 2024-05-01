import os
import cv2
import numpy as np
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import torch
from ultralytics import YOLO
import cloudinary
from cloudinary.uploader import upload
from PIL import Image, ImageDraw, ImageFont
import time

app = Flask(__name__)
CORS(app)

# Configure Cloudinary
cloudinary.config( 
    cloud_name="diykglllj", 
    api_key="239345618852227", 
    api_secret="JE2QGH1j-g9aqwL5unkSXVEiTDg"
)

def count_person_bounding_boxes(detections):
    # Count only the bounding boxes for persons
    return len(detections[0])

def count_weapon_bounding_boxes(detections):
    # Count only the bounding boxes for weapons
    return len(detections[1])

def track_bounding_boxes(detections):
    # Implement your tracking logic here
    # This function should return the number of tracked bounding boxes
    # For now, let's return the same count as detected bounding boxes
    return count_person_bounding_boxes(detections)

def alert_function(num_weapon_boxes):
    # Implement your alert function here
    if num_weapon_boxes > 0:
        # Trigger an alert
        return True
    else:
        return False

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.mp4'):
        # Save uploaded video
        video_path = "temp.mp4"
        file.save(video_path)

        # Process video frames
        processed_video_url, last_frame_url, processed_public_id, message = process_video(video_path)

        return jsonify({'processed_video_url': processed_video_url, 'last_frame_url': last_frame_url, 'processed_public_id': processed_public_id, 'message': message}), 200

    else:
        return jsonify({'error': 'Invalid file format. Please upload a .mp4 file'}), 400

@app.route('/webcam', methods=['POST'])
def process_webcam():
    # Capture video from webcam
    cap = cv2.VideoCapture(0)

    # Get original video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

    # Set the processing duration to 30 seconds
    processing_duration = 30  # in seconds
    start_time = time.time()
    
    # Process video frames
    processed_video_url, last_frame_url, processed_public_id, message = process_video(cap, processing_duration, start_time, frame_width, frame_height, frame_rate)

    # Release the VideoCapture object
    cap.release()

    return jsonify({'processed_video_url': processed_video_url, 'last_frame_url': last_frame_url, 'processed_public_id': processed_public_id, 'message': message}), 200

def process_video(video_source, processing_duration=None, start_time=None, input_width=None, input_height=None, frame_rate=None):
    if isinstance(video_source, str):
        # If video source is a file path
        cap = cv2.VideoCapture(video_source)
        video_type = 'file'
    else:
        # If video source is a VideoCapture object (webcam)
        cap = video_source
        video_type = 'webcam'

    if input_width is None or input_height is None or frame_rate is None:
        # Get original video properties
        input_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        input_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

    # Define output video dimensions
    output_width = input_width
    output_height = input_height

    # Create a list to store processed frames
    processed_frames = []

    # Create a folder to save processed frames
    frame_folder = os.path.join(os.getcwd(), "InteligentGuardReact", "frames")
    os.makedirs(frame_folder, exist_ok=True)

    # Define font and text position for annotations
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_position = (10, 20)
    font_scale = 0.6
    font_color = (255, 255, 255)
    line_type = 2

    # Load YOLO models for person and weapon detection
    yolo_person = YOLO('best.pt')  # for detecting persons
    yolo_weapon = YOLO('wappon.pt')  # for detecting weapons

    # Check if CUDA is available
    if torch.cuda.is_available():
        yolo_person.model.cuda()
        yolo_weapon.model.cuda()

    # Process video frames and perform detection
    frame_count = 0
    last_frame_url = None  # Initialize last frame URL
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform detection on the frame
        image = np.array(frame)

        # Detect persons
        detections_person = yolo_person.predict(image, save=False)

        # Detect weapons
        detections_weapon = yolo_weapon.predict(image, save=False)

        # Combine detections
        detections = [detections_person[0], detections_weapon[0]]

        num_person_boxes = count_person_bounding_boxes(detections)
        num_weapon_boxes = count_weapon_bounding_boxes(detections)

        # Trigger alert function if weapons are detected
        alert_triggered = alert_function(num_weapon_boxes)

        # Track bounding boxes
        num_tracked_boxes = track_bounding_boxes(detections)

        # Plot bounding boxes on the frame for persons
        res_plotted_person = detections[0].plot()
        frame_with_boxes_person = np.array(res_plotted_person)

        # Plot bounding boxes on the frame for weapons
        res_plotted_weapon = detections[1].plot()
        frame_with_boxes_weapon = np.array(res_plotted_weapon)

        # Combine frames with bounding boxes for persons and weapons
        frame_with_boxes = frame_with_boxes_person + frame_with_boxes_weapon

        # Add text annotations to the frame
        image_with_text = Image.fromarray(frame_with_boxes)
        draw = ImageDraw.Draw(image_with_text)
        text = f"PERSONS: {num_person_boxes}, TRACKED PERSONS: {num_tracked_boxes}"
        font = ImageFont.truetype("arial.ttf", 30)
        draw.text(text_position, text, font=font, fill=(255, 255, 255))

        # Display an alert if triggered
        if alert_triggered:
            alert_text = "WEAPON DETECTED!"
            draw.text((70, 50), alert_text, font=font, fill=(300, 300, 255))

        # Convert back to numpy array
        frame_with_boxes = np.array(image_with_text)

        # Resize the frame
        frame_with_boxes_resized = cv2.resize(frame_with_boxes, (output_width, output_height))

        # Append processed frame to list
        processed_frames.append(frame_with_boxes_resized)

        # Save processed frame to the frames folder
        frame_path = os.path.join(frame_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_path, frame_with_boxes_resized)

        frame_count += 1

        # Check if processing duration exceeded
        if processing_duration and time.time() - start_time > processing_duration:
            break

    # Upload last processed frame to Cloudinary
    last_frame_path = os.path.join(frame_folder, f"frame_{frame_count - 1}.jpg")
    cloudinary_response_frame = upload(last_frame_path, resource_type="image")
    last_frame_url = cloudinary_response_frame['secure_url']

    # Release the VideoCapture object if it's a file
    if video_type == 'file':
        cap.release()

    # Save the processed frames as a video file
    output_video_path = os.path.join(frame_folder, "processed_video.mp4")
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (output_width, output_height))
    for frame in processed_frames:
        out.write(frame)
    out.release()

    # Upload video to Cloudinary
    cloudinary_response = upload(output_video_path, resource_type="video")

    # Get URL for the processed video from Cloudinary response
    processed_video_url = cloudinary_response['secure_url']
    processed_public_id = cloudinary_response['public_id']
    return processed_video_url, last_frame_url, processed_public_id, 'Video processed successfully'

from flask import send_file
from flask import send_file

@app.route('/video')
def get_video():
    video_path = 'C:/Users/ARX56/OneDrive/Desktop/InteligentGuardReact/InteligentGuardReact/frames/processed_video.mp4'
    return send_file(video_path, mimetype='video/mp4', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
