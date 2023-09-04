# base image
FROM python:3.11.5-alpine

# Define the author
LABEL author="https://github.com/Maengdok" \
      maintainer="Maengdok" \
      version="0.0.0"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONBUFFERED 1

# Create a user to avoid using root user
RUN adduser -D python

# Set the user
USER python

# Switch to . directory so that everything runs from here
WORKDIR ./home/python/app

# Copy the requirements for the user
COPY --chown=python:python requirements.txt requirements.txt

# Create PATH environment variable
ENV PATH="/home/worker/app/.local/bin:${PATH}"

# Copy the app code to image working directory for the user
COPY --chown=python:python . .

# Let pip install required packages
RUN pip install -r requirements.txt