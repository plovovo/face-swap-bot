import numpy as np
import cv2
from PIL import Image
from io import BytesIO

def image_from_bytes(file_bytes):
    image = Image.open(BytesIO(file_bytes)).convert('RGB')
    return np.array(image)[:, :, ::-1]  # RGB → BGR (для OpenCV)

def image_to_bytes(image_array):
    image_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    byte_io = BytesIO()
    pil_image.save(byte_io, format='JPEG')
    byte_io.seek(0)
    return byte_io
