import requests
import json

class URLConstants:
    def urlconstant():
        # GET_ATTENDENCE = "http://localhost:8000/attendance"
        GET_ATTENDENCE = "https://3de9-61-247-238-221.ngrok-free.app/attendance"
        
        return GET_ATTENDENCE
    def delUrlConst():
        GET_DELETE_ATTENDENCE = "http://localhost:8000/delete_attendance"
        return GET_DELETE_ATTENDENCE

class AttendenceHandler:
    def attendenceHandler(emp_code):
        print("Marking attendence for Employee Code", emp_code)
        request_body = {
            "emp_code": str(emp_code)
            }
        response = requests.put(url=URLConstants.urlconstant(), timeout=30, json=request_body)
        if response != None or response != "":
            decoded_response = response.content.decode('utf-8')
            decoded_json = json.loads(decoded_response)
            return decoded_json
        else:
            resultItem = dict()
            resultItem = {
                "status" : False,
                "message" : "Failed to mark Attendence"
            }
            return resultItem
        
    def deleteCurrentAttendence(emp_code):
        print("Deleting Current Attendence", emp_code)
        request_body = {
            "emp_code" : str(emp_code)
        }

        response = requests.put(url=URLConstants.delUrlConst(), timeout=30, json=request_body)
        if response != None or response != "":
            decoded_response = response.content.decode('utf-8')
            decoded_json = json.loads(decoded_response)
            return decoded_json
        else:
            resultItem = dict()
            resultItem = {
                "status" : False,
                "message" : "Failed to mark Attendence"
            }
            return resultItem

