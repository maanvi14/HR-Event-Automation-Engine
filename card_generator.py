import os
from PIL import Image, ImageDraw, ImageFont


# ================= FONT LOADER =================
def load_font(size, bold=False):
    try:
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        font_folder = os.path.join(CURRENT_DIR, "fonts")

        font_name = "PlayfairDisplay-Bold.ttf" if bold else "PlayfairDisplay-Regular.ttf"
        path = os.path.join(font_folder, font_name)

        if os.path.exists(path):
            return ImageFont.truetype(path, size)

        return ImageFont.load_default()

    except Exception:
        return ImageFont.load_default()


# ================= MAIN FUNCTION =================
def generate_card(data, photo_path):
    try:
        event_type = data["event_type"].lower().strip()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # ================= OUTPUT =================
        output_dir = os.path.join(BASE_DIR, "temp_cards")
        os.makedirs(output_dir, exist_ok=True)

        # ================= CONFIG =================
        CONFIG = {
            "birthday": {
                "template": "birthday_template.png",
                "circle_cy_pct": 0.50,
                "circle_r_pct": 0.24,
                "name_y_pct": 0.72,
                "msg_gap": 0.09,
                "name_color": "#FFFFFF",
                "msg_color": "#EAEAEA",
                "border_color": "white",
                "uppercase": True
            },
            "anniversary": {
                "template": "anniversary_template.png",
                "circle_cy_pct": 0.44,
                "circle_r_pct": 0.18,
                "name_y_pct": 0.70,
                "msg_gap": 0.09,
                "name_color": "#FFD700",
                "msg_color": "#FFFFFF",
                "border_color": "#F3E48D",
                "uppercase": False
            }
        }

        cfg = CONFIG.get(event_type, CONFIG["birthday"])

        # ================= TEMPLATE =================
        template_path = os.path.join(BASE_DIR, "templates", cfg["template"])
        template = Image.open(template_path).convert("RGBA")
        draw = ImageDraw.Draw(template)

        width, height = template.size

        # ================= ANNIVERSARY HEADER =================
        if event_type == "anniversary":
            header_font = load_font(int(width * 0.055), bold=True)
            years = data.get("years", "")
            header_text = f"Happy {years} Year Work Anniversary!"

            header_w = draw.textbbox((0, 0), header_text, font=header_font)[2]

            draw.text(((width - header_w)//2 + 2, int(height * 0.18) + 2),
                      header_text, font=header_font, fill="black")

            draw.text(((width - header_w)//2, int(height * 0.18)),
                      header_text, font=header_font, fill="white")

        # ================= PHOTO =================
        if photo_path and os.path.exists(photo_path):
            photo = Image.open(photo_path).convert("RGBA")

            # 🔥 MEMORY FIX
            photo = photo.resize((500, 500))

            cx = width // 2
            cy = int(height * cfg["circle_cy_pct"])
            r = int(width * cfg["circle_r_pct"])
            size = r * 2

            photo = photo.crop((0, 0, 500, 500)).resize((size, size), Image.LANCZOS)

            mask = Image.new("L", (size, size), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
            photo.putalpha(mask)

            template.paste(photo, (cx - r, cy - r), photo)

            for i in range(3):
                draw.ellipse(
                    (cx - r - i, cy - r - i, cx + r + i, cy + r + i),
                    outline=cfg["border_color"]
                )

            photo.close()  # 🔥 MEMORY FIX

        # ================= NAME =================
        name_text = data["name"].upper() if cfg["uppercase"] else data["name"].title()

        font_size = int(width * 0.11)

        while True:
            name_font = load_font(font_size, bold=True)
            name_w = draw.textbbox((0, 0), name_text, font=name_font)[2]

            if name_w < width * 0.85 or font_size < 30:
                break
            font_size -= 2

        ny = int(height * cfg["name_y_pct"])

        draw.text(((width - name_w)//2 + 2, ny + 2),
                  name_text, font=name_font, fill="black")

        draw.text(((width - name_w)//2, ny),
                  name_text, font=name_font, fill=cfg["name_color"])

        # ================= MESSAGE =================
        msg_font = load_font(int(width * 0.048))

        if event_type == "anniversary":
            lines = [
                "Celebrating your dedication and hard work,",
                "wishing you continued success ahead!"
            ]
        else:
            lines = [
                "Wishing you a very happy birthday!",
                "All the best for your upcoming year 🎉"
            ]

        my = ny + int(height * cfg["msg_gap"])

        for line in lines:
            line_w = draw.textbbox((0, 0), line, font=msg_font)[2]

            draw.text(((width - line_w)//2 + 1, my + 1),
                      line, font=msg_font, fill="black")

            draw.text(((width - line_w)//2, my),
                      line, font=msg_font, fill=cfg["msg_color"])

            my += int(height * 0.055)

        # ================= SAVE =================
        filename = f"{data['employee_id']}_{event_type}.png"
        out_path = os.path.join(output_dir, filename)

        template.save(out_path)

        template.close()  # 🔥 MEMORY FIX

        return out_path

    except Exception as e:
        print("CARD ERROR:", e)
        return None