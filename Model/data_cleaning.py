import os
import cv2
import matplotlib.pyplot as plt
import shutil

# Load face and eye cascades
face_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('./opencv/haarcascades/haarcascade_eye.xml')

# Function to display an image
def display_image(image, cmap=None):
    """Displays an image using matplotlib."""
    plt.figure()
    plt.imshow(image, cmap=cmap)
    plt.axis('off')
    plt.show()

# Function to convert an image to grayscale
def to_gray(image):
    """Converts an image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Function to detect a face and check if it has two eyes
def detect_2eyes(image_path):
    """Detects face and checks if two eyes are present."""
    img = cv2.imread(image_path)

    # Check if image was loaded successfully
    if img is None:
        print(f"Error loading image: {image_path} (image is None)")
        return None
    
    try:
        gray = to_gray(img)
    except cv2.error as e:
        print(f"Error processing image: {image_path} - {str(e)}")
        return None
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        # Return cropped image only if there are two or more eyes detected
        if len(eyes) >= 2:
            return roi_color
    
    return None

# Pipeline to process bulk images
def process_images_in_bulk(source_folder, dest_folder):
    """
    Processes all images in the source_folder and saves cropped images of celebrities
    with two detected eyes in the dest_folder.
    """
    # Create destination folder if it doesn't exist
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    os.mkdir(dest_folder)

    display_first_image = True  # To ensure only the first image is displayed

    # For each celebrity folder inside the source folder
    for celeb_folder in os.listdir(source_folder):
        celeb_folder_path = os.path.join(source_folder, celeb_folder)
        
        if os.path.isdir(celeb_folder_path):
            print(f"Processing folder: {celeb_folder}")

            # Create a corresponding folder in the destination directory
            cropped_celeb_folder = os.path.join(dest_folder, celeb_folder)
            os.makedirs(cropped_celeb_folder, exist_ok=True)

            # Process each image in the celebrity folder
            for i, img_file in enumerate(os.listdir(celeb_folder_path)):
                img_path = os.path.join(celeb_folder_path, img_file)

                # Ensure we only process .jpeg or .jpg files
                if img_file.lower().endswith(('.jpeg', '.jpg')):
                    cropped_img = detect_2eyes(img_path)

                    if cropped_img is not None:
                        cropped_img_path = os.path.join(cropped_celeb_folder, f"{celeb_folder}_{i+1}.png")
                        cv2.imwrite(cropped_img_path, cropped_img)
                        print(f"Saved cropped image: {cropped_img_path}")
                        
                        # Display only the first image
                        if display_first_image:
                            display_image(cropped_img)
                            display_first_image = False
                    else:
                        print(f"Skipped {img_file} (no face with 2 eyes detected)")
                else:
                    print(f"Skipped {img_file} (unsupported file format)")

# Define source and destination directories
source_folder = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images'  # Folder containing celebrity folders
destination_folder = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\cropped'  # Folder to save cropped images

# Process all images in bulk from the source folder
process_images_in_bulk(source_folder, destination_folder)
