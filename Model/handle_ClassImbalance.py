import os
import shutil
import numpy as np
import cv2
from collections import Counter
from imblearn.over_sampling import SMOTE

def delete_cropped_folder(cropped_folder_path):
    """
    Delete the 'cropped' folder if it exists.

    Parameters:
    cropped_folder_path (str): Path to the folder containing cropped images.
    """
    cropped_path = os.path.join(cropped_folder_path, 'cropped')
    if os.path.exists(cropped_path):
        shutil.rmtree(cropped_path)  # Recursively delete the cropped folder
        print(f"Deleted the 'cropped' folder at {cropped_path}")
    else:
        print("No 'cropped' folder found.")

def create_balanced_dataset(cropped_folder_path, balanced_dataset_path, target_count):
    """
    Create a balanced dataset using SMOTE.
    
    Parameters:
    cropped_folder_path (str): Path to the folder with cropped images.
    balanced_dataset_path (str): Path to save the balanced dataset.
    target_count (int): The number of images to be balanced to.
    """
    # Load images and their labels
    image_data = []
    labels = []

    for celeb_folder in os.listdir(cropped_folder_path):
        celeb_path = os.path.join(cropped_folder_path, celeb_folder)

        # Ignore cropped folder (this will be deleted now)
        if celeb_folder == 'cropped':
            continue

        for img_name in os.listdir(celeb_path):
            img_path = os.path.join(celeb_path, img_name)
            img = cv2.imread(img_path)

            if img is not None:
                # Resize image to a fixed size
                img_resized = cv2.resize(img, (64, 64))  # Choose an appropriate size
                image_data.append(img_resized.flatten())  # Flatten image to 1D
                labels.append(celeb_folder)

    # Convert to numpy arrays
    X = np.array(image_data)
    y = np.array(labels)

    # Check class distribution
    print("Class distribution before SMOTE:", Counter(y))

    # Define SMOTE with a lower number of neighbors
    smote = SMOTE(sampling_strategy='auto', k_neighbors=3)  # Set k_neighbors to a lower number

    # Apply SMOTE
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Save the balanced dataset
    if not os.path.exists(balanced_dataset_path):
        os.makedirs(balanced_dataset_path)

    for label in np.unique(y_resampled):
        label_path = os.path.join(balanced_dataset_path, label)
        if not os.path.exists(label_path):
            os.makedirs(label_path)

        # Save resampled images
        indices = np.where(y_resampled == label)[0]
        for i in indices:
            img = X_resampled[i].reshape(64, 64, 3)  # Reshape back to original size
            img_name = f"{label}_{i}.png"  # Create a new filename
            cv2.imwrite(os.path.join(label_path, img_name), img)

    print("Balanced dataset created successfully!")
    print("Class distribution after SMOTE:", Counter(y_resampled))

# Define your paths
cropped_folder_path = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\augmented'
balanced_dataset_path = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\balanced_dataset'

# Execute the deletion and balancing
delete_cropped_folder(cropped_folder_path)
create_balanced_dataset(cropped_folder_path, balanced_dataset_path, 200)
