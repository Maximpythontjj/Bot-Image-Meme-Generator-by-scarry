import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import io
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

FONT_PATH = "text/ofont.ru_Impact.ttf"

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Шрифт не найден по пути {FONT_PATH}")

@bot.command(name="memz")
async def create_memz(ctx, text: str):
    if not ctx.message.attachments:
        await ctx.send("Пожалуйста, прикрепите изображение для создания мема!")
        return

    attachment = ctx.message.attachments[0]
    image_bytes = await attachment.read()
    image = Image.open(io.BytesIO(image_bytes))

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, size=int(image.height * 0.1))

    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    x = (image.width - text_width) / 2
    y = image.height - text_height - 10

    draw.text((x, y), text, font=font, fill="white", stroke_width=2, stroke_fill="black")

    output_buffer = io.BytesIO()
    image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    file = discord.File(fp=output_buffer, filename="memz.png")
    await ctx.send(file=file)

@bot.command(name="memzgif")
async def create_memzgif(ctx, text: str):
    if not ctx.message.attachments:
        await ctx.send("Пожалуйста, прикрепите GIF для создания мема!")
        return

    attachment = ctx.message.attachments[0]
    gif_bytes = await attachment.read()
    gif = Image.open(io.BytesIO(gif_bytes))

    font = ImageFont.truetype(FONT_PATH, size=int(gif.height * 0.1))

    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        draw = ImageDraw.Draw(frame)

        text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
        x = (frame.width - text_width) / 2
        y = frame.height - text_height - 10

        draw.text((x, y), text, font=font, fill="white", stroke_width=2, stroke_fill="black")
        frames.append(frame)

    output_buffer = io.BytesIO()
    frames[0].save(output_buffer, format="GIF", save_all=True, append_images=frames[1:], loop=0, duration=gif.info.get("duration", 100))
    output_buffer.seek(0)

    file = discord.File(fp=output_buffer, filename="memz.gif")
    await ctx.send(file=file)

bot.run("DISCORD_BOT_TOKEN")
