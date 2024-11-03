import argparse
import os

from PIL import Image, ImageOps

image_extensions = (".png", ".jpg")


def read_image_files(dir: str) -> list[str]:
    return [file for file in os.listdir(dir) if file.lower().endswith(image_extensions)]


def save_image(img: Image, image_path: str, output_dir: str):
    # Save or display the final padded image
    file_name = os.path.basename(image_path)
    img.save(os.path.join(output_dir, file_name))


def resize_with_same_aspect(img: Image, target_width=1024, target_height=1024):
    size = target_width if img.width >= img.height else target_height
    return img.resize(size, Image.LANCZOS)


def pad(
    img: Image, target_width=1024, target_height=1024, padding_color=(255, 255, 255)
):
    # Calculate padding to make the image square
    left_right_padding = (
        (target_width - img.width) // 2 if target_width > img.width else 0
    )
    top_bottom_padding = (
        (target_height - img.height) // 2 if target_height > img.height else 0
    )

    if left_right_padding is 0 and top_bottom_padding is 0:
        return img

    # Add padding to make the image square
    return ImageOps.expand(
        img,
        (
            left_right_padding,
            top_bottom_padding,
            left_right_padding,
            top_bottom_padding,
        ),
        padding_color,
    )


def resize(input_dir: str, target_width=1024, target_height=1024):
    output_dir = os.path.join(input, "resized")
    image_files = read_image_files(input_dir)

    for index, image_path in enumerate(image_files):
        with Image.open(image_path) as img:
            resized = img

            # Resize original as needed image as needed
            if img.height > target_height or img.width > target_width:
                resized = resize_with_same_aspect(
                    img=resized, target_width=target_width, target_height=target_height
                )

            # Pad image out to match requirement
            if img.height < target_height or img.width < target_width:
                resized = pad(
                    img=resized, target_width=target_width, target_height=target_height
                )
                save_image(img=resized, image_path=image_path, output_dir=output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="resize_images",
        description="""
        Resize a dir of images for training. 
        This will keep the original aspect ratio of the images, shrinking or expanding as required 
        and pad them out as necessary using white padding.
        """,
    )
    parser.add_argument("image_dir", type=str, help="The path to the image directory")
    parser.add_argument("target_width", type=int, help="Target width of the new image")
    parser.add_argument("target_height", type=int, help="Target width of the new image")
    args = parser.parse_args()
    resize(
        dir=args.image_dir,
        target_width=args.target_width,
        target_height=args.target_height,
    )
