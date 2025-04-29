from typing import Tuple, Callable

import customtkinter as cttk
from PIL import Image

from src.view.fonts.fonts import button_med_font


class ImageView(cttk.CTkFrame):

    def __init__(self, parent, path: str, index: int, on_swap_image: Callable[[cttk.CTkFrame], None],
                 on_remove_image: Callable[[str], None], size: Tuple[int, int] = (200, 200)):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.file_path = path

        self.swap_button = cttk.CTkButton(self, text="⇕", font=button_med_font(), width=20, command=lambda s=self: on_swap_image(s))
        if index > 0:
            self.swap_button.grid(row=0, column=0)

        remove_button = cttk.CTkButton(self, text="✖", font=button_med_font(), width=20, fg_color="#f44336", command=lambda p=path: on_remove_image(p))
        remove_button.grid(row=1, column=1)

        image = cttk.CTkImage(Image.open(path), size=size)
        self.label_logo = cttk.CTkLabel(self, image=image, text="")
        self.label_logo.grid(row=1, column=0, sticky=cttk.NSEW, padx=15, pady=15)

    def redraw(self, index: int):
        if index > 0:
            self.swap_button.grid(row=0, column=0)
        else:
            self.swap_button.grid_forget()

    def resize(self, size: Tuple[int, int]):
        self.label_logo.destroy()
        image = cttk.CTkImage(Image.open(self.file_path), size=size)
        self.label_logo = cttk.CTkLabel(self, image=image, text="")
        self.label_logo.grid(row=1, column=0, sticky=cttk.NSEW, padx=15, pady=15)
