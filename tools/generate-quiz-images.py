#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate themed images for quizzes
"""
from PIL import Image, ImageDraw, ImageFont
import os

def generate_french_history_image(output_path, width=800, height=400):
    """Generate an image for French History quiz"""

    # Create new image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # French flag colors
    draw.rectangle([0, 0, width//3, height], fill='#0055A4')
    draw.rectangle([width//3, 0, 2*width//3, height], fill='#FFFFFF')
    draw.rectangle([2*width//3, 0, width, height], fill='#EF4135')

    # Add a semi-transparent overlay for better text visibility
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 100))
    img_rgba = img.convert('RGBA')
    img_rgba = Image.alpha_composite(img_rgba, overlay)
    img = img_rgba.convert('RGB')
    draw = ImageDraw.Draw(img)

    # Add text with multiple lines for better readability
    try:
        font_large = ImageFont.truetype("arial.ttf", 52)
        font_medium = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except:
        try:
            font_large = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 52)
            font_medium = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40)
            font_small = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 28)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # Title line 1
    text1 = "Histoire"
    bbox1 = draw.textbbox((0, 0), text1, font=font_large)
    text1_width = bbox1[2] - bbox1[0]
    draw.text(((width - text1_width) // 2, height // 2 - 70),
              text1, fill='#FFFFFF', font=font_large, stroke_width=2, stroke_fill='#000000')

    # Title line 2
    text2 = "de France"
    bbox2 = draw.textbbox((0, 0), text2, font=font_large)
    text2_width = bbox2[2] - bbox2[0]
    draw.text(((width - text2_width) // 2, height // 2 - 10),
              text2, fill='#FFFFFF', font=font_large, stroke_width=2, stroke_fill='#000000')

    # Subtitle
    text3 = "1000 Questions"
    bbox3 = draw.textbbox((0, 0), text3, font=font_small)
    text3_width = bbox3[2] - bbox3[0]
    draw.text(((width - text3_width) // 2, height // 2 + 55),
              text3, fill='#FFDD44', font=font_small, stroke_width=1, stroke_fill='#000000')

    # Save image
    img.save(output_path)
    print(f"✓ Image generated: {output_path}")

def generate_world_cities_image(output_path, width=800, height=400):
    """Generate an image for World Cities Latitude/Longitude quiz"""

    # Create new image with ocean gradient
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Blue gradient background (ocean)
    for y in range(height):
        color_val = int(50 + (150 * y / height))
        draw.rectangle([0, y, width, y+1], fill=(20, color_val, 220))

    # Draw latitude lines
    num_lines = 7
    for i in range(num_lines):
        y = int((i + 1) * height / (num_lines + 1))
        draw.line([(0, y), (width, y)], fill='#FFFFFF', width=3)
        # Add small tick marks
        for x in range(0, width, 50):
            draw.line([(x, y-5), (x, y+5)], fill='#FFDD44', width=2)

    # Draw longitude lines
    num_vlines = 9
    for i in range(num_vlines):
        x = int((i + 1) * width / (num_vlines + 1))
        draw.line([(x, 0), (x, height)], fill='#FFFFFF', width=2)

    # Draw continents (simplified shapes)
    # Europe
    draw.ellipse([width*0.45, height*0.15, width*0.55, height*0.35], fill='#228B22', outline='#006400', width=2)
    # Africa
    draw.ellipse([width*0.48, height*0.35, width*0.58, height*0.65], fill='#228B22', outline='#006400', width=2)
    # Asia
    draw.ellipse([width*0.60, height*0.10, width*0.75, height*0.45], fill='#228B22', outline='#006400', width=2)
    # Americas
    draw.ellipse([width*0.15, height*0.20, width*0.25, height*0.50], fill='#228B22', outline='#006400', width=2)
    draw.ellipse([width*0.18, height*0.50, width*0.28, height*0.75], fill='#228B22', outline='#006400', width=2)

    # Add text with multiple lines for better readability
    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_medium = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 26)
    except:
        try:
            font_large = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 48)
            font_medium = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 36)
            font_small = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 26)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()

    # Title line 1 - with shadow
    text1 = "Villes du Monde"
    bbox1 = draw.textbbox((0, 0), text1, font=font_large)
    text1_width = bbox1[2] - bbox1[0]
    x_pos1 = (width - text1_width) // 2
    y_pos1 = height // 2 - 60
    # Shadow
    draw.text((x_pos1 + 3, y_pos1 + 3), text1, fill='#000000', font=font_large)
    # Main text
    draw.text((x_pos1, y_pos1), text1, fill='#FFFFFF', font=font_large, stroke_width=2, stroke_fill='#000000')

    # Title line 2 - with shadow
    text2 = "Latitude &"
    bbox2 = draw.textbbox((0, 0), text2, font=font_medium)
    text2_width = bbox2[2] - bbox2[0]
    x_pos2 = (width - text2_width) // 2
    y_pos2 = y_pos1 + 55
    # Shadow
    draw.text((x_pos2 + 2, y_pos2 + 2), text2, fill='#000000', font=font_medium)
    # Main text
    draw.text((x_pos2, y_pos2), text2, fill='#FFDD44', font=font_medium, stroke_width=1, stroke_fill='#000000')

    # Title line 3 - with shadow
    text3 = "Longitude"
    bbox3 = draw.textbbox((0, 0), text3, font=font_medium)
    text3_width = bbox3[2] - bbox3[0]
    x_pos3 = (width - text3_width) // 2
    y_pos3 = y_pos2 + 45
    # Shadow
    draw.text((x_pos3 + 2, y_pos3 + 2), text3, fill='#000000', font=font_medium)
    # Main text
    draw.text((x_pos3, y_pos3), text3, fill='#FFDD44', font=font_medium, stroke_width=1, stroke_fill='#000000')

    # Save image
    img.save(output_path)
    print(f"✓ Image generated: {output_path}")

def main():
    # Ensure output directory exists
    output_dir = "src/main/resources/static/images"
    os.makedirs(output_dir, exist_ok=True)

    # Generate images
    print("Generating quiz images...")
    print("-" * 50)

    generate_french_history_image(
        os.path.join(output_dir, "french-history-quiz.png")
    )

    generate_world_cities_image(
        os.path.join(output_dir, "world-cities-quiz.png")
    )

    print("-" * 50)
    print("All images generated successfully!")
    print(f"\nImages saved in: {output_dir}")

if __name__ == "__main__":
    main()

