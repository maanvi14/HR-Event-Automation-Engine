import requests
from PIL import Image
from io import BytesIO
import os


def convert_drive_url(url):
    if "drive.google.com" in url:
        try:
            file_id = url.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=download&id={file_id}"
        except:
            return url
    return url


def download_photo(url, name):
    os.makedirs("temp/photos", exist_ok=True)

    try:
        url = convert_drive_url(url)

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # 🔥 catch HTTP errors

        img = Image.open(BytesIO(response.content)).convert("RGB")

        # ================= FIX: RESIZE + COMPRESS =================
        img.thumbnail((800, 800))  # resize (keeps aspect ratio)

        path = f"temp/photos/{name}.jpg"

        img.save(path, "JPEG", quality=80, optimize=True)

        return path

    except Exception as e:
        print("PHOTO ERROR:", e)
        return None
    
    