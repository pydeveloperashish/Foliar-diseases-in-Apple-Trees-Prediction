# Use the official Ubuntu base image
FROM python:3.10.12-slim-buster

# Set the working directory inside the container
WORKDIR /app/

# Update the package lists and install necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip

RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install libpq-dev python-dev -y

COPY requirements.txt /app/
COPY setup.py /app/
COPY models/ /app/models/
COPY uploads /app/uploads/
COPY samples/ /app/samples/
COPY gradio_app2.py /app/

RUN pip3 install --no-cache-dir -r requirements.txt


CMD ["python3", "gradio_app2.py"]