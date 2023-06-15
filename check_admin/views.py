import serializers as slr
import dbHandeller as dbH
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json 


class FileView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            request_data = json.loads(request.body)
            emp_code = request_data.get('employee_code')
            print("Checking if the user is admin or not:", emp_code)
            
            # Your existing logic to check admin status
            check_admin_result = dbH.DBHandler.checkAdmin(emp_code=emp_code)
            
            response_maker_data = {
                "ret_code": 0,
                "status_body": {
                    "message": check_admin_result
                }
            }
            
            return Response(status=status.HTTP_200_OK, data=response_maker_data)
        
        except json.JSONDecodeError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid JSON"})


