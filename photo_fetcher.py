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
        img = Image.open(BytesIO(response.content)).convert("RGB")

        path = f"temp/photos/{name}.png"
        img.save(path)

        return path

    except Exception as e:
        print("PHOTO ERROR:", e)
        return None

        