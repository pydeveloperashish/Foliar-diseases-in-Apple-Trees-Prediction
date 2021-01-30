from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
#from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/apple-224.h5'

# Load your trained model
model = load_model(MODEL_PATH)


def model_predict(img_path, model):
    test_image = image.load_img(img_path, target_size=(224, 224))

    #test_image = image.load_img(test_image_single, target_size=(224, 224))
    test_image = image.img_to_array(test_image)
    test_image = test_image / 255
    test_image = np.expand_dims(test_image, axis=0)
    result = model.predict(test_image)
    return result



@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(os.path.realpath('__file__'))
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        result = model_predict(file_path, model)
        categories = ['healthy', 'multiple diseases', 'rust', 'scab']


        # Process your result for human
        pred_class = result.argmax(axis=-1)            # Simple argmax
        #print(pred_class)

        #pred_class = decode_predictions(preds, top=1)    #ImageNet Decode
        result = pred_class[0]
        status=categories[result]
        print(status)
        return status
    return None


if __name__ == '__main__':
    app.run(debug=False,port=1667)

