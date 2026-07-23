import os
import random
import time
import numpy as np
import cv2
from PIL import Image, ImageDraw
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Model parameters matching repo fabric_defect_detection.py
CLASSES = ["hole", "horizontal", "vertical", "normal"]
IMG_HEIGHT = 224
IMG_WIDTH = 224
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "fabric_defect_model.pt")

class FabricCNN(nn.Module):
    """
    PyTorch implementation of the exact 3-block CNN architecture from fabric_defect_detection.py
    Block 1: Conv2d(3, 32, 3) -> ReLU -> MaxPool2d(2, 2)
    Block 2: Conv2d(32, 64, 3) -> ReLU -> MaxPool2d(2, 2)
    Block 3: Conv2d(64, 128, 3) -> ReLU -> MaxPool2d(2, 2)
    Dense: Linear(128 * 28 * 28, 128) -> ReLU -> Dropout(0.5) -> Linear(128, 4)
    """
    def __init__(self, num_classes=4):
        super(FabricCNN, self).__init__()
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            # Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            # Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 28 * 28, 128),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

def preprocess_image(img_input):
    """
    Reuses preprocessing pipeline from fabric_defect_detection.py:
    1. Read/Convert image to RGB
    2. Resize to 224x224
    3. Normalize pixel values to [0, 1]
    """
    if isinstance(img_input, str):
        img_bgr = cv2.imread(img_input)
        if img_bgr is None:
            raise ValueError(f"Could not read image from path: {img_input}")
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    elif isinstance(img_input, np.ndarray):
        if len(img_input.shape) == 2:
            img_rgb = cv2.cvtColor(img_input, cv2.COLOR_GRAY2RGB)
        elif img_input.shape[2] == 4:
            img_rgb = cv2.cvtColor(img_input, cv2.COLOR_RGBA2RGB)
        elif img_input.shape[2] == 3:
            img_rgb = img_input.copy()
        else:
            img_rgb = img_input
    elif isinstance(img_input, Image.Image):
        img_rgb = np.array(img_input.convert('RGB'))
    else:
        raise TypeError("Unsupported image format")

    # Resize to target resolution (224, 224)
    resized = cv2.resize(img_rgb, (IMG_WIDTH, IMG_HEIGHT))
    
    # Normalize to range [0, 1]
    normalized = resized.astype(np.float32) / 255.0
    
    return normalized, resized

def create_synthetic_dataset(dest_dir="fabric_data", num_images=40):
    """
    Generates synthetic fabric defect dataset as implemented in repo's fabric_defect_detection.py
    """
    os.makedirs(dest_dir, exist_ok=True)
    for class_name in CLASSES:
        class_dir = os.path.join(dest_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)
        
        for i in range(num_images):
            img_size = (256, 256)
            img = Image.new('RGB', img_size, color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            
            # Texture pattern
            for x in range(0, img_size[0], 4):
                for y in range(0, img_size[1], 4):
                    color_var = random.randint(-12, 12)
                    c = max(0, min(255, 230 + color_var))
                    draw.point((x, y), fill=(c, c, c))
            
            # Defect overlays
            if class_name == "hole":
                cx, cy = random.randint(60, 190), random.randint(60, 190)
                r = random.randint(12, 28)
                draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=(30, 30, 30))
                for _ in range(8):
                    dx, dy = random.randint(-r, r), random.randint(-r, r)
                    draw.ellipse((cx+dx-3, cy+dy-3, cx+dx+3, cy+dy+3), fill=(20, 20, 20))
                    
            elif class_name == "horizontal":
                for _ in range(random.randint(1, 3)):
                    y = random.randint(30, 220)
                    thickness = random.randint(3, 7)
                    draw.line([(0, y), (256, y)], fill=(70, 70, 70), width=thickness)
                    
            elif class_name == "vertical":
                for _ in range(random.randint(1, 3)):
                    x = random.randint(30, 220)
                    thickness = random.randint(3, 7)
                    draw.line([(x, 0), (x, 256)], fill=(70, 70, 70), width=thickness)
                    
            # Save image
            img_path = os.path.join(class_dir, f"synthetic_{class_name}_{i:03d}.png")
            img.save(img_path)
            
    return dest_dir

def train_and_save_model(data_dir="fabric_data", epochs=15):
    """
    Trains the CNN model using PyTorch and saves weights to fabric_defect_model.pt
    """
    if not os.path.exists(data_dir):
        create_synthetic_dataset(data_dir, num_images=40)
        
    X_list, y_list = [], []
    for idx, class_name in enumerate(CLASSES):
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.exists(class_dir):
            continue
        for fname in os.listdir(class_dir):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                fpath = os.path.join(class_dir, fname)
                try:
                    norm, _ = preprocess_image(fpath)
                    X_list.append(norm)
                    y_list.append(idx)
                except Exception:
                    pass
                    
    if len(X_list) == 0:
        raise RuntimeError("No training images found!")
        
    X_arr = np.array(X_list, dtype=np.float32).transpose(0, 3, 1, 2) # (N, C, H, W)
    y_arr = np.array(y_list, dtype=np.int64)
    
    dataset = TensorDataset(torch.from_numpy(X_arr), torch.from_numpy(y_arr))
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = FabricCNN(num_classes=len(CLASSES)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    model.train()
    for epoch in range(epochs):
        for batch_x, batch_y in dataloader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
    model.eval()
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    return model

def load_fabric_model():
    """
    Loads trained PyTorch model weights or auto-trains if model file doesn't exist
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = FabricCNN(num_classes=len(CLASSES)).to(device)
    
    if os.path.exists(MODEL_SAVE_PATH):
        try:
            model.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=device))
            model.eval()
            return model, device
        except Exception:
            pass
            
    # Auto-train if weights not found
    model = train_and_save_model()
    model.eval()
    return model, device

def run_inference(img_input, model=None, device=None):
    """
    Runs model inference on uploaded fabric image.
    Returns:
    - predicted_class: str ('hole', 'horizontal', 'vertical', 'normal')
    - confidence: float (0.0 to 1.0)
    - probabilities: dict mapping class name -> probability
    - inference_time: float (seconds)
    - preprocessed_rgb: np.ndarray (224, 224, 3)
    """
    start_time = time.time()
    
    if model is None or device is None:
        model, device = load_fabric_model()
        
    norm_img, resized_rgb = preprocess_image(img_input)
    
    # Format for PyTorch tensor (1, 3, 224, 224)
    tensor_input = torch.from_numpy(norm_img).float().permute(2, 0, 1).unsqueeze(0).to(device)
    
    model.eval()
    with torch.no_grad():
        outputs = model(tensor_input)
        probs = torch.softmax(outputs, dim=1).cpu().numpy()[0]
        
    pred_idx = int(np.argmax(probs))
    predicted_class = CLASSES[pred_idx]
    confidence = float(probs[pred_idx])
    
    prob_dict = {CLASSES[i]: float(probs[i]) for i in range(len(CLASSES))}
    inference_time = time.time() - start_time
    
    return {
        "label": predicted_class,
        "confidence": confidence,
        "probabilities": prob_dict,
        "inference_time": inference_time,
        "resized_rgb": resized_rgb
    }
