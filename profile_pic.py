# from flask import Flask, send_file, request
# import io

# app = Flask(__name__)


# def generate_image(emp_code):
#     emp_faces_path = "/Users/Cubastion/Desktop/django_apis/biometricApis/known_faces/" + emp_code + ".jpg"
#     with open(emp_faces_path, 'rb') as f:
#         image_data = f.read()

#     stream = io.BytesIO()
#     stream.write(image_data)
#     stream.seek(0)

#     # Return the image as a response with appropriate MIME type
#     return send_file(stream, mimetype='image/jpg')

# @app.route('/image/<emp_code>')
# def get_image(emp_code):
#     return generate_image(emp_code)

# if __name__ == '__main__':
#     app.run()

from flask import Flask, send_file, request
import io

app = Flask(__name__)


def generate_image(emp_code):
    emp_faces_path = "/Users/Cubastion/Desktop/django_apis/biometricApis/known_faces/" + emp_code + ".jpg"
    with open(emp_faces_path, 'rb') as f:
        image_data = f.read()

    # Return the image data as a response with appropriate MIME type
    return image_data

@app.route('/image/<emp_code>')
def get_image(emp_code):
    image_data = generate_image(emp_code)
    return send_file(io.BytesIO(image_data), mimetype='image/jpg')

if __name__ == '__main__':
    app.run()





