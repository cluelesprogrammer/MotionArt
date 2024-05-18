from flask import Flask, request, jsonify
import base64
from PIL import Image
import logging
import io


app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:%(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(file_handler)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/upload_image', methods=['POST'])
def upload_image():
    logger.debug('upload image accessed')
    try:
        data = request.get_json()
        image_data = data['image']

        # Remove the "data:image/png;base64," part
        image_data = image_data.split(",")[1]

        # Decode the base64 string to bytes
        image_bytes = base64.b64decode(image_data)

        # Save the image
        with open("captured_image.png", "wb") as image_file:
            image_file.write(image_bytes)

        return jsonify({'message': 'Image uploaded successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
