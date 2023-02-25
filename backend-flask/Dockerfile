FROM python:3.10-slim-buster

# Inside Container
# Create a new folder in the container
WORKDIR /backend-flask

# Outside Container -> Inside Container
# Copy this file to the created folder in the container
# This file contains the libraries we need to install to run the app
COPY requirements.txt requirements.txt

# Inside Container
# A command to install the python libraries needed to run the app located in the `requirements.txt` file
RUN pip3 install -r requirements.txt

# Need to install CURL to make HealthCheck to run properly
RUN apt-get update 
RUN apt-get install -y gcc
RUN apt-get install -y curl

# Outside Container -> Inside Container
# . (period) means everything in the corrent directory
# First Period . - /backend-flask (outside the container)
# Second Period . - /backend-flask (inside the container)
COPY . .

# Set ENV ( Enviroment Variables )
# They get set inside the Container and will remain set when the container is running 
ENV FLASK_ENV=development

EXPOSE ${PORT}

# CMD (Command)
# python3 -m flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]