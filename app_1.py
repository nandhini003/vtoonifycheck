from PIL import Image
from flask import Flask, request, jsonify
from google.cloud import storage
from vtoonify_model import Model
import numpy as np
from PIL import Image
from io import BytesIO
import torch
import os

def main(input_image_path):
    # Open the image file
    with Image.open(input_image_path) as img:
        # Display the image
        img.show()
    model = Model(device='cuda' if torch.cuda.is_available() else 'cpu')
    model.load_model('cartoon1')
    print("[Loading Model]")

if __name__ == '__main__':
    # Hardcoded image path
    app = Flask(__name__)
    # port = int(os.environ.get('PORT', 8080))
    # app.run(host='0.0.0.0', port=port)
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)
    input_image_path = "gs://flowerimage03/Flower.jpeg"
    print(input_image_path)
    main(input_image_path)