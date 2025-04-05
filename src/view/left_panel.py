from typing import Tuple, Callable

import customtkinter as cttk

from src.view.fonts.fonts import heading_font, button_med_font, body_med_font


class LeftPanel(cttk.CTkFrame):
    DEFAULT_GRAY = ("gray50", "gray30")

    def __init__(self, parent, output_size: Tuple[cttk.StringVar, cttk.StringVar], on_select_image: Callable[[], None],
                 on_remove_all_images: Callable[[], None], on_convert: Callable[[], None]):
        super().__init__(parent)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(7, weight=0)

        self.build_ui(output_size, on_select_image, on_remove_all_images, on_convert)

    def build_ui(self, output_size: Tuple[cttk.StringVar, cttk.StringVar], on_select_image=None,
                 on_remove_all_images=None, on_convert=None):
        self.label_1 = cttk.CTkLabel(master=self, text="Actions", font=heading_font())
        self.label_1.grid(row=0, column=0, sticky=cttk.NSEW, padx=10, pady=10)

        self.select_image_button = cttk.CTkButton(
            master=self,
            fg_color="#008CBA",
            hover_color=self.DEFAULT_GRAY,
            text="Select",
            font=button_med_font(),
            command=on_select_image,
        )
        self.select_image_button.grid(row=1, column=0, pady=(5, 10), padx=5)

        self.remove_all_button = cttk.CTkButton(
            master=self,
            fg_color="#f44336",
            hover_color=self.DEFAULT_GRAY,
            text="Remove all",
            font=button_med_font(),
            command=on_remove_all_images,
        )
        self.remove_all_button.grid(row=2, column=0, pady=(5, 10), padx=5)

        self.convert_button = cttk.CTkButton(
            master=self,
            fg_color="#04AA6D",
            hover_color=self.DEFAULT_GRAY,
            text="Convert",
            font=button_med_font(),
            command=on_convert,
        )
        self.convert_button.grid(row=3, column=0, pady=(5, 10), padx=5)

        self.width_label = cttk.CTkLabel(master=self, text="Width", font=body_med_font())
        self.width_label.grid(row=4, column=0, sticky=cttk.NSEW, padx=10, pady=0)
        self.width_entry = cttk.CTkEntry(
            master=self,
            placeholder_text_color="darkblue",
            fg_color="#008CBA",
            state="normal",
            textvariable=output_size[0]
        )
        self.width_entry.grid(row=5, column=0, pady=(5, 10), padx=5)

        self.height_label = cttk.CTkLabel(master=self, text="Height", font=body_med_font())
        self.height_label.grid(row=6, column=0, sticky=cttk.NSEW, padx=10, pady=0)
        self.height_entry = cttk.CTkEntry(
            master=self,
            placeholder_text_color="darkblue",
            fg_color="#008CBA",
            state="normal",
            textvariable=output_size[1],
        )
        self.height_entry.grid(row=7, column=0, pady=(5, 10), padx=5)