from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
import dbHandeller as dbH

class FileView(APIView):
    parser_classes = (MultiPartParser, )
    
    def post(self, request, *args, **kwargs):
        emp_images = request.FILES.get('images')
        result = dbH.DBHandler.detectFaceAndCompare(personImage=emp_images)
        
        response_maker_data = {
            "ret_code": 1,
            "status_body": {
                "message": result
            }
        }
        
        return Response(status=status.HTTP_200_OK, data=response_maker_data)
