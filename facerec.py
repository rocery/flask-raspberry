import os
import cv2
import numpy as np
import argparse
import warnings
import time
import face_recognition
import pickle
from PIL import Image, ImageDraw, ImageFont

from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name
warnings.filterwarnings('ignore')

def liveness_check(frame, model_dir, device_id):
    model_test = AntiSpoofPredict(device_id)
    image_cropper = CropImage()
    liveness_result = []
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    
    if len(face_locations) == 0:
        return []
    
    for face_location in face_locations:
        top, right, bottom, left = face_location
        image_bbox = [left, top, right - left, bottom - top]
        prediction = np.zeros((1, 3))
        
        for model_name in os.listdir(model_dir):
            h_input, w_input, model_type, scale = parse_model_name(model_name)
            param = {
                "org_img": frame,
                "bbox": image_bbox,
                "scale": scale,
                "out_w": w_input,
                "out_h": h_input,
                "crop": True,
            }
            if scale is None:
                param["crop"] = False
            img = image_cropper.crop(**param)
            prediction += model_test.predict(img, os.path.join(model_dir, model_name))
            
        label = np.argmax(prediction)
        value = prediction[0][label] / 2
        
        lab_val = (label, value, face_location)
        liveness_result.append(lab_val)
    
    return liveness_result

def predict(X_frame, knn_clf = None, model_path = None, distance_threshold = 0.5):
    if knn_clf is None and model_path is None:
        raise Exception("File Encoding Tidak Ditemukan")