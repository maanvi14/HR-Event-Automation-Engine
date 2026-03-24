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

    except Exception as e:
        print("FONT ERROR:", e)
        return ImageFont.load_default()


# ================= TEXT WRAP =================
def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""

    for w in words:
        test = (current + " " + w).strip()
        width = draw.textbbox((0, 0), test, font=font)[2]

        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w

    if current:
        lines.append(current)

    return lines


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
                "msg_gap": 0.08,
                "name_color": "white",
                "msg_color": "white",
                "border_color": "white",
                "uppercase": True,
                "header": "Happy Birthday 🎉",
                "default_msg": "Wishing you a fantastic birthday filled with joy and success!"
            },
            "anniversary": {
                "template": "anniversary_template.png",
                "circle_cy_pct": 0.44,
                "circle_r_pct": 0.18,
                "name_y_pct": 0.70,
                "msg_gap": 0.08,
                "name_color": "#FFD700",
                "msg_color": "#FFFFFF",
                "border_color": "#F3E48D",
                "uppercase": False,
                "header": "Happy Work Anniversary 🎉",
                "default_msg": "Celebrating your dedication and contribution!"
            }
        }

        cfg = CONFIG.get(event_type, CONFIG["birthday"])

        # ================= TEMPLATE =================
        template_path = os.path.join(BASE_DIR, "templates", cfg["template"])

        if not os.path.exists(template_path):
            raise Exception(f"Template not found: {template_path}")

        template = Image.open(template_path).convert("RGBA")
        draw = ImageDraw.Draw(template)

        width, height = template.size

        # ================= HEADER =================
        header_font = load_font(int(width * 0.07), bold=True)
        header_text = cfg["header"]

        header_w = draw.textbbox((0, 0), header_text, font=header_font)[2]

        draw.text(((width - header_w)//2 + 2, int(height * 0.18) + 2),
                  header_text, font=header_font, fill="black")

        draw.text(((width - header_w)//2, int(height * 0.18)),
                  header_text, font=header_font, fill="white")

        # ================= PHOTO =================
        if photo_path and os.path.exists(photo_path):
            photo = Image.open(photo_path).convert("RGBA")

            cx = width // 2
            cy = int(height * cfg["circle_cy_pct"])
            r = int(width * cfg["circle_r_pct"])
            size = r * 2

            w_p, h_p = photo.size
            m = min(w_p, h_p)

            photo = photo.crop((
                (w_p - m)//2,
                (h_p - m)//2,
                (w_p + m)//2,
                (h_p + m)//2
            )).resize((size, size), Image.LANCZOS)

            mask = Image.new("L", (size, size), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
            photo.putalpha(mask)

            template.paste(photo, (cx - r, cy - r), photo)

            # glow border
            for i in range(3):
                draw.ellipse(
                    (cx - r - i, cy - r - i, cx + r + i, cy + r + i),
                    outline=cfg["border_color"]
                )

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

        # glow effect
        for offset in range(2):
            draw.text(((width - name_w)//2 - offset, ny),
                      name_text, font=name_font, fill="#FFD700")

        draw.text(((width - name_w)//2 + 3, ny + 3),
                  name_text, font=name_font, fill="black")

        draw.text(((width - name_w)//2, ny),
                  name_text, font=name_font, fill=cfg["name_color"])

        # ================= MESSAGE =================
        message = data.get("message") or cfg["default_msg"]

        msg_font = load_font(int(width * 0.05))
        lines = wrap_text(draw, message, msg_font, int(width * 0.75))

        my = ny + int(height * cfg["msg_gap"])

        for line in lines:
            line_w = draw.textbbox((0, 0), line, font=msg_font)[2]

            draw.text(((width - line_w)//2 + 1, my + 1),
                      line, font=msg_font, fill="black")

            draw.text(((width - line_w)//2, my),
                      line, font=msg_font, fill=cfg["msg_color"])

            my += int(height * 0.05)

        # ================= SAVE =================
        filename = f"{data['employee_id']}_{event_type}.png"
        out_path = os.path.join(output_dir, filename)

        template.save(out_path)

        return out_path

    except Exception as e:
        print("CARD GENERATION ERROR:", e)
        return None
    
    