# Use an official Python runtime as a parent image
FROM python:3.12

# Install PDM
RUN pip install pdm

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install project dependencies
RUN pdm install

# Make port 8000 available to the world outside this container
EXPOSE 8000
