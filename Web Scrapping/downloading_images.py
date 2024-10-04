import os
import time
import base64
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the Selenium WebDriver (Chrome)
driver = webdriver.Chrome()

# List of celebrity names and years
CelebName = [
    "Selena Gomez 2016 face", "Selena Gomez 2017 face", "Selena Gomez 2018 face", "Selena Gomez 2019 face", "Selena Gomez 2020 face", "Selena Gomez 2021 face", "Selena Gomez 2022 face",
    "Taylor Swift 2015 face", "Taylor Swift 2016 face", "Taylor Swift 2017 face", "Taylor Swift 2018 face", "Taylor Swift 2019 face", "Taylor Swift 2020 face", "Taylor Swift 2021 face", "Taylor Swift 2022 face",
    "Beyonce 2015 face", "Beyonce 2016 face", "Beyonce 2017 face", "Beyonce 2018 face", "Beyonce 2019 face", "Beyonce 2020 face", "Beyonce 2021 face", "Beyonce 2022 face",
    "Ariana Grande 2015 face", "Ariana Grande 2016 face", "Ariana Grande 2017 face", "Ariana Grande 2018 face", "Ariana Grande 2019 face", "Ariana Grande 2020 face", "Ariana Grande 2021 face", "Ariana Grande 2022 face",
    "Ed Sheeran 2015 face", "Ed Sheeran 2016 face", "Ed Sheeran 2017 face", "Ed Sheeran 2018 face", "Ed Sheeran 2019 face", "Ed Sheeran 2020 face", "Ed Sheeran 2021 face", "Ed Sheeran 2022 face",
    "Bruno Mars 2015 face", "Bruno Mars 2016 face", "Bruno Mars 2017 face", "Bruno Mars 2018 face", "Bruno Mars 2019 face", "Bruno Mars 2020 face", "Bruno Mars 2021 face", "Bruno Mars 2022 face",
    "Shawn Mendes 2015 face", "Shawn Mendes 2016 face", "Shawn Mendes 2017 face", "Shawn Mendes 2018 face", "Shawn Mendes 2019 face", "Shawn Mendes 2020 face", "Shawn Mendes 2021 face", "Shawn Mendes 2022 face",
    "Zayn Malik 2015 face", "Zayn Malik 2016 face", "Zayn Malik 2017 face", "Zayn Malik 2018 face", "Zayn Malik 2019 face", "Zayn Malik 2020 face", "Zayn Malik 2021 face", "Zayn Malik 2022 face"
]

# Create the main folder to save all images
main_save_path = r"C:\Users\kvrus\Downloads\dad_demo"
os.makedirs(main_save_path, exist_ok=True)

# Function to download images
def download_images(image_elements, save_path, celeb, year):
    for i, img in enumerate(image_elements):
        img_url = img.get_attribute("src")

        if img_url and img_url.startswith('data:image'):
            # Handle base64 images
            header, encoded = img_url.split(",", 1)
            image_data = base64.b64decode(encoded)

            # Filter: Only save the image if it's larger than 10KB
            if len(image_data) > 10240:  # 10KB = 10 * 1024 bytes
                with open(os.path.join(save_path, f"{celeb}_{year}_image_{i+1}.jpg"), "wb") as f:
                    f.write(image_data)
                print(f"Downloaded base64 image: {celeb}_{year}_image_{i+1}.jpg")
            else:
                print(f"Skipped base64 image (size < 10KB): {celeb}_{year}_image_{i+1}.jpg")

        elif img_url and "http" in img_url:
            # Handle regular image URLs
            try:
                img_data = requests.get(img_url).content
                # Filter: Only save the image if it's larger than 10KB
                if len(img_data) > 10240:  # 10KB = 10 * 1024 bytes
                    with open(os.path.join(save_path, f"{celeb}_{year}_image_{i+1}.jpg"), "wb") as f:
                        f.write(img_data)
                    print(f"Downloaded image: {celeb}_{year}_image_{i+1}.jpg")
                else:
                    print(f"Skipped image (size < 10KB): {celeb}_{year}_image_{i+1}.jpg")
            except Exception as e:
                print(f"Failed to download image from {img_url}: {e}")

# Loop through the list of CelebName
for celeb in CelebName:
    # Extract celebrity name and year
    parts = celeb.split()
    celeb_name = " ".join(parts[:-2])  # e.g., "Selena Gomez"
    year = parts[-2]  # e.g., "2016"

    # Create a folder for the celebrity (without spaces in folder name)
    celeb_folder = celeb_name.replace(" ", "")
    celeb_save_path = os.path.join(main_save_path, celeb_folder)
    os.makedirs(celeb_save_path, exist_ok=True)

    # Create the Google search URL for the celebrity
    url = f"https://www.google.com/search?q={celeb}+images&tbm=isch"
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(3)
    
    # Scroll down to load more images
    scroll_pause_time = 2
    scrolls = 5

    for i in range(scrolls):
        # Scroll down by 1000 pixels each time
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(scroll_pause_time)
        scroll_pause_time += 1

    # Find image elements
    image_elements = driver.find_elements(By.TAG_NAME, "img")

    # Download images for the current celebrity into their individual folder
    download_images(image_elements, celeb_save_path, celeb_folder, year)

# Close the browser
driver.quit()
