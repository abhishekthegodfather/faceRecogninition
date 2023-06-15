import face_recognition
from rembg import remove
import cv2
import numpy as np
from PIL import Image
import pickle
import os


def processImgAndTeach(images):
    person_encodings = []   
    for image in images:
        pil_image = Image.open(image)
        np_image = np.array(pil_image)
        cv2_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
        removed_background_image = remove(cv2_image)
        rgb_image = cv2.cvtColor(removed_background_image, cv2.COLOR_RGBA2RGB)
        face_locations = face_recognition.face_locations(rgb_image, model='hog')
        face_encodings = []
        if len(face_locations) == 0:
            continue
        elif len(face_locations) > 1:
            continue
        else:
            for (top, right, bottom, left) in face_locations:
                face_image = rgb_image[top:bottom, left:right]
                resized_face_image = cv2.resize(face_image, (128, 128))
                resized_face_image_rgb = cv2.cvtColor(resized_face_image, cv2.COLOR_BGR2RGB)
                face_encoding = face_recognition.face_encodings(resized_face_image_rgb)[0]
                face_encodings.append(face_encoding)

            person_encodings.append(face_encodings)

    return person_encodings


def compareImage(image):
    pil_image = Image.open(image)
    np_image = np.array(pil_image)
    cv2_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
    removed_background_image = remove(cv2_image)
    rgb_image = cv2.cvtColor(removed_background_image, cv2.COLOR_RGBA2RGB)
    face_locations = face_recognition.face_locations(rgb_image, model='hog')
    resultItem = dict()
    if len(face_locations) == 0:
        resultItem = {
            "status" : False,
            "message" : "No Face Found"
        }
        return resultItem
    elif len(face_locations) > 1:
        resultItem = {
            "status" : False,
            "message" : "Multiple Face Found"
        }
        return resultItem
    else:
        face_encodings = []
        for (top, right, bottom, left) in face_locations:
            face_image = rgb_image[top:bottom, left:right]
            resized_face_image = cv2.resize(face_image, (128, 128))
            resized_face_image_rgb = cv2.cvtColor(resized_face_image, cv2.COLOR_BGR2RGB)
            face_encoding = face_recognition.face_encodings(resized_face_image_rgb)[0]
            face_encodings.append(face_encoding)
        pickle_file_matches = ""
        knownFaceEncodingFolder = "/Users/Cubastion/Desktop/django_apis/biometricApis/known_face_encoding"
        for file_name in os.listdir(knownFaceEncodingFolder):
            if file_name.endswith(".pickle"):
                pickle_path = os.path.join(knownFaceEncodingFolder, file_name)
                with open(pickle_path, 'rb') as f:
                    stored_encodings = pickle.load(f)
                    for stored_encoding in stored_encodings:
                        face_distances = face_recognition.face_distance(stored_encoding, face_encodings)
                        threshold = 0.6
                        if any(face_distances <= threshold):
                            pickle_file_matches = file_name
                            resultItem = {
                                "status" : True,
                                "message" : "Face Found",
                                "emp_code" : pickle_file_matches
                            }
                            
                            return resultItem 

        resultItem = {
            "status" : False,
            "message" : "No Face Model Found For this Employee"
        }
        return resultItem

    

