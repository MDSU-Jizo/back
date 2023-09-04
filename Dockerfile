# base image
FROM python:3.11.5-alpine

# Define the author
LABEL Author="https://github.com/Maengdok"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONBUFFERED 1

# Switch to . directory so that everything runs from here
WORKDIR .

# Copy the app code to image working directory
COPY . .

# Let pip install required packages
RUN pip install -r requirements.txt