FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip \
    build-essential \
    cmake \
    git \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    python3-dev \
    python3-pip \
    golang && \
    apt-get clean

RUN git clone https://github.com/davisking/dlib.git
RUN pip install dlib
RUN pip install numpy opencv-python
RUN pip install face-recognition
RUN pip install rembg
RUN pip install flask

WORKDIR /face_recog_project
COPY . /face_recog_project
RUN chmod +x run_file.sh

EXPOSE 8000
# EXPOSE 5000
# EXPOSE 8045

CMD ["/bin/sh", "/face_recog_project/run_file.sh"]
