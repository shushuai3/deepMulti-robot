# File may be useful. Rotate the ppm images
from PIL import Image
for i in range(1, 21):
    path_image = "img{:05d}.ppm".format(i)
    image = Image.open(path_image)
    rotated = image.rotate(180)
    rotated.save("rot"+path_image)
    # rotated.show()