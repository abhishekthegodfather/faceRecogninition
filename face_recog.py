import face_recognition
from rembg import remove
import cv2
import numpy as np
from PIL import Image, ImageOps
import pickle
import os


def processImgAndTeach(images):
    person_encodings = []   
    for image in images:
        pil_image = Image.open(image)
        np_image = np.array(pil_image)
        cv2_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)

        image = cv2.rotate(cv2_image, cv2.ROTATE_90_CLOCKWISE)
        image = remove(image)
        desired_width = 640
        aspect_ratio = image.shape[1] / image.shape[0]
        desired_height = int(desired_width / aspect_ratio)
        image = cv2.resize(image, (desired_width, desired_height))
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        equalized_image = cv2.equalizeHist(gray_image)
        blurred_image = cv2.GaussianBlur(equalized_image, (5, 5), 0)
        rgbImage = cv2.cvtColor(blurred_image, cv2.COLOR_GRAY2RGB)


        face_locations = face_recognition.face_locations(rgbImage, model='hog')
        print(face_locations)
        face_encodings = []
        if len(face_locations) == 0:
            continue
        elif len(face_locations) > 1:
            continue
        else:
            for (top, right, bottom, left) in face_locations:
                face_image = rgbImage[top:bottom, left:right]
                resized_face_image = cv2.resize(face_image, (128, 128))
                resized_face_image_rgb = cv2.cvtColor(resized_face_image, cv2.COLOR_BGR2RGB)
                face_encoding = face_recognition.face_encodings(resized_face_image_rgb)[0]
                face_encodings.append(face_encoding)

            person_encodings.append(face_encodings)

    return person_encodings


def compareImage(image):
    print(image)
    pil_image = Image.open(image)
    np_image = np.array(pil_image)
    cv2_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
    image = cv2.rotate(cv2_image, cv2.ROTATE_90_CLOCKWISE)
    image = remove(image)
    desired_width = 640
    aspect_ratio = image.shape[1] / image.shape[0]
    desired_height = int(desired_width / aspect_ratio)
    image = cv2.resize(image, (desired_width, desired_height))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized_image = cv2.equalizeHist(gray_image)
    blurred_image = cv2.GaussianBlur(equalized_image, (5, 5), 0)
    rgbImage = cv2.cvtColor(blurred_image, cv2.COLOR_GRAY2RGB)
    cv2.imwrite('result.png', rgbImage)

    face_locations = face_recognition.face_locations(rgbImage, model='hog')
    print(face_locations)
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
            face_image = rgbImage[top:bottom, left:right]
            resized_face_image = cv2.resize(face_image, (128, 128))
            face_encoding = face_recognition.face_encodings(resized_face_image)[0]
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
                        if any(face_distances >= 0 and face_distances <= 0.35):
                            pickle_file_matches = file_name.split(".")
                            pickle_file_matches = pickle_file_matches[0]
                            resultItem = {
                                "status" : True,
                                "message" : "Face Found",
                                "emp_code" : pickle_file_matches
                            }
                            return resultItem 

        resultItem = {
            "status" : False,
            "message" : "No Match Found"
        }
        return resultItem

    

