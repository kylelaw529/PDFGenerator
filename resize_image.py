
import os
from PIL import Image

def resize_images(directory, target_size=(300, 300)):
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            filepath = os.path.join(directory, filename)
            try:
                image = Image.open(filepath)
                image.thumbnail(target_size)

                # Remove whitespace
                image = image.crop(image.getbbox())

                image.save(filepath)
                print(f"Resized and saved {filename}")
            except Exception as e:
                print(f"Failed to resize {filename}: {str(e)}")

# Example usage
directory = "alumni logos"
resize_images(directory)