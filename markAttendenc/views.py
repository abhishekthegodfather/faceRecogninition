from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
import AttendenceHandler as AHR
from rest_framework import status
import json


class FileView(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, *args, **kwargs):
        try:
            request_data = json.loads(request.body)
            emp_code = request_data.get('employee_code')
            result = AHR.AttendenceHandler.attendenceHandler(emp_code=emp_code)
            print(result)
            response_maker_data = {
                    "ret_code" : 0,
                    "status_body" : {
                        "message" : result
                    }
                }
            return Response(status=status.HTTP_200_OK, data=response_maker_data)
        
        except json.JSONDecodeError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid JSON"})

