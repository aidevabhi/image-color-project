FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV DEBUG=False \
    DJANGO_ALLOWED_HOSTS=* \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Optional: skip collectstatic at build time
ENV DISABLE_COLLECTSTATIC=1

# Expose the port
EXPOSE 8000

# Run Gunicorn with collectstatic
CMD sh -c "python manage.py collectstatic --noinput && gunicorn image_colorizer.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120"
