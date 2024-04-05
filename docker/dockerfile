# Use a Pythontime as a base image
FROM python:3.9-slim

#Current dir into the docker container.
WORKDIR /app

#Copy the above dir into /app
COPY . /app

# Install packages in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Allow port 8080
EXPOSE 8080


#Run the app
CMD ["uvicorn", "trading_api:app", "--host", "0.0.0.0", "--port", "8080"]