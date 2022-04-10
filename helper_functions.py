import glob
import os
from PIL import Image
import typing


def load_photo(filename: str) -> Image.Image:
    return Image.open(filename)


def get_image_files_in_directory(
    dir_name: str, extension_list: typing.List[str] = None
) -> typing.List[str]:
    if extension_list is None:
        extension_list = [".jpg", ".jpeg", ".png", ".gif", ".tif"]
    extensions = (f"*{e}" for e in extension_list)
    file_list = []
    for f in extensions:
        file_list.extend(glob.glob(os.path.join(dir_name, f)))

    return file_list


def load_images_from_directory(dir_name: str) -> typing.List[Image.Image]:

    file_list = get_image_files_in_directory(dir_name)

    image_list = []
    for f in file_list:
        try:
            image_list.append(load_photo(f))
        except Exception:
            print("Unable to load image")

    return image_list
