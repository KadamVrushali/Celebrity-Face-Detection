import os
import shutil
import random

def split_dataset(source_dir, train_dir, test_dir, split_ratio=0.8):
    # Create train and test directories if they don't exist
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Iterate over each class in the source directory
    for class_name in os.listdir(source_dir):
        class_path = os.path.join(source_dir, class_name)

        # Check if the path is a directory
        if os.path.isdir(class_path):
            # Create class subdirectories in train and test directories
            os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
            os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)

            # Get a list of all files in the class directory
            files = os.listdir(class_path)
            random.shuffle(files)  # Shuffle the files for randomness

            # Calculate split index
            split_index = int(len(files) * split_ratio)

            # Move files to training and testing directories
            for i, file in enumerate(files):
                if i < split_index:
                    shutil.move(os.path.join(class_path, file), os.path.join(train_dir, class_name, file))
                else:
                    shutil.move(os.path.join(class_path, file), os.path.join(test_dir, class_name, file))

# Example usage
source_data_dir = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\balanced_dataset'  # Your dataset path
train_data_dir = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\train'  # Directory to save training data
test_data_dir = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\test'  # Directory to save test data

split_dataset(source_data_dir, train_data_dir, test_data_dir, split_ratio=0.8)
