import os
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import logging
from io import BytesIO

app = Flask(__name__)
app.config["ALLOWED_EXTENSIONS"] = set(["png", "jpg", "jpeg"])
app.config["UPLOAD_FOLDER"] = "static/uploads/"

app.logger.setLevel(logging.DEBUG)

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# Load pre-trained model
model = load_model("Model_Complete_Test_New.h5", compile=False)
with open("labels.txt", "r") as file:
    class_names = file.read().splitlines()

def predict_image_class(image_bytes):
    # Process the uploaded image
    image = Image.open(BytesIO(image_bytes))
    image = image.resize((299, 299)) 
    image_array = np.array(image) / 255.0 

    # Preprocess the image
    image_array = image_array.astype(np.float32)
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Use the model to predict the class probabilities
    predictions = model.predict(image_array)

    # Convert the probabilities to class labels
    predicted_class_index = np.argmax(predictions, axis=1)
    predicted_class = class_names[predicted_class_index[0]]

    confidence_scores = {class_names[i]: float(predictions[0][i]) for i in range(len(class_names))}

    return predicted_class, confidence_scores

@app.route('/')
def index():
    return jsonify({
        'status': {
            'code': 200,
            'message': 'Success fetching the API'
        },
        "data": None
    }), 200

@app.route("/prediction", methods=["POST"])
def prediction():
    try:
        if request.method == "POST":
            image = request.files["image"]

            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                
                predicted_class, confidence_scores = predict_image_class(image.read())
                
                image.save(image_path)

                return jsonify({
                    'status': {
                        'code': 200,
                        'message': 'Success fetching the API'
                    },
                    "data": {
                        "predicted_class": predicted_class,
                        "confidence_scores": confidence_scores
                    }
                }), 200
            else:
                return jsonify({
                    'status': {
                        'code': 400,
                        'message': 'Client side error: Invalid file format'
                    },
                    "data": None
                }), 400
        else:
            return jsonify({
                'status': {
                    'code': 405,
                    'message': 'Method Not Allowed'
                },
                "data": None
            }), 405
            
    except Exception as e:
        app.logger.error("Error during inference: %s", e)

        return jsonify({
            'status': {
                'code': 500,
                'message': 'Internal Server Error'
            },
            "data": None
        }), 500
        
upload_folder = app.config["UPLOAD_FOLDER"]
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

if __name__ == '__main__':
    app.run(debug=True)
