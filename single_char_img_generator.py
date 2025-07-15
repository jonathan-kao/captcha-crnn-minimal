import os
import random
import argparse
from PIL import Image, ImageDraw, ImageFont

LETTERS = "abcdefghijklmnopqrstuvwxyz"
IMG_WIDTH = 30
IMG_HEIGHT = 100
FONT_SIZE = 50


def apply_random_horizontal_stretch(img, segments=4, scale_range=(0.8, 1.2)):
    """
        horizontal slicing and randomly stretch the width of each segment
        - segments: number of segments (higher means finer and smoother variations)
        - scale_range: range of scaling factors applied to each segment’s width
    """
    w, h = img.size
    segment_width = w // segments
    new_img = Image.new("L", (w, h), color=0)

    current_x = 0
    for i in range(segments):
        x0 = i * segment_width
        x1 = (i + 1) * segment_width if i < segments - 1 else w
        seg = img.crop((x0, 0, x1, h))

        scale = random.uniform(*scale_range)
        new_width = max(1, int((x1 - x0) * scale))
        seg = seg.resize((new_width, h), resample=Image.BILINEAR)

        new_img.paste(seg, (current_x, 0))
        current_x += new_width

    return new_img.crop((0, 0, w, h))


def apply_random_vertical_stretch(img, segments=4, scale_range=(0.8, 1.2)):
    """
        vertical slicing and randomly stretch the height of each segment
        - segments: number of segments (higher means finer and smoother variations)
        - scale_range: range of scaling factors applied to each segment’s height
    """
    w, h = img.size
    segment_height = h // segments
    new_img = Image.new("L", (w, h), color=0)

    current_y = 0
    for i in range(segments):
        y0 = i * segment_height
        y1 = (i + 1) * segment_height if i < segments - 1 else h
        seg = img.crop((0, y0, w, y1))

        scale = random.uniform(*scale_range)
        new_height = max(1, int((y1 - y0) * scale))
        seg = seg.resize((w, new_height), resample=Image.BILINEAR)

        new_img.paste(seg, (0, current_y))
        current_y += new_height

    return new_img.crop((0, 0, w, h))


def apply_random_affine(img):
    # Random rotation within ±15°
    angle = random.uniform(-15, 15)
    img = img.rotate(angle, fillcolor=0)

    # Random X (±2px) and Y (±5px) translation
    dx = random.randint(-2, 2)
    dy = random.randint(-5, 5)
    img = img.transform(
        img.size,
        Image.AFFINE,
        (1, 0, dx, 0, 1, dy),
        fillcolor=0
    )
    return img


def apply_random_erasing(img, p=1):
    if random.random() > p:
        return img

    draw = ImageDraw.Draw(img)
    w, h = img.size
    erase_w = random.randint(int(w * 0.1), int(w * 0.4))
    erase_h = random.randint(int(h * 0.1), int(h * 0.4))
    x1 = random.randint(0, w - erase_w)
    y1 = random.randint(0, h - erase_h)
    draw.rectangle([x1, y1, x1 + erase_w, y1 + erase_h], fill=0)
    return img


def generate_single_letter_images(font_path, output_dir, num_samples):
    os.makedirs(output_dir, exist_ok=True)
    font = ImageFont.truetype(font_path, FONT_SIZE)

    for letter in LETTERS:
        letter_dir = os.path.join(output_dir, letter)
        os.makedirs(letter_dir, exist_ok=True)

        for i in range(num_samples):
            # black background
            img = Image.new("L", (IMG_WIDTH, IMG_HEIGHT), color=0)
            draw = ImageDraw.Draw(img)

            # put character in the middle
            bbox = draw.textbbox((0, 0), letter, font=font)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x = (IMG_WIDTH - w) // 2 - bbox[0]
            y = (IMG_HEIGHT - h) // 2 - bbox[1]
            draw.text((x, y), letter, fill=255, font=font)

            # apply augmentation
            img = apply_random_affine(img)
            img = apply_random_horizontal_stretch(img)
            img = apply_random_vertical_stretch(img)
            img = apply_random_erasing(img)

            img.save(os.path.join(letter_dir, f"{letter}_{i}.png"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate augmented single-letter images.")
    parser.add_argument("--font", type=str, required=True, help="Path to the TTF font file.")
    parser.add_argument("--output", type=str, default="single_char_images", help="Output directory for images.")
    parser.add_argument("--num_samples", type=int, default=200, help="Number of samples per letter.")
    args = parser.parse_args()

    generate_single_letter_images(args.font, args.output, args.num_samples)
