import numpy as np
import colorsys
import io
import cv2
from PIL import Image, ImageOps, ImageFilter
from rembg import remove, new_session

# Create simpler color presets
COLOR_PRESETS = {
    "🔥 Red": "#FF3333",
    "🌊 Blue": "#0066CC",
    "🌿 Green": "#50C878",
    "🌸 Pink": "#FF6EC7",
    "🌅 Orange": "#FD5E53",
    "💜 Purple": "#967BB6",
    "⚫ Black": "#2C3E50",
    "⚪ White": "#F8F8FF",
    "⭐ Gold": "#FFD700", 
    "💎 Silver": "#C0C0C0"
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB"""
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

def rgb_to_hsv(r, g, b):
    """Convert RGB to HSV"""
    return colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

def resize_image_for_processing(image, max_size=1024):
    """
    Resize image to a maximum dimension while preserving aspect ratio
    """
    width, height = image.size
    if max(width, height) <= max_size:
        return image, 1.0  # No resize needed
    
    # Calculate scale factor
    scale = max_size / max(width, height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Resize image
    resized_img = image.resize((new_width, new_height), Image.LANCZOS)
    return resized_img, scale

def create_object_mask(image, method="rembg", max_size=1024):
    """
    Create a mask to separate object from background
    Methods: 'rembg', 'grabcut', 'threshold'
    """
    try:
        # Resize large images for faster processing
        orig_size = image.size
        resized_img, scale = resize_image_for_processing(image, max_size)
        
        if method == "rembg":
            # Using rembg for automatic background removal
            session = new_session('u2net')  # You can try 'silueta' or other models
            
            # Convert PIL to bytes
            img_byte_arr = io.BytesIO()
            resized_img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Remove background with shadow removal
            output = remove(img_byte_arr, session=session, alpha_matting=True, alpha_matting_foreground_threshold=240)
            
            # Convert back to PIL
            result_image = Image.open(io.BytesIO(output)).convert("RGBA")
            
            # Extract alpha channel as mask
            mask = np.array(result_image)[:, :, 3]
            
            # Apply threshold to remove shadows (higher threshold = less shadow)
            mask = (mask > 180).astype(np.uint8) * 255
            
            # Resize mask back to original size if needed
            if scale < 1.0:
                mask_img = Image.fromarray(mask, mode='L')
                mask_img = mask_img.resize(orig_size, Image.LANCZOS)
                return mask_img
            
            return Image.fromarray(mask, mode='L')
            
        elif method == "grabcut":
            # Using OpenCV GrabCut algorithm with shadow removal
            img_cv = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)
            height, width = img_cv.shape[:2]
            
            # Create initial mask - assume center region contains object
            mask = np.zeros((height, width), np.uint8)
            
            # Define rectangle around the center area (adjustable)
            margin_x, margin_y = width // 6, height // 6
            rect = (margin_x, margin_y, width - 2*margin_x, height - 2*margin_y)
            
            # Initialize background and foreground models
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)
            
            # Apply GrabCut
            cv2.grabCut(img_cv, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
            
            # Convert mask
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            mask_final = mask2 * 255
            
            # Apply shadow removal using HSV color space
            hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            # Shadows typically have lower V (value/brightness)
            # Create shadow mask (low brightness areas)
            shadow_mask = (v < 80).astype(np.uint8) * 255
            
            # Remove shadow areas from the mask
            mask_final = cv2.bitwise_and(mask_final, cv2.bitwise_not(shadow_mask))
            
            # Resize mask back to original size if needed
            if scale < 1.0:
                mask_img = Image.fromarray(mask_final, mode='L')
                mask_img = mask_img.resize(orig_size, Image.LANCZOS)
                return mask_img
            
            return Image.fromarray(mask_final, mode='L')
            
        elif method == "threshold":
            # Simple edge-based segmentation
            gray = ImageOps.grayscale(resized_img)
            
            # Apply edge detection
            edges = gray.filter(ImageFilter.FIND_EDGES)
            
            # Threshold to create mask
            threshold = 30
            mask = np.array(edges)
            mask = (mask > threshold).astype(np.uint8) * 255
            
            # Morphological operations to fill gaps
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Resize mask back to original size if needed
            if scale < 1.0:
                mask_img = Image.fromarray(mask, mode='L')
                mask_img = mask_img.resize(orig_size, Image.LANCZOS)
                return mask_img
            
            return Image.fromarray(mask, mode='L')
            
    except Exception as e:
        print(f"Error creating mask with {method}: {str(e)}")
        # Fallback: return a mask that covers the center region
        w, h = image.size
        mask = np.zeros((h, w), dtype=np.uint8)
        center_w, center_h = w//4, h//4
        mask[center_h:h-center_h, center_w:w-center_w] = 255
        return Image.fromarray(mask, mode='L')

def enhance_mask(mask, blur_radius=2, expand_pixels=3):
    """
    Enhance the mask by smoothing edges and expanding slightly
    """
    mask_array = np.array(mask)
    
    # Dilate to expand the mask slightly
    if expand_pixels > 0:
        kernel = np.ones((expand_pixels*2+1, expand_pixels*2+1), np.uint8)
        mask_array = cv2.dilate(mask_array, kernel, iterations=1)
    
    # Blur for smooth edges
    if blur_radius > 0:
        mask_pil = Image.fromarray(mask_array, mode='L')
        mask_pil = mask_pil.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        mask_array = np.array(mask_pil)
    
    return Image.fromarray(mask_array, mode='L')

def recolor_object_only(image, color_rgb, intensity=0.7, mask=None, edge_smooth=2):
    """
    Recolor only the object in the image using pre-computed mask
    """
    # Use provided mask or return original image
    if mask is None:
        return image, None
    
    # Resize large images for faster processing
    from django.conf import settings
    max_size = getattr(settings, 'MAX_IMAGE_SIZE', 1024)
    
    orig_size = image.size
    process_image = image
    process_mask = mask
    
    # Check if resizing is needed
    if max(orig_size) > max_size:
        scale = max_size / max(orig_size)
        new_width = int(orig_size[0] * scale)
        new_height = int(orig_size[1] * scale)
        
        # Resize image and mask for processing
        process_image = image.resize((new_width, new_height), Image.LANCZOS)
        process_mask = mask.resize((new_width, new_height), Image.LANCZOS)
    
    # Enhance mask for better edges
    enhanced_mask = enhance_mask(process_mask, blur_radius=edge_smooth, expand_pixels=1)
    
    # Convert images to arrays
    img_array = np.array(process_image)
    mask_array = np.array(enhanced_mask).astype(float) / 255.0
    
    # Create colored version of the image
    gray_img = ImageOps.grayscale(process_image)
    gray_array = np.array(gray_img)
    gray_array = np.stack([gray_array, gray_array, gray_array], axis=2)
    
    # Create color layer
    color_layer = np.zeros_like(img_array)
    color_layer[:, :] = color_rgb
    
    # Blend grayscale with color
    colored_img = (gray_array.astype(float) / 255.0) * color_layer.astype(float)
    
    # Apply intensity
    colored_img = img_array.astype(float) * (1 - intensity) + colored_img * intensity
    
    # Use mask to blend original and colored versions
    # Expand mask to 3 channels
    mask_3channel = np.stack([mask_array, mask_array, mask_array], axis=2)
    
    # Final blend: original background + colored object
    result = img_array.astype(float) * (1 - mask_3channel) + colored_img * mask_3channel
    
    # Clip and convert back
    result = np.clip(result, 0, 255).astype(np.uint8)
    result_img = Image.fromarray(result)
    
    # Resize back to original size if needed
    if max(orig_size) > max_size:
        result_img = result_img.resize(orig_size, Image.LANCZOS)
    
    return result_img, enhanced_mask

def process_color_change(image, color_hex, intensity, edge_smooth, cached_mask=None):
    """Process color change with the cached mask"""
    try:
        if cached_mask is None:
            cached_mask = create_object_mask(image)
            
        color_rgb = hex_to_rgb(color_hex)
        result, enhanced_mask = recolor_object_only(
            image, 
            color_rgb, 
            intensity, 
            cached_mask, 
            edge_smooth
        )
        return result, enhanced_mask
    except Exception as e:
        print(f"Error applying color: {str(e)}")
        return image, cached_mask