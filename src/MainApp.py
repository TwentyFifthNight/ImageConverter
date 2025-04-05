import os
import re
import shutil
import tkinter.filedialog
from tkinter import filedialog
from typing import Tuple

import customtkinter as cttk
from CustomTkinterMessagebox import CTkMessagebox

from src.converter import start_conversion
from src.definitions import APP_WIDTH, APP_HEIGHT, MAX_OUTPUT_SIZE, MIN_OUTPUT_SIZE, TEMP_IMAGE_PATH
from view import *
from view.fonts.fonts import *

cttk.set_appearance_mode("Dark")


class App(cttk.CTk):
    DEFAULT_GRAY = ("gray50", "gray30")
    OUTPUT_SIZE_NAME = "Output Width", "Output Height"

    def __init__(self):
        super().__init__()

        self.output_size = (cttk.StringVar(name=self.OUTPUT_SIZE_NAME[0], value=str(MAX_OUTPUT_SIZE[0])),
                            cttk.StringVar(name=self.OUTPUT_SIZE_NAME[1], value=str(MAX_OUTPUT_SIZE[1])))
        self.output_size[0].trace_add("write", self._on_size_change)
        self.output_size[1].trace_add("write", self._on_size_change)

        self.build_ui()

        files = os.listdir(TEMP_IMAGE_PATH)
        for file in files:
            print(file)
            file_path = os.path.join(TEMP_IMAGE_PATH, file)
            if file_path.endswith((".png", ".jpg", ".jpeg", ".bmp")):
                self.image_list_view.add_image(file_path)

    def build_ui(self):
        self.title("Image To Header File Converter")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = cttk.CTkFrame(
            master=self,
            corner_radius=0,
        )
        self.frame_left.grid(row=0, column=0, sticky=cttk.NSEW)

        self.frame_right = cttk.CTkFrame(master=self)
        self.frame_right.grid_rowconfigure(1)
        self.frame_right.grid(row=0, column=1, sticky=cttk.NSEW, padx=20, pady=20)

        # Right-Side Image List
        self.image_list_view = ImageListView(parent=self.frame_right)
        self.image_list_view.IMAGE_SIZE = MAX_OUTPUT_SIZE
        self.image_list_view.pack(
            in_=self.frame_right,
            side=cttk.TOP,
            fill=cttk.BOTH,
            expand=True,
            padx=0,
            pady=0,
        )

        # Left-Side
        self.frame_left.grid_columnconfigure(1, weight=0)
        self.frame_left.grid_rowconfigure(7, weight=0)

        self.label_1 = cttk.CTkLabel(master=self.frame_left, text="Actions", font=heading_font())
        self.label_1.grid(row=0, column=0, sticky=cttk.NSEW, padx=10, pady=10)

        self.select_image_button = cttk.CTkButton(
            master=self.frame_left,
            fg_color="#008CBA",
            hover_color=self.DEFAULT_GRAY,
            text="Select",
            font=button_med_font(),
            command=self.__on_select_image,
        )
        self.select_image_button.grid(row=1, column=0, pady=(5, 10), padx=5)

        self.remove_all_button = cttk.CTkButton(
            master=self.frame_left,
            fg_color="#f44336",
            hover_color=self.DEFAULT_GRAY,
            text="Remove all",
            font=button_med_font(),
            command=self.__on_remove_all_images,
        )
        self.remove_all_button.grid(row=2, column=0, pady=(5, 10), padx=5)

        self.convert_button = cttk.CTkButton(
            master=self.frame_left,
            fg_color="#04AA6D",
            hover_color=self.DEFAULT_GRAY,
            text="Convert",
            font=button_med_font(),
            command=self.__on_convert,
        )
        self.convert_button.grid(row=3, column=0, pady=(5, 10), padx=5)

        self.width_label = cttk.CTkLabel(master=self.frame_left, text="Width", font=body_med_font())
        self.width_label.grid(row=4, column=0, sticky=cttk.NSEW, padx=10, pady=0)
        self.width_entry = cttk.CTkEntry(
            master=self.frame_left,
            placeholder_text_color="darkblue",
            fg_color="#008CBA",
            state="normal",
            textvariable=self.output_size[0]
        )
        self.width_entry.grid(row=5, column=0, pady=(5, 10), padx=5)

        self.height_label = cttk.CTkLabel(master=self.frame_left, text="Height", font=body_med_font())
        self.height_label.grid(row=6, column=0, sticky=cttk.NSEW, padx=10, pady=0)
        self.height_entry = cttk.CTkEntry(
            master=self.frame_left,
            placeholder_text_color="darkblue",
            fg_color="#008CBA",
            state="normal",
            textvariable=self.output_size[1],
        )
        self.height_entry.grid(row=7, column=0, pady=(5, 10), padx=5)

    @staticmethod
    def _clean_int_str(string: str):
        value = re.sub(r'\D', '', string)
        value = value.lstrip('0')

        return value

    def _on_size_change(self, name, index, operation):
        if name == self.OUTPUT_SIZE_NAME[0]:
            value = self.output_size[0].get()
            new_value = self._clean_int_str(value)
            if value != new_value:
                self.output_size[0].set(new_value)
        elif name == self.OUTPUT_SIZE_NAME[1]:
            value = self.output_size[1].get()
            new_value = self._clean_int_str(value)
            if value != new_value:
                self.output_size[1].set(new_value)

        size = (self.output_size[0].get(), self.output_size[1].get())
        if self._validate_image_output_size(size)[0]:
            size = (int(size[0]), int(size[1]))

            self.__verify_image_paths()
            self.image_list_view.resize_list(size)

    def _validate_image_output_size(self, size: (str, str)) -> Tuple[bool, list[str]]:
        if len(size[0]) == 0:
            size = (-1, size[1])
        if len(size[1]) == 0:
            size = (size[0], -1)

        size = int(size[0]), int(size[1])

        invalid_data_list = []
        is_valid = True
        for index in range(2):
            result = self._validate_size_range(size[index], self.OUTPUT_SIZE_NAME[index])
            is_valid = is_valid and result[0]
            invalid_data_list.append(result[1])

        return is_valid, invalid_data_list

    def _validate_size_range(self, value: int, name: str) -> Tuple[bool, str]:
        result = True
        invalid_data_message = ""

        min_value = MIN_OUTPUT_SIZE[0] if name == self.OUTPUT_SIZE_NAME[0] else MIN_OUTPUT_SIZE[1]
        if value < min_value:
            result = False
            invalid_data_message = f"{name} must be at least {min_value}."

        max_value = MAX_OUTPUT_SIZE[0] if name == self.OUTPUT_SIZE_NAME[0] else MAX_OUTPUT_SIZE[1]
        if value > max_value:
            result = False
            invalid_data_message = f"{name} must be at most {max_value}."

        return result, invalid_data_message

    def __on_select_image(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", (".png", ".jpg", ".jpeg", ".bmp"))])
        for file_path in file_paths:
            file_copy_path = shutil.copy(file_path, TEMP_IMAGE_PATH)
            self.image_list_view.add_image(file_copy_path)

    def __on_remove_all_images(self):
        self.image_list_view.remove_all()
        files = os.listdir(TEMP_IMAGE_PATH)
        for file in files:
            file_path = os.path.join(TEMP_IMAGE_PATH, file)
            self.__remove_temp_file(file_path)

    def __remove_temp_file(self, path):
        try:
            if os.path.isfile(path):
                os.remove(path)
        except OSError:
            print("Error occurred while deleting files.")

    def __on_convert(self):
        size = self.output_size[0].get(), self.output_size[1].get()
        result = self._validate_image_output_size(size)
        if not result[0]:
            box_message = ""
            for index, message in enumerate(result[1]):
                box_message += message
                if index + 1 < len(result[1]):
                    box_message += "\n"
            CTkMessagebox.messagebox('Invalid Data', box_message, sound="off")
            return

        size = int(size[0]), int(size[1])

        image_path_list = self.image_list_view.get_image_path_list()
        if len(image_path_list) < 1:
            CTkMessagebox.messagebox('Invalid Data', 'Add one or more images before starting the conversion',
                                     sound="off", size="400x150")
            return

        output_path = tkinter.filedialog.asksaveasfilename(defaultextension=".h", initialfile="output")
        if not output_path.endswith(".h"):
            CTkMessagebox.messagebox('Invalid Data', 'File extension has to be .h', sound="off")
            return

        if not self.__verify_image_paths(image_path_list):
            CTkMessagebox.messagebox('Invalid Data', 'One or more input files no longer exist', sound="off")
            return

        progress_view = ProgressView(self.frame_right, self.__on_conversion_completed)
        progress_view.pack(
            in_=self.frame_right,
            side=cttk.BOTTOM,
            fill=cttk.BOTH,
            expand=True,
            padx=0,
            pady=0,
        )
        start_conversion(image_path_list, output_path, size, progress_view.update_progress)

    def __verify_image_paths(self, image_path_list: list[str] = None) -> bool:
        if image_path_list is None:
            image_path_list = self.image_list_view.get_image_path_list()

        all_files_exist = True
        for path in image_path_list:
            if not os.path.exists(path):
                all_files_exist = False
                self.image_list_view.remove_image_by_path(path)

        return all_files_exist

    def __on_conversion_completed(self, view: ProgressView, success: bool):
        view.destroy()
        CTkMessagebox.messagebox('Invalid Data', 'File extension has to be .h', sound="off")

    # ============ Misc Handlers ============
    def on_closing(self, event=0):
        self.image_list_view.remove_all()
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
