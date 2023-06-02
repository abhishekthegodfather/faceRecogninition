from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import dbHandeller as dbH
from serializers import ResponseMaker


class FileView(APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, *args, **kwargs):
        emp_code = request.data['employee_code']
        print("Finding Details for this Employee Code", emp_code)
        send_response_dict = dbH.DBHandler.getEmployeeDetails(emp_code=emp_code)
        if send_response_dict["status"] == False:
             response_maker_data = {
                 "ret_code" : 1,
                 "status_body" : {
                     "message" : send_response_dict
                 }
             }
             response_maker = ResponseMaker(data=response_maker_data)
             if response_maker.is_valid():
                # print("not got error")
                serialized_data = response_maker.data
                return Response(status=200, data=serialized_data)
             else:
                #  print("got error")
                errors = response_maker.data
                return Response(status=200, data=errors)
        else:
            response_maker_data = {
                    "ret_code" : 0,
                    "status_body" : send_response_dict
                }
            response_maker = ResponseMaker(data=response_maker_data)
            
            if response_maker.is_valid():
                print("not got error")
                serialized_data = response_maker.data
                return Response(status=200, data=serialized_data)
            else:
                 print("got error")
                 errors = response_maker.data
                 return Response(status=200, data=serialized_data)
            



