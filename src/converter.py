from threading import Thread
from typing import Tuple, Callable

import numpy as np
from PIL import Image


def rgb_to_hex565(image: np.ndarray) -> np.ndarray:
    r = (image[..., 0] * 31 / 255).astype(np.uint16) << 11
    g = (image[..., 1] * 63 / 255).astype(np.uint16) << 5
    b = (image[..., 2] * 31 / 255).astype(np.uint16)
    return r | g | b


def convert(filepaths: list[str], output_path: str, size: Tuple[int, int], progress_handler: Callable[[float], None]):
    file_count = len(filepaths)
    progress = 0

    try:
        with open(output_path, "w") as f:
            f.write("int frames = {0};\n".format(file_count))
            f.write("int width = {0};\n".format(size[0]))
            f.write("int height = {0};\n".format(size[1]))
            f.write("const uint16_t data[{0}][{1}] PROGMEM = ".format(len(filepaths), (size[0] * size[1])))
            f.write("{\n")
            f.write("{")

            for image_index, path in enumerate(filepaths):
                progress = float(image_index + 1) / file_count
                progress_handler(progress)

                image = Image.open(path).resize(size)

                image = np.asarray(image, dtype=np.uint16)
                rgb565_array = rgb_to_hex565(image)

                hex_values = ", ".join(f"0x{val:04X}" for val in rgb565_array.flatten())
                f.write(f" {hex_values}")

                f.write("}")
                if image_index != file_count - 1:
                    f.write(",\n{")

            f.write("\n};")
    finally:
        if progress < 1:
            progress_handler(1)


def start_conversion(filepaths: list[str], output_path: str, size: Tuple[int, int],
                     progress_handler: Callable[[float], None]):
    thread = Thread(target=convert, args=(filepaths, output_path, size, progress_handler))
    thread.start()
