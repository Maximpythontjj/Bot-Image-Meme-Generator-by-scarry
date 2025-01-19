from PIL import ImageSequence, ImageDraw, ImageFont

def add_text_to_gif(gif, text, font_path, font_size):
    frames = []
    font = ImageFont.truetype(font_path, size=font_size)
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        draw = ImageDraw.Draw(frame)
        text_width, text_height = draw.textsize(text, font=font)
        x = (frame.width - text_width) / 2
        y = frame.height - text_height - 10
        draw.text((x, y), text, font=font, fill="white", stroke_width=2, stroke_fill="black")
        frames.append(frame)
    return frames