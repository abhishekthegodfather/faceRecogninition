import serializers as slr
import dbHandeller as dbH
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json 
import requests
import base64

class FileView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            request_data = json.loads(request.body)
            emp_code = request_data.get('employee_code')
            
            # Make a request to the Flask server to retrieve the image
            flask_server_url = 'http://localhost:5000/image/' + emp_code
            response = requests.get(flask_server_url)
            if response.status_code == requests.codes.ok:
                # Image retrieval successful, you can access the image data
                image_data = response.content
                
                # Convert image data to Base64 encoded string
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                
                # Return the image data as a response
                return Response(status=status.HTTP_200_OK, data={"image_data": image_base64})
            else:
                # Image retrieval failed
                return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "Image retrieval failed"})
        
        except json.JSONDecodeError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid JSON"})


