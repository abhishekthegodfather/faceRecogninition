from rest_framework import serializers

class ResponseMaker(serializers.Serializer):
    ret_code = serializers.IntegerField()
    status_body = serializers.DictField()


class EmployeeModel:
    def __init__(self, first_name: str, last_name: str, emp_code: str, emp_status: str, profile_url: str):
        self.first_name = first_name
        self.last_name = last_name
        self.emp_code = emp_code
        self.emp_status = emp_status
        self.profile_url = profile_url



