import requests
import json

class URLConstants:
    def urlconstant():
        GET_ATTENDENCE = "http://localhost:8000/attendance"
        return GET_ATTENDENCE
    def delUrlConst():
        GET_DELETE_ATTENDENCE = ""
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
