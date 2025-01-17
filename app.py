import os
import requests
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import logging
from io import BytesIO

from flask_httpauth import HTTPTokenAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from errors import bp as errors_bp

app = Flask(__name__)
# Register the blueprint for error handling
app.register_blueprint(errors_bp)

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

app.config["ALLOWED_EXTENSIONS"] = set(["png", "jpg", "jpeg"])
app.config["UPLOAD_FOLDER"] = "static/uploads/"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

auth = HTTPTokenAuth(scheme='Bearer')
app.logger.setLevel(logging.DEBUG)

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
        
#Authentication
@auth.verify_token
def verify_token(token):
    return app.config["SECRET_KEY"] == token

@auth.error_handler
def unauthorized():
    return {
        "status": {
            "code": 401,
            "message": "Unauthorized Access!"
        },
        "data": None,
    }, 401 

# Load pre-trained model
model = load_model("Model_Complete_Test_New.h5", compile=False)
with open("labels.txt", "r") as file:
    class_names = file.read().splitlines()

def predict_image_class(image_bytes):
    # Process the uploaded image
    image = Image.open(BytesIO(image_bytes))
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
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
@auth.login_required
@limiter.limit("20 per hour")
def index():
    return jsonify({
        'status': {
            'code': 200,
            'message': 'Success fetching the API'
        },
        "data": None
    }), 200

@app.route("/prediction", methods=["POST"])
@auth.login_required
@limiter.limit("20 per hour")
def prediction():
    try:
        if request.method == "POST":
            if "image" in request.files:
                image = request.files["image"]

                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

                    predicted_class, confidence_scores = predict_image_class(image.read())

                    image.save(image_path)
                    
                    if predicted_class == "Blur":
                        accepted = False
                    elif predicted_class == "Bokeh" or predicted_class == "Normal":
                        accepted = True

                    return jsonify({
                        'status': {
                            'code': 200,
                            'message': 'Success fetching the API'
                        },
                        "data": {
                            "predicted_class": predicted_class,
                            "confidence_scores": confidence_scores,
                            "accepted": accepted
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

            elif "image_url" in request.json:
                image_url = request.json["image_url"]
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_bytes = response.content

                    predicted_class, confidence_scores = predict_image_class(image_bytes)
                    
                    if predicted_class == "Blur":
                        accepted = False
                    elif predicted_class == "Bokeh" or predicted_class == "Normal":
                        accepted = True

                    return jsonify({
                        'status': {
                            'code': 200,
                            'message': 'Success fetching the API'
                        },
                        "data": {
                            "predicted_class": predicted_class,
                            "confidence_scores": confidence_scores,
                            "accepted": accepted
                        }
                    }), 200
                else:
                    return jsonify({
                        'status': {
                            'code': 400,
                            'message': 'Client side error: Invalid image URL or format'
                        },
                        "data": None
                    }), 400
            else:
                return jsonify({
                    'status': {
                        'code': 400,
                        'message': 'Client side error: No image or URL provided'
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
