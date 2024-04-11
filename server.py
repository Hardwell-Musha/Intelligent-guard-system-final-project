from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
import cv2
from PIL import Image
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for your Flask app

# Load YOLO model
yolo = YOLO('C://Users//ARX56//OneDrive//Desktop//Intelligent guard react app//best.pt')

# Path to save the processed video
output_folder = 'C://Users//ARX56//OneDrive//Desktop//Intelligent guard react app//client//processedvideo'
os.makedirs(output_folder, exist_ok=True)
output_video_path = os.path.join(output_folder, 'processedvideo.mp4')  # Specify the output video file with .mp4 extension

# Path to save the frames
frames_folder = 'C:\\Users\\ARX56\\OneDrive\\Desktop\\Intelligent guard react app\\frames'
os.makedirs(frames_folder, exist_ok=True)

def process_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to an image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Perform object detection using YOLO
        detections = yolo.predict(image, save=False)
        res_plotted = detections[0].plot()

        # Convert the result to a numpy array
        np_image = np.array(res_plotted)

        # Write the frame to the output video file
        out.write(cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR))

        # Save the frame as an image
        frame_path = os.path.join(frames_folder, f'frame_{frame_count}.jpg')
        cv2.imwrite(frame_path, cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR))
        frame_count += 1

    # Release resources
    cap.release()
    out.release()

@app.route('/process-video', methods=['POST'])
def process_video_route():
    try:
        # Get the uploaded video file
        video_file = request.files['file']
        
        # Save the uploaded video to a temporary file
        video_path = 'temp_video.mp4'
        video_file.save(video_path)

        # Process the video frames
        process_frames(video_path)

        # Return success response with JSON data
        return jsonify({'videoUrl': 'http://localhost:5000/processed-video.mp4'}), 200

    except Exception as e:
        # Return error message
        return str(e), 500

@app.route('/processed-video-url', methods=['GET'])
def get_processed_video_url():
    try:
        # Return the processed video URL as a response
        return jsonify({'videoUrl': 'http://localhost:5000/processed-video.mp4'}), 200

    except Exception as e:
        # Return error message
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
