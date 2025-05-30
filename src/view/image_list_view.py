from typing import Tuple, Callable

import customtkinter as cttk

from src.view import *


class ImageListView(cttk.CTkFrame):
    IMAGE_SIZE: Tuple[int, int] = (200, 200)

    def __init__(self, parent, on_remove_image: Callable[[str], None]):
        super().__init__(parent)
        self.image_list: list[ImageView] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.scrollable_frame = cttk.CTkScrollableFrame(master=self, width=160,
                                                        fg_color="#2b2b2b",
                                                        scrollbar_button_color="#333333")
        self.scrollable_frame.grid(row=0, column=0, sticky=cttk.NSEW, padx=5, pady=5)
        self.scrollable_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.on_remove_image = on_remove_image

    def add_image(self, path: str):
        if not path:
            return

        index = len(self.image_list)
        image_view = self.__create_image(path, index)
        image_view.grid(row=index, column=1)

        self.image_list.append(image_view)

    def __create_image(self, path: str, index: int):
        image_view = ImageView(self.scrollable_frame, path, index, self.__swap_image, self.on_remove_image, self.IMAGE_SIZE)

        return image_view

    def remove_all(self):
        for image in self.image_list:
            image.destroy()
        self.image_list.clear()

    def __swap_image(self, image_view):
        index = self.image_list.index(image_view)
        if index > 0:
            self.image_list[index], self.image_list[index - 1] = self.image_list[index - 1], self.image_list[index]
            self.image_list[index].grid(row=index)
            self.image_list[index - 1].grid(row=index - 1)

        if index - 1 == 0:
            self.image_list[index].redraw(index)
            self.image_list[index - 1].redraw(index - 1)

    def __remove_image_view(self, image):
        if image in self.image_list:
            self.image_list.remove(image)
            image.destroy()
            self.image_list[0].redraw(0)
            self.__update_image_row()

    def remove_image_by_path(self, path):
        image = next((image for image in self.image_list if image.file_path == path), None)
        if image is not None:
            if image in self.image_list:
                self.image_list.remove(image)
                if len(self.image_list) > 0:
                    self.image_list[0].redraw(0)
            image.destroy()
        self.__update_image_row()

    def __update_image_row(self, start_from: int = 0):
        for index, image in enumerate(self.image_list[start_from:]):
            image.grid(row=index)

    def get_image_path_list(self):
        return list(map(lambda x: x.file_path, self.image_list))

    def resize_all_images(self, size: Tuple[int, int]):
        self.IMAGE_SIZE = size
        for index, image in enumerate(self.image_list):
            image.resize(size)
            image.redraw(index)
