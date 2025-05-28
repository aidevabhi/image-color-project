# AI Object Colorizer - Django Application

This Django application allows users to upload images and change the color of objects using AI-powered image segmentation.

## Features

- Upload images and automatically detect objects
- Apply different colors to objects while preserving the background
- Adjust color intensity and edge smoothness
- Download the colorized images
- Choose from preset colors or use a custom color picker

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Create a superuser (optional):
   ```
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

1. Navigate to http://127.0.0.1:8000/ in your web browser
2. Upload an image
3. Select a color from the presets or use the color picker
4. Adjust intensity and edge smoothness as needed
5. Click "Colorize Image" to process the image
6. Download the result or try different colors

## Technologies Used

- Django
- PIL (Python Imaging Library)
- OpenCV
- rembg (for background removal)
- NumPy
- Bootstrap (for frontend styling)

## Project Structure

- `colorizer_app/` - Main Django application
  - `models.py` - Database models for storing images
  - `views.py` - View functions for handling requests
  - `utils.py` - Image processing utilities
  - `templates/` - HTML templates
  - `static/` - CSS, JS, and static assets

## License

This project is licensed under the MIT License.