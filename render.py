from PIL import Image, ImageDraw, ImageFont
import sys
import io


def render_text_on_image(input_image_path, text_to_draw, output_image_path=None, font_path="arial-unicode-ms-bold.ttf", font_size=52):
    image = Image.open(input_image_path)

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size)

    text_color = (255, 255, 255)

    image_width, image_height = image.size

    def wrap_text(text, draw, font, max_width):
        words = text.split()
        lines = []
        current_line = []
        current_line_width = 0

        for word in words:
            word_width, word_height = draw.textbbox((0, 0), word, font=font)[2:4]
            space_width = draw.textbbox((0, 0), ' ', font=font)[2]

            if current_line and (current_line_width + word_width + space_width) > max_width:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_line_width = word_width
            else:
                current_line.append(word)
                current_line_width += word_width + space_width
        
        if current_line:
            lines.append(' '.join(current_line))

        return lines

    lines = wrap_text(text_to_draw, draw, font, image_width - 20)  

    total_text_height = sum([draw.textbbox((0, 0), line, font=font)[3] for line in lines])

    current_y = 10

    for line in lines:
        draw.text((10, current_y), line, font=font, fill=text_color)
        
        current_y += draw.textbbox((0, 0), line, font=font)[3] + 5  

        if current_y > image_height:
            break

    if output_image_path:
        image.save(output_image_path)
    
    else:
        file = io.BytesIO()

        image.thumbnail((512, 512))

        image.save(file, format="WEBP")

        file.seek(0)

        return file

WIDTH = 22
HEIGHT = 9

def image_to_string(image_file):

    img = Image.open(image_file)

    img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


    img = img.convert("1")

    # Get image dimensions
    width, height = img.size
    if width != 22 or height != 9:
        raise ValueError("The image must be exactly 22x9 pixels.")
    
    # Create the string representation
    pixel_string = ""
    for y in range(height):
        for x in range(width):
            # Get the pixel value (0 for black, 255 for white)
            pixel = img.getpixel((x, y))
            if pixel == 0:  # Black pixel
                pixel_string += "Ń"
            else:  # White pixel
                pixel_string += "…"
        pixel_string += " "  # New line for each row
    
    return pixel_string


if __name__ == "__main__":

    render_text_on_image("red_ebalo.png", " ".join(sys.argv[1:]), output_image_path="red_ebalo_text.png")
