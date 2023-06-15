from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import dbHandeller as dbH
import serializers as sl

class FileView(APIView):
    parser_classes = (MultiPartParser, )
    def post(self, request, *args, **kwargs):
        emp_code = request.data['employee_code']
        print("droping details for this employee code", emp_code)
        delete_result = dbH.DBHandler.deleteUserFromDB(emp_code=emp_code)
        if delete_result["status"] == False:
            response_maker_data = {
                 "ret_code" : 1,
                 "status_body" : {
                     "message" : delete_result
                 }
             }
            response_maker = sl.ResponseMaker(data=response_maker_data)
            if response_maker.is_valid():
                serialized_data = response_maker.data
                return Response(status=200, data=serialized_data)
            else:
                errors = response_maker.data
                return Response(status=200, data=errors)
        else:
            response_maker_data = {
                 "ret_code" : 0,
                 "status_body" : {
                     "message" : delete_result
                 }
             }
            response_maker = sl.ResponseMaker(data=response_maker_data)
            if response_maker.is_valid():
                serialized_data = response_maker.data
                return Response(status=200, data=serialized_data)
            else:
                error = response_maker.data
                return Response(status=200, data=error)
