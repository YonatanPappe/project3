import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import math

# Constants
DESIRED_HEIGHT = 480
DESIRED_WIDTH = 480

def resize_and_show(image):
    h, w = image.shape[:2]
    if h < w:
        img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
    else:
        img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preprocess_image(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(lab)
    l = cv2.add(l, 10)  # Increase brightness
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_Lab2BGR)

def postprocess_image(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(lab)
    l = cv2.add(l, 10)  # Increase brightness
    lab = cv2.merge([l, a, b])
    return cv2.cvtColor(lab, cv2.COLOR_Lab2BGR)

input_image_filename = r'project3\src\project3\similing_woman.jpeg'
output_image_filename = r'project3\src\project3\smiling_cartoon.png'
file_path = r'project3\face_stylizer.task'

# Load the image
image = cv2.imread(input_image_filename)
if image is None:
    raise FileNotFoundError(f"Image file '{input_image_filename}' not found.")

# Preprocess image
preprocessed_image = preprocess_image(image)

# Face stylization setup
try:
    with open(file_path, 'rb') as f:
        model_data = f.read()
    base_options = python.BaseOptions(model_asset_buffer=model_data)
    options = vision.FaceStylizerOptions(base_options=base_options)
    with vision.FaceStylizer.create_from_options(options) as stylizer:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=preprocessed_image)
        stylized_image = stylizer.stylize(mp_image)
        rgb_stylized_image = cv2.cvtColor(stylized_image.numpy_view(), cv2.COLOR_BGR2RGB)
        # Postprocess the stylized image
        final_image = postprocess_image(rgb_stylized_image)
        cv2.imwrite(output_image_filename, final_image)
        resize_and_show(final_image)
    print("Face stylization successful with model_asset_buffer.")
except Exception as e:
    print(f"Error with model_asset_buffer: {e}")
