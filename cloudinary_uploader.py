import cloudinary
import cloudinary.uploader
import os
import uuid


# ================= CONFIG =================
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


# ================= UPLOAD FUNCTION =================
def upload_to_cloudinary(file_path):
    try:
        if not file_path or not os.path.exists(file_path):
            print("Invalid file path")
            return None

        # Unique filename
        public_id = f"hr_cards/{uuid.uuid4().hex}"

        response = cloudinary.uploader.upload(
            file_path,
            public_id=public_id,
            resource_type="image",
            quality="auto",        # 🔥 auto optimize
            fetch_format="auto"    # 🔥 best format (webp/jpg)
        )

        return response.get("secure_url")

    except Exception as e:
        print("CLOUDINARY ERROR:", e)
        return None
    
    