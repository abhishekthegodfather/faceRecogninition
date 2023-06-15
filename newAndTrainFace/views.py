from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import dbHandeller as dbH

class FileView(APIView):
    parser_classes = (MultiPartParser, )
    def post(self, request, *args, **kwargs):
        emp_name = str(request.data.get('emp_name'))
        emp_code = str(request.data.get('emp_code'))
        emp_images = request.FILES.getlist('images')

        emp_name_array = emp_name.split()
        fname = emp_name_array[0]
        lname = emp_name_array[-1]
        result = dbH.DBHandler.insetFaceModelToDb(emp_code=emp_code, fname=fname, lname=lname, person_images=emp_images)
        response_maker_data = {
                 "ret_code" : 1,
                 "status_body" : {
                     "message" : result
                 }
             }
        return Response(status=status.HTTP_200_OK, data=response_maker_data)
        # dbH.DBHandler.detectFaceAndCompare(personImage=emp_images[0])

        return Response({'message': 'Files uploaded successfully'})

        


