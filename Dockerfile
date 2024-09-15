# Base image: Python 3.10
FROM python:3.10-slim

# Install system dependencies needed for Playwright browsers
RUN apt-get update && apt-get install -y \
    libatk-bridge2.0-0 libatspi2.0-0 libgbm1 libasound2 \
    libnss3 libxcomposite1 libxdamage1 libxrandr2 libxss1 libgtk-3-0 libxshmfence1 \
    && apt-get clean

# Set environment variables to avoid Python bytecode and buffering issues
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt /app/

# Install Python dependencies (including Playwright)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright browsers (Chromium, Firefox, WebKit)
RUN playwright install

# Copy the rest of the project files
COPY . /app/

# Run Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN apt-get update && apt-get install -y xvfb


