import os
import random
from django.conf import settings

def get_random_image_from(folder_name: str):
    folder = os.path.join(settings.MEDIA_ROOT, folder_name)
    if not os.path.exists(folder):
        return None
    files = [f for f in os.listdir(folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not files:
        return None
    return os.path.join(folder_name, random.choice(files))