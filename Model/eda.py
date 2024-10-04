import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def count_images_per_celebrity(folder_path):
    """
    Counts the number of images for each celebrity in the dataset.
    
    Parameters:
    folder_path (str): Path to the folder containing the celebrity subfolders with images.
    
    Returns:
    dict: A dictionary where keys are celebrity names and values are the count of images.
    """
    celeb_image_counts = {}
    
    # Loop through each folder (celebrity) in the dataset folder
    for celeb_folder in os.listdir(folder_path):
        celeb_folder_path = os.path.join(folder_path, celeb_folder)
        
        # Ensure it's a directory
        if os.path.isdir(celeb_folder_path):
            # Count the number of images in the celebrity folder
            num_images = len([img for img in os.listdir(celeb_folder_path) if img.lower().endswith(('.jpeg', '.jpg', '.png'))])
            celeb_image_counts[celeb_folder] = num_images
    
    return celeb_image_counts

def plot_celebrity_distribution(celeb_image_counts):
    """
    Plots the distribution of images across celebrities using a bar chart and prints the data.
    
    Parameters:
    celeb_image_counts (dict): A dictionary with celebrity names as keys and image counts as values.
    """
    # Convert the dictionary to a pandas DataFrame for easier plotting
    celeb_data = pd.DataFrame(list(celeb_image_counts.items()), columns=['Celebrity', 'Image Count'])
    
    # Sort the data by image count
    celeb_data = celeb_data.sort_values(by='Image Count', ascending=False)
    
    # Print the image count for each celebrity in text format
    print("Image Count per Celebrity:")
    print(celeb_data.to_string(index=False))

    # Plot a bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Celebrity', y='Image Count', data=celeb_data, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    
    # Call the plot function to set title, labels, and layout
    plot('Image Distribution Across Celebrities', 'Number of Images', 'Celebrity Name')

def plot(title, ylabel, xlabel):
    """
    Sets the title, labels, and layout for a plot.
    
    Parameters:
    title (str): Title of the plot.
    ylabel (str): Label for the y-axis.
    xlabel (str): Label for the x-axis.
    """
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.show()

def basic_eda(celeb_image_counts):
    """
    Performs basic exploratory data analysis on the celebrity image dataset.
    
    Parameters:
    celeb_image_counts (dict): A dictionary with celebrity names as keys and image counts as values.
    """
    celeb_data = pd.Series(celeb_image_counts)
    
    print("Basic Statistics:")
    print(f"Total Celebrities: {len(celeb_data)}")
    print(f"Total Images: {celeb_data.sum()}")
    print(f"Mean Images per Celebrity: {celeb_data.mean():.2f}")
    print(f"Median Images per Celebrity: {celeb_data.median():.2f}")
    print(f"Standard Deviation of Images: {celeb_data.std():.2f}")
    print(f"Celebrity with Most Images: {celeb_data.idxmax()} ({celeb_data.max()} images)")
    print(f"Celebrity with Fewest Images: {celeb_data.idxmin()} ({celeb_data.min()} images)")

# Folder path where all the cropped celebrity images are stored
folder_path = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\augmented'

# Get the image count for each celebrity
celeb_image_counts = count_images_per_celebrity(folder_path)

# Perform EDA
basic_eda(celeb_image_counts)

# Plot the distribution of images and print the results
plot_celebrity_distribution(celeb_image_counts)
