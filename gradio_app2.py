## NOTE:-  This app2 is added later on, this is not a part of the main tutorial in my youtube video.

import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import gradio as gr
import cv2 
import os

MODEL_PATH = os.path.join(os.getcwd(), 'models', 'apple-224.h5')
model = load_model(MODEL_PATH)

def classify_image(test_image):
    test_image = cv2.resize(test_image, (224, 224))
    test_image = test_image/255
    test_image = np.expand_dims(test_image, axis = 0)
    result = model.predict(test_image)
    # print(np.argmax(result,axis=1))
    categories = ['healthy', 'multiple diseases', 'rust', 'scab']
    return categories[np.argmax(result)]



gr.Interface(fn=classify_image,
             inputs=gr.Image(),
             outputs=gr.Label(num_top_classes = 3),
             examples=["images/train/healthy/Train_2.jpg", "images/train/rust/Train_10.jpg", "images/train/scab/Train_16.jpg"]).launch()
