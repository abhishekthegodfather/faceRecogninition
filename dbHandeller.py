from mysql.connector import connect
from datetime import date
import numpy as np
import serializers as sr
import face_recog as fr
import pickle
from PIL import Image
import profile_pic as pp
import os

class DBHandler:
    def getEmployeeDetails(emp_code):
        resultItem = dict()
        dbConnect = DBConnectorHandler.DBconnector()
        cursor = dbConnect.cursor()
        requiredQuery = "SELECT first_name, last_name, emp_code, emp_status, profile_pic_url FROM devbiometricDB WHERE emp_code = %s"
        try:
            cursor.execute(requiredQuery, (emp_code,))
            result = cursor.fetchone() 
            if result is None:
                print("Failed to get user from DB")
                resultItem = {
                    "status" : False,
                    "Result" : "Failed to get user"
                }
                return resultItem
            else:
                print("Sucess to get user from DB")
                single_employee = sr.EmployeeModel(result[0], result[1], result[2], result[3], result[4])
                resultItem = {
                    "status" : True,
                    "Result" : {
                        "first_name": single_employee.first_name,
                        "last_name" : single_employee.last_name,
                        "emp_code" : single_employee.emp_code,
                        "emp_status" : single_employee.emp_status,
                        "profile_pic" : single_employee.profile_url
                    }
                }
                return resultItem
        except Exception as e:
            print("Failed to get user")
            resultItem = {
                    "status" : False,
                    "Result" : "Failed to get user"
                }
            return resultItem
        
    def deleteUserFromDB(emp_code):
        resultItem = dict()
        dbConnect = DBConnectorHandler.DBconnector()
        cursor = dbConnect.cursor()
        requirdQuery = "DELETE FROM devbiometricDB WHERE emp_code = %s"
        known_face_folder = "/Users/Cubastion/Desktop/django_apis/biometricApis/known_faces"
        known_face_encoding_foldeer = "/Users/Cubastion/Desktop/django_apis/biometricApis/known_face_encoding"
        try:
            cursor.execute(requirdQuery, (emp_code,))
            if cursor.rowcount > 0:
                print("Record deleted successfully.")
                dbConnect.commit()
                cursor.close()
                dbConnect.close() 
                
                reletivePathFace = os.path.join(known_face_folder, str(emp_code))
                reletivePathFaceEncoding = os.path.join(known_face_encoding_foldeer, str(emp_code))

                if os.path.isfile(reletivePathFace) and os.path.isfile(reletivePathFaceEncoding):
                    os.remove(reletivePathFace)
                    os.remove(reletivePathFaceEncoding)

                    resultItem = {
                        "status" : True,
                        "Result" : "Deleted User Successfully from DB and locally"
                    }
                    return resultItem
                else:
                    resultItem = {
                        "status" : False,
                        "Result" : "Deleted User Suceessfully from DB and not from locally"
                    }
            else:
                print("No record found to delete.")
                resultItem = {
                    "status" : False,
                    "Result" : "Deleting User Failed"
                }
                return resultItem
                   
        except Exception as e:
            print("Failed to delete record:", str(e))
            resultItem = {
                "status" : False,
                "Result" : "Deleting User Failed"
            }
            return resultItem
        
    def checkAdmin(emp_code):
        resultItem = dict()
        dbConnect = DBConnectorHandler.DBconnector()
        cursor = dbConnect.cursor()
        requirdQuery = "SELECT emp_status FROM devbiometricDB WHERE emp_code = %s"
        try:
            cursor.execute(requirdQuery, (emp_code,))
            result = cursor.fetchone()
            if result is None:
                print("Failed to get user from DB")
                resultItem = {
                    "status": False,
                    "Result": "Failed to get user from DB"
                }
                return resultItem
            else:
                print("Success to get user from DB and Now checking if it is an Admin")
                emp_status = result[0]
                if emp_status == 'admin':
                    resultItem = {
                        "status": True,
                        "Result": "admin user"
                    }
                else:
                    resultItem = {
                        "status": False,
                        "Result": "Not an Admin"
                    }
                    
                return resultItem
        except Exception as e:
            resultItem = {
                    "status": False,
                    "Result": "Failed to get user from DB"
                }
            return resultItem
        
    def insetFaceModelToDb(emp_code, fname, lname, person_images):
        first_image = person_images[0]
        profile_url = "http://localhost:5000/image/" + emp_code
        resultItem = dict()


        knownFacePath = "/Users/Cubastion/Desktop/django_apis/biometricApis/known_faces/" + emp_code + ".jpg"
        pil_image = Image.open(first_image)
        pil_image.save(knownFacePath)


        file_name = emp_code + ".pickle"
        knownFaceEncodingPath = os.path.join("/Users/Cubastion/Desktop/django_apis/biometricApis/known_face_encoding", file_name)
        person_encodings = fr.processImgAndTeach(images=person_images)
        merged_person_encodings = np.array(person_encodings)
        serialized_encodings = pickle.dumps(merged_person_encodings)
        with open(knownFaceEncodingPath, 'wb') as file:
            file.write(serialized_encodings)

    
        dbConnect = DBConnectorHandler.DBconnector()
        cursor = dbConnect.cursor()
        select_query = "INSERT INTO devbiometricDB (first_name, last_name, emp_code, emp_status, face_model, profile_pic_url) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(select_query, (fname, lname, emp_code, "active", serialized_encodings, profile_url))
            result = cursor.fetchone()
            dbConnect.commit()
            cursor.close()
            dbConnect.close()

            resultItem = {
                    "status" : True,
                    "Result" : {
                        "messagee" : "Sucessfully uploaded user to DB"
                    }
                }
            return resultItem
        except Exception as e:
            resultItem = {
                    "status" : False,
                    "Result" : {
                        "messagee" : "Failed to uploaded user to DB"
                    }
                }
            return resultItem

    def detectFaceAndCompare(personImage):
        match_results = fr.compareImage(personImage)
        resultItem = {
            "status" : True,
            "Result" : {
                "messagee" : match_results
            }
        }
        return resultItem


class DBConnectorHandler:
    def DBconnector():
        dbConnect = connect(
            host='localhost',
            port=3306,  
            user='root',
            password='cubastion',
            database='demoBiometricDB'
        )
        return dbConnect











