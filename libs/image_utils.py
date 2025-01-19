from PIL import Image, ImageDraw, ImageFont

def add_text_to_image(image, text, font_path, font_size):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, size=font_size)
    text_width, text_height = draw.textsize(text, font=font)
    x = (image.width - text_width) / 2
    y = image.height - text_height - 10
    draw.text((x, y), text, font=font, fill="white", stroke_width=2, stroke_fill="black")
    return image