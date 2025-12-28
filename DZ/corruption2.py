from PIL import Image
import io
import random
import numpy as np

def corrupt_image(image_bytes, tameness=0):
    TAMENESS = (100 - tameness) / 100

    img = Image.open(io.BytesIO(image_bytes))
    
    img_array = np.array(img)
    
    # color shift
    while random.random() < 0.66 * TAMENESS:
        shift = random.randint(1, 30)
        img_array[:, :, random.randint(0, 2)] = np.roll(img_array[:, :, 0], shift, axis=1)
        
    # line shift
    while random.random() < 0.8 * TAMENESS:
        for _ in range(random.randint(1, 20)):
            y = random.randint(0, img_array.shape[0] - 1)
            height = random.randint(2, 20)
            shift = random.randint(-25, 25)
            img_array[y:y+height] = np.roll(img_array[y:y+height], shift, axis=1)

    # blocks
    while random.random() <= 0.8 * TAMENESS:
        width = random.randint(1, img_array.shape[1])
        height = random.randint(1, img_array.shape[0])

        x = random.randint(0, img_array.shape[1] - width - 1)
        y = random.randint(0, img_array.shape[0] - height - 1)
    
        img_array[y:y+height, x:x+width, random.randint(0, 2)] = 0
        if random.random() <= 0.66: img_array[y:y+height, x:x+width, random.randint(0, 2)] = 0

    corrupted_img = Image.fromarray(img_array)
    
    img_bytes = io.BytesIO()
    corrupted_img.save(img_bytes, format='JPEG', quality=100)
    img_bytes.seek(0)
    
    return img_bytes.getvalue()
