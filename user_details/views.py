from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from serializers import ResponseMaker
import dbHandeller as dbH
import json

class FileView(APIView):
    parser_classes = (MultiPartParser,)
    
    def post(self, request, *args, **kwargs):
        try:
            request_data = json.loads(request.body)
            emp_code = request_data.get('employee_code')
            print("Finding Details for this Employee Code:", emp_code)
            
            send_response_dict = dbH.DBHandler.getEmployeeDetails(emp_code=emp_code)
            
            if send_response_dict["status"] == False:
                response_maker_data = {
                    "ret_code": 1,
                    "status_body": {
                        "message": send_response_dict
                    }
                }
                
                response_maker = ResponseMaker(data=response_maker_data)
                
                if response_maker.is_valid():
                    serialized_data = response_maker.data
                    return Response(status=200, data=serialized_data)
                else:
                    errors = response_maker.data
                    return Response(status=200, data=errors)
            
            else:
                response_maker_data = {
                    "ret_code": 0,
                    "status_body": send_response_dict
                }
                
                response_maker = ResponseMaker(data=response_maker_data)
                
                if response_maker.is_valid():
                    serialized_data = response_maker.data
                    return Response(status=200, data=serialized_data)
                else:
                    errors = response_maker.data
                    return Response(status=200, data=serialized_data)
        
        except json.JSONDecodeError:
            return Response(status=400, data={"error": "Invalid JSON"})
