import os
import cv2
import numpy as np
import random
from pathlib import Path

# Augmentation Functions
def rotate_image(image, angle):
    """Rotates the image by a given angle."""
    height, width = image.shape[:2]
    center = (width / 2, height / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    rotated_img = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_img

def flip_image(image, flip_code):
    """Flips the image horizontally or vertically based on flip_code.
    flip_code: 1 for horizontal, 0 for vertical, -1 for both."""
    return cv2.flip(image, flip_code)

def shift_image(image, shift_x, shift_y):
    """Shifts the image by given pixel amounts in the x and y direction."""
    height, width = image.shape[:2]
    translation_matrix = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
    shifted_img = cv2.warpAffine(image, translation_matrix, (width, height))
    return shifted_img

def augment_image(image):
    """Applies a series of augmentations (rotation, flipping, shifting) to an image."""
    # Define augmentation parameters
    angles = [15, -15, 30, -30]
    flip_codes = [1, 0, -1]
    shifts = [(10, 0), (-10, 0), (0, 10), (0, -10)]

    augmented_images = []

    # Apply rotations
    for angle in angles:
        rotated_img = rotate_image(image, angle)
        augmented_images.append(rotated_img)

    # Apply flipping
    for flip_code in flip_codes:
        flipped_img = flip_image(image, flip_code)
        augmented_images.append(flipped_img)

    # Apply shifting
    for shift_x, shift_y in shifts:
        shifted_img = shift_image(image, shift_x, shift_y)
        augmented_images.append(shifted_img)

    return augmented_images

# Pipeline to augment images for all celebrities
def augment_images_in_bulk(source_folder, dest_folder):
    """
    Augments all cropped images in the source_folder and saves augmented images
    in the same folder under destination folder structure.
    """
    # Create destination folder if it doesn't exist
    Path(dest_folder).mkdir(parents=True, exist_ok=True)

    # Process each celebrity folder
    for celeb_folder in os.listdir(source_folder):
        celeb_folder_path = os.path.join(source_folder, celeb_folder)

        if os.path.isdir(celeb_folder_path):
            print(f"Augmenting images for: {celeb_folder}")

            # Create a corresponding folder in the destination directory
            augmented_celeb_folder = os.path.join(dest_folder, celeb_folder)
            Path(augmented_celeb_folder).mkdir(parents=True, exist_ok=True)

            # Process each image in the celebrity folder
            for i, img_file in enumerate(os.listdir(celeb_folder_path)):
                img_path = os.path.join(celeb_folder_path, img_file)

                # Ensure we only process .jpeg, .jpg, or .png files
                if img_file.lower().endswith(('.jpeg', '.jpg', '.png')):
                    img = cv2.imread(img_path)

                    # Check if image is loaded successfully
                    if img is not None:
                        augmented_images = augment_image(img)

                        # Save the original image in the destination folder
                        cv2.imwrite(os.path.join(augmented_celeb_folder, f"{celeb_folder}_{i+1}.png"), img)

                        # Save augmented images with unique names
                        for j, aug_img in enumerate(augmented_images):
                            aug_img_path = os.path.join(augmented_celeb_folder, f"{celeb_folder}_{i+1}_aug_{j+1}.png")
                            cv2.imwrite(aug_img_path, aug_img)
                            print(f"Saved augmented image: {aug_img_path}")
                    else:
                        print(f"Failed to load image: {img_file}")
                else:
                    print(f"Skipped {img_file} (unsupported file format)")

# Define source and destination directories
source_folder = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\cropped'  # Folder containing cropped celebrity images
destination_folder = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\augmented'  # Folder to save augmented images

# Augment all images in bulk
augment_images_in_bulk(source_folder, destination_folder)
