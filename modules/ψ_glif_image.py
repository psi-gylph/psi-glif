# ~/psi_lab/modules/ψ_glif_image.py

from PIL import Image, ImageDraw, ImageFont

def ascii_to_image(ascii_str, output_path="glif.png"):
    lines = ascii_str.strip().split('\n')
    font = ImageFont.load_default()

    width = max([font.getsize(line)[0] for line in lines])
    height = font.getsize(lines[0])[1] * len(lines)

    img = Image.new("RGB", (width + 20, height + 20), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    y_offset = 10
    for line in lines:
        draw.text((10, y_offset), line, font=font, fill=(0, 0, 0))
        y_offset += font.getsize(line)[1]

    img.save(output_path)
    return output_path
    
def ascii_to_image(ascii_str, output_path="glif.png"):
    lines = ascii_str.strip().split('\n')
    font = ImageFont.load_default()

    width = max([font.getsize(line)[0] for line in lines])
    height = font.getsize(lines[0])[1] * len(lines)

    img = Image.new("RGB", (width + 20, height + 20), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    y_offset = 10
    for line in lines:
        draw.text((10, y_offset), line, font=font, fill=(0, 0, 0))
        y_offset += font.getsize(line)[1]

    img.save(output_path)
    return output_path

def ascii_to_image(ascii_art, output_path="glif.png", font_path="/Library/Fonts/Andale Mono.ttf", font_size=14):
    lines = ascii_art.split("\n")
    width = max(len(line) for line in lines)
    height = len(lines)

    image = Image.new("RGB", (font_size * width, font_size * height), "white")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    for i, line in enumerate(lines):
        draw.text((0, i * font_size), line, fill="black", font=font)

    image.save(output_path)
    return output_path

def ascii_to_image(ascii_str, output_path="glif.png", font_size=10):
    lines = ascii_str.splitlines()
    width = max(len(line) for line in lines)
    height = len(lines)

    font = ImageFont.load_default()
    img = Image.new("RGB", (width * font_size // 2, height * font_size), color="white")
    draw = ImageDraw.Draw(img)

    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill="black")
        y += font_size
    img.save(output_path)
    return os.path.abspath(output_path)
