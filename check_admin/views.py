import serializers as slr
import dbHandeller as dbH
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

class FileView(APIView):
    parser_classes = (MultiPartParser, )
    def post(self, request, *args, **kwargs):
        emp_code = request.data['employee_code']
        print("checking the user is admin or not", emp_code)
        check_admin_result =  dbH.DBHandler.checkAdmin(emp_code=emp_code)
        response_maker_data = {
                    "ret_code" : 0,
                    "status_body" : {
                     "message" : check_admin_result
                     }
                 }
        response_maker = slr.ResponseMaker(data=response_maker_data)
        if response_maker.is_valid():
            # print("not got error")
            serialized_data = response_maker.data
            return Response(status=200, data=serialized_data)
        else:
            errors = response_maker.data
            return Response(status=200, data=errors)
        
