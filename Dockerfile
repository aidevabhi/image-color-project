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

# Skip collectstatic during build
ENV DISABLE_COLLECTSTATIC=1

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["sh", "-c", "cd image_colorizer && python manage.py collectstatic --noinput && gunicorn image_colorizer.wsgi:application --bind 0.0.0.0:8000"]
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--chdir", "/app/image_colorizer", "image_colorizer.wsgi:application", "--bind", "0.0.0.0:8000"]
