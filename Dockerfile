# Use an official Python runtime as a base image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY /app /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#ENV FLASK_APP=run.py

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
# ENV NAME World

# Run run.py when the container launches
ENTRYPOINT [ "python" ]

CMD [ "run.py" ]


#CMD ["flask", "run", "--host", "0.0.0.0"]
