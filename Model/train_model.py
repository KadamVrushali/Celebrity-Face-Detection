import os
import joblib
import tensorflow as tf
from keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report

# Function to load images and labels from a directory
def load_images_from_directory(directory, target_size):
    images = []
    labels = []
    class_names = os.listdir(directory)
    
    for label, class_name in enumerate(class_names):
        class_dir = os.path.join(directory, class_name)
        if os.path.isdir(class_dir):
            for img_name in os.listdir(class_dir):
                img_path = os.path.join(class_dir, img_name)
                img = tf.keras.utils.load_img(img_path, target_size=target_size)
                img_array = tf.keras.utils.img_to_array(img)
                images.append(img_array)
                labels.append(label)

    images = np.array(images) / 255.0  # Normalizing the images
    labels = np.array(labels)
    return images, labels, class_names

# Function to build the CNN model
def build_model(input_shape, num_classes):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(num_classes, activation='softmax'))  # Adjust the number of classes as needed

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Function to plot training history
def plot_history(history):
    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1])
    plt.legend(loc='lower right')
    plt.show()

# Main execution
if __name__ == "__main__":
    input_shape = (150, 150, 3)  # Adjust as per your image size
    batch_size = 32               # Adjust batch size as needed
    epochs = 10                   # Number of epochs

    # Set the directories for training and testing datasets
    train_dir = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\train'  # Directory with training data
    test_dir = r'C:\Users\kvrus\OneDrive\Desktop\Projects\Python\DATA SCIENCE\Celebrity_Face_Detection\model\Celebrity_Images\test'  # Directory with test data

    # Load training data
    train_images, train_labels, class_names = load_images_from_directory(train_dir, target_size=(150, 150))
    test_images, test_labels, _ = load_images_from_directory(test_dir, target_size=(150, 150))

    # Check number of classes (for final softmax layer)
    num_classes = len(class_names)
    print(f'Number of classes: {num_classes}')

    # Build model
    model = build_model(input_shape, num_classes)

    # Train model
    history = model.fit(train_images, train_labels, validation_data=(test_images, test_labels), epochs=epochs, batch_size=batch_size)

#save the model
joblib.dump(model, 'saved_model.pkl') 

#Plot history of the model
plot_history(history)

test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
print(f'\nTest accuracy: {test_accuracy:.4f}')

# Predictions
test_predictions = np.argmax(model.predict(test_images), axis=1)

# Calculate Precision, Recall, and F1-score
report = classification_report(test_labels, test_predictions, target_names=class_names)
print("\nClassification Report:")
print(report)
    
