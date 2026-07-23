import numpy as np
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import PIL.Image as Image
import tensorflow as tf
import os
import seaborn as sns  # Fixed import (was 'sb')
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# Fixed import for to_categorical
try:
    # For TensorFlow 2.x
    from tensorflow.keras.utils import to_categorical
except ImportError:
    # For older versions
    from tensorflow.keras.utils import to_categorical

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

def load_and_preprocess_data(data_dir, img_height=224, img_width=224):
    """
    Load and preprocess fabric defect images from directory
    """
    # Define class directories
    classes = ["hole", "horizontal", "vertical", "normal"]
    class_indices = {class_name: i for i, class_name in enumerate(classes)}
    
    images = []
    labels = []
    
    # Load images from each class directory
    for class_name in classes:
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.exists(class_dir):
            print(f"Warning: Directory {class_dir} not found. Skipping.")
            continue
        
        class_idx = class_indices[class_name]
        
        # Get all image files in the directory
        image_files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        
        for img_file in image_files:
            img_path = os.path.join(class_dir, img_file)
            
            # Read image using cv2
            try:
                img = cv2.imread(img_path)
                if img is None:
                    print(f"Warning: Could not read image {img_path}")
                    continue
                
                # Convert BGR to RGB (cv2 loads as BGR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Resize image
                img = cv2.resize(img, (img_height, img_width))
                
                # Normalize pixel values to [0,1]
                img = img / 255.0
                
                images.append(img)
                labels.append(class_idx)
            except Exception as e:
                print(f"Error processing {img_path}: {str(e)}")
    
    # Convert lists to numpy arrays
    X = np.array(images)
    y = np.array(labels)
    
    # Convert labels to one-hot encoding
    y_categorical = to_categorical(y, num_classes=len(classes))
    
    return X, y_categorical, classes

def create_cnn_model(img_height, img_width, num_classes):
    """
    Create a CNN model for fabric defect classification
    """
    model = Sequential([
        # First convolutional block
        Conv2D(32, (3, 3), activation='relu', padding='same', 
               input_shape=(img_height, img_width, 3)),
        MaxPooling2D((2, 2)),
        
        # Second convolutional block
        Conv2D(64, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        
        # Third convolutional block
        Conv2D(128, (3, 3), activation='relu', padding='same'),
        MaxPooling2D((2, 2)),
        
        # Flatten and dense layers
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def plot_training_history(history):
    """
    Plot training and validation accuracy/loss
    """
    plt.figure(figsize=(12, 5))
    
    # Plot accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    # Plot loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.show()

def evaluate_model(model, X_test, y_test, class_names):
    """
    Evaluate model and display results
    """
    # Get predictions
    y_pred_prob = model.predict(X_test)
    y_pred = np.argmax(y_pred_prob, axis=1)
    y_true = np.argmax(y_test, axis=1)
    
    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Plot confusion matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names,
                yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.savefig('confusion_matrix.png')
    plt.show()
    
    # Print classification report
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))

def create_synthetic_dataset(dest_dir="fabric_data", num_images=50):
    """
    Create a synthetic dataset of fabric images with defects for demonstration
    """
    import random
    from PIL import Image, ImageDraw
    
    # Create directory structure
    classes = ["hole", "horizontal", "vertical", "normal"]
    
    # Create main directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created main directory: {dest_dir}")
    
    # Create class subdirectories
    for class_name in classes:
        class_dir = os.path.join(dest_dir, class_name)
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)
            print(f"Created class directory: {class_dir}")
    
    # Generate synthetic images for each class
    for class_name in classes:
        print(f"Generating {num_images} synthetic images for class '{class_name}'...")
        
        for i in range(num_images):
            # Create a base fabric texture
            img_size = (256, 256)
            img = Image.new('RGB', img_size, color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            
            # Add basic fabric texture
            for x in range(0, img_size[0], 4):
                for y in range(0, img_size[1], 4):
                    color_variation = random.randint(-10, 10)
                    color = (230 + color_variation, 230 + color_variation, 230 + color_variation)
                    draw.point((x, y), fill=color)
            
            # Add specific defect based on class
            if class_name == "hole":
                # Draw a hole (dark circle)
                x = random.randint(50, img_size[0]-50)
                y = random.randint(50, img_size[1]-50)
                radius = random.randint(10, 30)
                draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=(50, 50, 50))
            
            elif class_name == "horizontal":
                # Draw horizontal lines
                for _ in range(random.randint(1, 3)):
                    y = random.randint(20, img_size[1]-20)
                    thickness = random.randint(2, 5)
                    color = (100, 100, 100)
                    draw.line([(0, y), (img_size[0], y)], fill=color, width=thickness)
            
            elif class_name == "vertical":
                # Draw vertical lines
                for _ in range(random.randint(1, 3)):
                    x = random.randint(20, img_size[0]-20)
                    thickness = random.randint(2, 5)
                    color = (100, 100, 100)
                    draw.line([(x, 0), (x, img_size[1])], fill=color, width=thickness)
            
            # Normal class has no defects, just the base texture
            
            # Save the image
            img_path = os.path.join(dest_dir, class_name, f"synthetic_{class_name}_{i:03d}.png")
            img.save(img_path)
    
    print("\nSynthetic dataset created successfully!")
    return dest_dir

def main():
    # Parameters
    img_height = 224
    img_width = 224
    batch_size = 32
    epochs = 20
    data_dir = "fabric_data"
    
    # Check if data directory exists, if not create synthetic data
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} not found. Creating synthetic dataset...")
        data_dir = create_synthetic_dataset(data_dir)
    
    # Load and preprocess data
    print("Loading and preprocessing data...")
    X, y, class_names = load_and_preprocess_data(data_dir, img_height, img_width)
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Print dataset information
    print(f"Dataset loaded: {len(X_train)} training samples, {len(X_test)} testing samples")
    print(f"Classes: {class_names}")
    
    # Create and compile model
    print("Creating model...")
    model = create_cnn_model(img_height, img_width, len(class_names))
    model.summary()
    
    # Train model
    print("Training model...")
    history = model.fit(
        X_train, y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(X_test, y_test),
        callbacks=[
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            )
        ]
    )
    
    # Plot training history
    plot_training_history(history)
    
    # Evaluate model
    print("Evaluating model...")
    evaluate_model(model, X_test, y_test, class_names)
    
    # Save model
    model_path = 'fabric_defect_model.h5'
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    print("Fabric defect classification model training completed!")

if __name__ == "__main__":
    main() 