FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OpenCV and other libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn whitenoise

# Copy project files
COPY image_colorizer/ .

# Set environment variables
ENV DEBUG=False \
    DJANGO_ALLOWED_HOSTS=* \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=image_colorizer.settings

# Create media directories
RUN mkdir -p media/uploads media/colorized media/masks

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "image_colorizer.wsgi:application"]
