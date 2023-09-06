# base image
FROM python:3.11.5-alpine

# Define the author
LABEL author="https://github.com/Maengdok" \
      maintainer="Maengdok" \
      version="0.0.0"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Switch to app directory so that everything runs from here
WORKDIR app
RUN mkdir /app/staticfiles

# Install system dependencies
RUN apk update

# install dependencies
RUN pip install --upgrade pip

# Copy the required packages for the user
COPY ./requirements.txt .

# Let pip install required packages
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY /docker/entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy the app code to image working directory for the user
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]