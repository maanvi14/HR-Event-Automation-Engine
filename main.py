from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

from card_generator import generate_card
from photo_fetcher import download_photo
from cloudinary_uploader import upload_to_cloudinary

app = FastAPI()


# ================= MODEL =================
class Employee(BaseModel):
    employee_id: str
    name: str
    email: str
    dob: str
    joining_date: str
    photo_link: str
    department: str
    event_type: str  # birthday / anniversary


# ================= HEALTH CHECK =================
@app.get("/")
def home():
    return {"status": "HR Card API running on Render 🚀"}


# ================= MAIN API =================
@app.post("/generate-card")
def generate(employee: Employee):
    try:
        data = employee.dict()

        # ================= CALCULATE YEARS =================
        years = None
        if data["event_type"].lower() == "anniversary":
            today = datetime.today()
            joining_date = datetime.strptime(data["joining_date"], "%Y-%m-%d")

            years = today.year - joining_date.year

            if (today.month, today.day) < (joining_date.month, joining_date.day):
                years -= 1

        # ================= DOWNLOAD PHOTO =================
        photo_path = download_photo(data["photo_link"], data["employee_id"])

        if not photo_path:
            raise HTTPException(status_code=400, detail="Failed to download photo")

        # ================= MESSAGE CONTROL =================
        if data["event_type"].lower() == "birthday":
            message = "Wishing you a very happy birthday! All the best for your upcoming year 🎉"
        else:
            message = None

        # ================= GENERATE CARD =================
        card_path = generate_card(
            {
                "employee_id": data["employee_id"],
                "name": data["name"],
                "department": data["department"],
                "event_type": data["event_type"],
                "years": years,
                "message": message
            },
            photo_path
        )

        if not card_path:
            raise HTTPException(status_code=500, detail="Card generation failed")

        # ================= UPLOAD =================
        card_url = upload_to_cloudinary(card_path)

        if not card_url:
            raise HTTPException(status_code=500, detail="Cloud upload failed")

        return {
            "status": "success",
            "employee_id": data["employee_id"],
            "event_type": data["event_type"],
            "card_url": card_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    