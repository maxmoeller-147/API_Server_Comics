# Base lightweight Python image
FROM python:3.12-slim

# Prevent .pcy files and enable logging in real time
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container    
WORKDIR /app

# Copy dependencies file and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose that the app uses port 8080
EXPOSE 8080

# Flask Environment Config
ENV FLASK_APP=main:create_app \
    FLASK_ENV=development \
    FLASK_DEBUG=1

# Start the Flask development Server
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]