import cv2
import numpy as np

def analyze_and_draw_defects(image_rgb, predicted_label):
    """
    Analyzes fabric image using OpenCV edge detection, thresholding, and contour analysis
    to highlight defect regions and compute bounding boxes.
    
    Returns:
    - annotated_img: RGB np.ndarray with defect bounding boxes & highlights
    - heatmap_img: RGB np.ndarray heatmap overlay of defect regions
    - defect_info: dict with bounding box coords, defect area, contour count, and status
    """
    img_h, img_w, _ = image_rgb.shape
    annotated = image_rgb.copy()
    
    # Convert to grayscale for image processing
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian Blur to smooth texture noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    boxes = []
    total_defect_area = 0
    contour_count = 0
    
    if predicted_label == "normal":
        # For normal fabrics, no bounding boxes are drawn
        # Create subtle green status indicator border
        cv2.rectangle(annotated, (5, 5), (img_w - 5, img_h - 5), (34, 197, 94), 2)
        heatmap = image_rgb.copy()
        defect_info = {
            "defect_detected": False,
            "defect_type": "None (Normal Fabric)",
            "bounding_boxes": [],
            "total_defect_area_px": 0,
            "defect_coverage_pct": 0.0,
            "contour_count": 0
        }
        return annotated, heatmap, defect_info

    # Image Processing for Defect Localization (Hole, Horizontal, Vertical)
    if predicted_label == "hole":
        # Holes appear as dark circular spots on fabric
        # Adaptive / Otsu Thresholding for dark regions
        _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
    elif predicted_label == "horizontal":
        # Edge detection emphasizing horizontal gradients (Sobel Y or Canny)
        edges_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
        edges_y = cv2.convertScaleAbs(edges_y)
        _, thresh = cv2.threshold(edges_y, 40, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
    elif predicted_label == "vertical":
        # Edge detection emphasizing vertical gradients (Sobel X or Canny)
        edges_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
        edges_x = cv2.convertScaleAbs(edges_x)
        _, thresh = cv2.threshold(edges_x, 40, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 15))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
    else:
        # Fallback Canny Edge Detection
        edges = cv2.Canny(blurred, 50, 150)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        thresh = cv2.dilate(edges, kernel, iterations=1)
        
    # Find contours of defect regions
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter small noise contours
    min_area = 15.0 if predicted_label == "hole" else 25.0
    valid_contours = [c for c in contours if cv2.contourArea(c) >= min_area]
    
    # Color palette for defect overlay (Red / Coral for defects)
    bbox_color = (239, 68, 68)   # Bright Red RGB
    label_color = (255, 255, 255) # White
    
    # Create Heatmap Overlay
    heatmap_colored = cv2.applyColorMap(thresh, cv2.COLORMAP_JET)
    heatmap_rgb = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    heatmap = cv2.addWeighted(image_rgb, 0.6, heatmap_rgb, 0.4, 0)
    
    for c in valid_contours:
        x, y, w, h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        total_defect_area += area
        contour_count += 1
        boxes.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h), "area": float(area)})
        
        # Draw bounding box
        cv2.rectangle(annotated, (x, y), (x + w, y + h), bbox_color, 2)
        
        # Draw translucent filled defect mask inside bounding box
        sub_img = annotated[y:y+h, x:x+w]
        red_mask = np.full_like(sub_img, (239, 68, 68))
        annotated[y:y+h, x:x+w] = cv2.addWeighted(sub_img, 0.7, red_mask, 0.3, 0)
        
        # Draw defect tag label
        tag = f"{predicted_label.upper()} ({int(area)}px)"
        cv2.putText(annotated, tag, (x, max(15, y - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, label_color, 1, cv2.LINE_AA)
        
    coverage_pct = round((total_defect_area / (img_h * img_w)) * 100.0, 2)
    
    defect_info = {
        "defect_detected": True,
        "defect_type": predicted_label.capitalize(),
        "bounding_boxes": boxes,
        "total_defect_area_px": float(total_defect_area),
        "defect_coverage_pct": coverage_pct,
        "contour_count": contour_count
    }
    
    return annotated, heatmap, defect_info
