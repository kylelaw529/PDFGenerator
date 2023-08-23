from PIL import Image as PI
from reportlab.platypus import Image

# dimensions should be a tuple (width, height)
# images should be a list of image paths

# returns list of reportlab image objects

def resize(images, dimensions_of_container):
   
    new_width_max = dimensions_of_container[0]/len(images)
    if len(images)>3:
        new_width_max = dimensions_of_container[0]/3
    new_height_max = dimensions_of_container[1] / (len(images)/3) # dividing by 3 bc that is # of images in a row --> len(images)/3 is the number of rows

    new_images = []

    for i in images:
        img = PI.open(i)
        width,height = img.size

        while width > new_width_max or height > new_height_max:
            width = width/1.2
            height = height/1.2

           
        new_images.append(Image(i, width=width, height=height))
        #new_images.append(Image(i, width=50, height=50))

    return new_images

