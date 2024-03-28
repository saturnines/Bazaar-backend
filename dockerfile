# Use a Pythontime as a base image
FROM python:3.9-slim

#Current dir into the docker container.
WORKDIR /app

#Copy the above dir into /app
COPY . /app

# Install packages in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Allow port 8000 (Not sure if this is bad practice)??
EXPOSE 8000

#Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]