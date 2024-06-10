from flask import Flask, request, jsonify, render_template
import base64
from PIL import Image
import logging
import threading
import io
from flask_cors import CORS
import numpy as np
import cv2
from model import bodypose_model
from body import Body
import torch
import util
from time import time
from load_model import body_estimation
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

#latest_result = None
#inference_interval = 0.3  # 300 milliseconds

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/')
def index():
    return render_template('index.html')

def load_model():
    logger.debug('load model function')
    global body_estimation
    body_estimation=Body('openpose_models/body_pose_model.pth')

@socketio.on('frame')
def process_image(data_image):
    logger.debug('function evoked')
    try:
        sbuf = io.StringIO()
        sbuf.write(data_image)
        
        # Step 1: Decode the base64 string to bytes
        image_bytes = base64.b64decode(data_image)

        # Step 2: Convert bytes to a BytesIO object
        image_stream = io.BytesIO(image_bytes)

        # Step 3: Read the BytesIO object into a NumPy array
        image_array = np.frombuffer(image_stream.getvalue(), dtype=np.uint8)

        # Step 4: Decode the NumPy array to an image using OpenCV
        img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        candidate, subset = body_estimation(img)
        canvas = util.draw_bodypose(img, candidate, subset)
        
        # Encode image back to base64
        _, buffer = cv2.imencode('.jpg', canvas)
        processed_image_str = base64.b64encode(buffer).decode('utf-8')
        processed_image_data = f"data:image/jpeg;base64,{processed_image_str}"
        emit('processed_frame', {'processed_image': processed_image_data})
    except Exception as e:
        logger.debug('some error is occuring')
        return jsonify({'error': str(e)}), 400

"""
def run_inference():
    global latest_result
    while True:
        # Simulate image capture from a camera
        image_data = capture_image_from_camera()

        # Preprocess the image
        input_tensor = preprocess_image(image_data)

        # Perform inference
        with torch.no_grad():
            output = model(input_tensor)
            latest_result = output

        # Wait for the next inference
        time.sleep(inference_interval)


@app.route('/inference', methods=['GET'])
def get_inference():
    global latest_result
    if latest_result is not None:
        # Convert the result to a JSON-serializable format
        result = latest_result.numpy().tolist()
        return jsonify(result)
    else:
        return jsonify({"error": "No inference result available"}), 500

"""

if __name__ == '__main__':
    socketio.run(app, port=8000)
    """
    , host='0.0.0.0',
    inference_thread = threading.Thread(target=run_inference)
    inference_thread.daemon = True
    inference_thread.start()
    """
    