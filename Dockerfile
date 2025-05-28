# FROM python:3.11-slim

# # Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libgl1 \
#     libglib2.0-0 \
#     && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# # Copy everything
# COPY . .

# # Install dependencies
# RUN pip install -r requirements.txt

# # Set environment variables
# ENV DEBUG=False \
#     DJANGO_ALLOWED_HOSTS=* \
#     PYTHONUNBUFFERED=1

# # Skip collectstatic during build
# ENV DISABLE_COLLECTSTATIC=1

# # Expose port
# EXPOSE 8000

# # Run gunicorn
# CMD ["sh", "-c", "cd image_colorizer && python manage.py collectstatic --noinput && gunicorn image_colorizer.wsgi:application --bind 0.0.0.0:8000"]
# EXPOSE 8000

# # Run gunicorn
# CMD ["gunicorn", "--chdir", "/app/image_colorizer", "image_colorizer.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies without rembg
RUN pip install --no-cache-dir Django==4.2.7 numpy opencv-python matplotlib Pillow scikit-image fpdf gunicorn whitenoise

# Copy project files
COPY . .

# Set environment variables
ENV DEBUG=False \
    DJANGO_ALLOWED_HOSTS=* \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Create media directories
RUN mkdir -p image_colorizer/media/uploads image_colorizer/media/colorized image_colorizer/media/masks

# Expose port
EXPOSE 8000

# Run gunicorn with minimal workers
CMD ["sh", "-c", "cd image_colorizer && python manage.py collectstatic --noinput && gunicorn image_colorizer.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120"]

