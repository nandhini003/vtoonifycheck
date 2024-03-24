from flask import Flask, request, jsonify
from google.cloud import storage
from vtoonify_model import Model
import numpy as np
from PIL import Image
from io import BytesIO
import torch
import os
import yaml

# Load config file
current_path = os.getcwd()
path_to_yaml = os.path.join(current_path, 'vtoonify.yml')
print(path_to_yaml)
try:
    with open(path_to_yaml, 'r') as c_file:
        config = yaml.safe_load(c_file)
except Exception as e:
    print('Error reading the config file')

app = Flask(__name__)


@app.route('/image_toonify', methods=['POST'])
def image_toonify():
    # Get parameters from request
    aligned_face_path = request.json.get('aligned_face_path', 'default_aligned_face_path')
    instyle = request.json.get('instyle', 'default_instyle')
    exstyle = request.json.get('exstyle', 'default_exstyle')
    style_degree = request.json.get('style_degree', 'default_style_degree')
    style_type = request.json.get('style_type', 'default_style_type')

    # Load model
    model = Model(device='cuda' if torch.cuda.is_available() else 'cpu')
    model.load_model('cartoon1')

    # Read the aligned face from GCS
    input_path = "gs://flowerimage03/Flower.jpeg"
    bucket_name, blob_name = input_path.replace("gs://", "").split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    aligned_face = np.array(Image.open(BytesIO(blob.download_as_bytes())))

    # Make prediction
    result_face = model.image_toonify(aligned_face, instyle, exstyle, style_degree, style_type)

    # Save the result to GCS
    output_path = request.json.get('output_path', 'default_output_path')
    output_bucket_name, output_blob_name = output_path.replace("gs://", "").split("/", 1)
    output_bucket = storage_client.bucket(output_bucket_name)
    output_blob = output_bucket.blob(output_blob_name)
    output_blob.upload_from_string(Image.fromarray(result_face).tobytes())

    # Return result
    return jsonify({'message': 'Image saved to {}'.format(output_path)})

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)