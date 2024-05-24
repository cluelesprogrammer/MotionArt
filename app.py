from flask import Flask, request, jsonify
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

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

# Global variables for the model and inference results
body_estimation = None
#latest_result = None
#inference_interval = 0.3  # 300 milliseconds

@app.route('/')
def index():
    return 'Hello, World!'

def load_model():
    global body_estimation 
    body_estimation=Body('openpose_models/body_pose_model.pth')

@app.route('/process_image', methods=['POST'])
def process_image():
    logger.debug('function evoked')
    try:
        #logger.debug(request.content_type)
        #logger.debug(request.data)
        #data = request.data
        data = request.get_json(force=True)  # force=True ensures JSON parsing
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Convert byte data to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)

        # Decode image
        img = np.array(cv2.imdecode(nparr, cv2.IMREAD_COLOR))
        logger.debug('before inference')
        candidate, subset = body_estimation(img, logger)
        logger.debug('body estimation inference worked')

        canvas = util.draw_bodypose(img, candidate, subset)
        logger.debug('drawing bodypose worked')

        # Encode image back to base64
        _, buffer = cv2.imencode('.jpg', canvas)
        processed_image_data = base64.b64encode(buffer).decode('utf-8')
        processed_image_url = f"data:image/jpeg;base64,{processed_image_data}"

        return jsonify({'processed_image': processed_image_url})
    
    except Exception as e:
        logger.debug(type(body_estimation))
        logger.debug(body_estimation==None)
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
    load_model()
    app.run(debug=True)
  
    """
    inference_thread = threading.Thread(target=run_inference)
    inference_thread.daemon = True
    inference_thread.start()
    """
    