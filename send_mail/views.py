import dbHandeller as dbH
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import json 


class FileView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            request_data = json.loads(request.body)
            emp_email = request_data.get('emailId')
            emp_issue_desc = request_data.get('issue_desc')
            emp_issue_title = request_data.get('issue_title')

            result = dbH.MailSender.mailSender(emp_issue_title, emp_issue_desc, emp_email)            
            return Response(status=status.HTTP_200_OK, data=result)
        
        except json.JSONDecodeError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Invalid JSON"})


