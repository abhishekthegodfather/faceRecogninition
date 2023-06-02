from mysql.connector import connect
from datetime import date
import serializers as sr

class DBHandler:
    def getEmployeeDetails(emp_code):
        resultItem = dict()
        dbConnect = DBConnectorHandler.DBconnector()
        cursor = dbConnect.cursor()
        requiredQuery = "SELECT first_name, last_name, emp_code, emp_status, profile_pic_url FROM devbiometricDB WHERE emp_code = %s"
        try:
            cursor.execute(requiredQuery, (emp_code,))
            result = cursor.fetchone() 
            if result is None:
                print("Failed to get user from DB")
                resultItem = {
                    "status" : False,
                    "Result" : "Failed to get user"
                }
                return resultItem
            else:
                print("Sucess to get user from DB")
                single_employee = sr.EmployeeModel(result[0], result[1], result[2], result[3], result[4])
                resultItem = {
                    "status" : True,
                    "Result" : {
                        "first_name": single_employee.first_name,
                        "last_name" : single_employee.last_name,
                        "emp_code" : single_employee.emp_code,
                        "emp_status" : single_employee.emp_status,
                        "profile_pic" : single_employee.profile_url
                    }
                }
                return resultItem
        except Exception as e:
            print("Failed to get user")
            resultItem = {
                    "status" : False,
                    "Result" : "Failed to get user"
                }
            return resultItem
        
    def deleteUserFromDB(emp_code):
        resultItem = dict()
        dbConnect = DBConnectorHandler.DBconnector()
        cursor = dbConnect.cursor()
        requirdQuery = "DELETE FROM devbiometricDB WHERE emp_code = %s"
        try:
            cursor.execute(requirdQuery, (emp_code,))
            if cursor.rowcount > 0:
                print("Record deleted successfully.")
                dbConnect.commit()  # Commit the transaction
                resultItem = {
                    "status" : True,
                    "Result" : "Deleted User Successfully"
                }
                return resultItem
            else:
                print("No record found to delete.")
                resultItem = {
                    "status" : False,
                    "Result" : "Deleting User Failed"
                }
                return resultItem
        except Exception as e:
            print("Failed to delete record:", str(e))
            resultItem = {
                "status" : False,
                "Result" : "Deleting User Failed"
            }
            return resultItem
        
    def checkAdmin(emp_code):
        resultItem = dict()
        dbConnect = DBConnectorHandler.DBconnector()
        cursor = dbConnect.cursor()
        requirdQuery = "SELECT emp_status FROM devbiometricDB WHERE emp_code = %s"
        try:
            cursor.execute(requirdQuery, (emp_code,))
            result = cursor.fetchone()
            if result is None:
                print("Failed to get user from DB")
                resultItem = {
                    "status": False,
                    "Result": "Failed to get user from DB"
                }
                return resultItem
            else:
                print("Success to get user from DB and Now checking if it is an Admin")
                emp_status = result[0]
                if emp_status == 'admin':
                    resultItem = {
                        "status": True,
                        "Result": "admin user"
                    }
                else:
                    resultItem = {
                        "status": False,
                        "Result": "Not an Admin"
                    }
                    
                return resultItem
        except Exception as e:
            resultItem = {
                    "status": False,
                    "Result": "Failed to get user from DB"
                }
            return resultItem

class DBConnectorHandler:
    def DBconnector():
        dbConnect = connect(
            host='localhost',
            port=3306,  
            user='root',
            password='cubastion',
            database='demoBiometricDB'
        )
        return dbConnect

# if __name__ == '__main__':
#     DBHandler.checkAdmin(emp_code='EMP001')










