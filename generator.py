import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageColor

COLORS = ["lightgreen", "darkgreen", "blue", "white", "orange", "red", "black", "yellow", "brown"]
COLORS_RGB = [np.array(ImageColor.getrgb(color)) for color in COLORS]

def get_color(pixel: np.array):
    closest = None
    distance = 100000
    for color in COLORS_RGB:
        dist = np.sum((color - pixel) ** 2)
        if dist < distance:
            distance = dist
            closest = color
    return closest

def convert_image(image: Image):
    im = np.array(image)
    height, width, channels = im.shape
    im_out = np.zeros((height, width, channels))

    for y in range(height):
        for x in range(width):
            im_out[y,x,:] = get_color(im[y,x])

    return Image.fromarray(im_out.astype('uint8'), 'RGB')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="path to source image",
                        type=str)
    parser.add_argument("out", help="path to output image",
                        type=str, default="out.png")
    parser.add_argument("--dims", help="number of pixels in each dimension",
                        type=int, required=False, default=10)
    parser.add_argument("--show", help="show output image",
                        type=bool, required=False, default=False)
    args = parser.parse_args()

    image_path = args.image
    out_path = args.out
    dims = args.dims
    show = args.show

    image = Image.open(image_path).convert("RGB").resize((dims, dims), resample=Image.NEAREST)
    new_image = convert_image(image).resize((dims * 40, dims * 40), resample=Image.NEAREST)

    # Draw lines
    draw = ImageDraw.Draw(new_image)
    y_start = 0
    y_end = new_image.height
    step_size = int(new_image.width / dims)

    for x in range(0, new_image.width, step_size):
        line = ((x, y_start), (x, y_end))
        draw.line(line, fill="white")

    x_start = 0
    x_end = new_image.width

    for y in range(0, new_image.height, step_size):
        line = ((x_start, y), (x_end, y))
        draw.line(line, fill="white")

    del draw

    if show:
        new_image.show()
    new_image.save(out_path)

    