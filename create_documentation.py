from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        # Logo
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, 'Image Colorizer - Technical Documentation', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 6, body)
        self.ln(5)
    
    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(2)
    
    def bullet_point(self, text):
        self.set_font('Arial', '', 12)
        self.cell(10, 6, chr(149), 0, 0, 'C')  # bullet character
        self.multi_cell(0, 6, text)

# Create PDF
pdf = PDF()
pdf.add_page()

# Overview
pdf.chapter_title("Overview")
pdf.chapter_body("Image Colorizer is a web application that allows users to change the color of objects in images using AI-powered image segmentation and color manipulation techniques.")

# Technologies Used
pdf.chapter_title("Technologies Used")

# Backend
pdf.section_title("Backend")
pdf.bullet_point("Django 4.2.7: Web framework for handling requests, routing, and templating")
pdf.bullet_point("Python 3.10: Programming language for backend logic and image processing")
pdf.bullet_point("SQLite: Database for storing image metadata and user preferences")

# Image Processing
pdf.section_title("Image Processing")
pdf.bullet_point("PIL/Pillow: Image manipulation library for opening, resizing, and saving images")
pdf.bullet_point("OpenCV (cv2): Computer vision library for advanced image processing and mask creation")
pdf.bullet_point("NumPy: Numerical computing library for array operations on image data")
pdf.bullet_point("rembg: Background removal library using deep learning models (U2Net)")
pdf.bullet_point("colorsys: Python module for color space conversions (RGB, HSV)")

# Frontend
pdf.section_title("Frontend")
pdf.bullet_point("HTML/CSS/JavaScript: Core web technologies for UI implementation")
pdf.bullet_point("Bootstrap 5.3: CSS framework for responsive design and UI components")
pdf.bullet_point("jQuery 3.6: JavaScript library for DOM manipulation and AJAX requests")
pdf.bullet_point("CSS Transitions/Animations: For smooth UI interactions and loading states")

# Key Features
pdf.section_title("Key Features")
pdf.bullet_point("Object detection and background separation using AI")
pdf.bullet_point("Real-time color changes with AJAX")
pdf.bullet_point("Color intensity and edge smoothness adjustments")
pdf.bullet_point("Optimized processing for large images (auto-resizing)")
pdf.bullet_point("Shadow removal algorithms")
pdf.bullet_point("Mask caching for improved performance")

# Performance Optimizations
pdf.section_title("Performance Optimizations")
pdf.bullet_point("Image resizing for large images (max dimension: 1024px)")
pdf.bullet_point("JPEG compression for faster loading")
pdf.bullet_point("Mask caching to avoid regeneration")
pdf.bullet_point("Debounced UI controls to prevent excessive API calls")

# Deployment
pdf.section_title("Deployment")
pdf.bullet_point("Static files served via Django's staticfiles system")
pdf.bullet_point("Media files for storing uploaded and processed images")
pdf.bullet_point("Compatible with PythonAnywhere and other Django hosting platforms")

# System Requirements
pdf.section_title("System Requirements")
pdf.bullet_point("Python 3.8+ with pip")
pdf.bullet_point("2GB+ RAM recommended for image processing")
pdf.bullet_point("Sufficient disk space for image storage")

# Save the PDF
pdf_path = os.path.join(os.path.dirname(__file__), 'image_colorizer_documentation.pdf')
pdf.output(pdf_path)
print(f"PDF documentation created at: {pdf_path}")