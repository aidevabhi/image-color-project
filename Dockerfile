FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variables
ENV DEBUG=False \
    DJANGO_ALLOWED_HOSTS=* \
    PYTHONUNBUFFERED=1

# Create media directories
RUN mkdir -p image_colorizer/media/uploads image_colorizer/media/colorized image_colorizer/media/masks

# Collect static files
WORKDIR /app/image_colorizer
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--chdir", "/app/image_colorizer", "image_colorizer.wsgi:application", "--bind", "0.0.0.0:8000"]

# Run gunicorn
CMD ["sh", "-c", "cd image_colorizer && gunicorn image_colorizer.wsgi:application --bind 0.0.0.0:8000"]
