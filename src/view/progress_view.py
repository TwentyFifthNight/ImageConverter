import customtkinter as cttk

from src.view.fonts.fonts import small_font


class ProgressView(cttk.CTkFrame):
    def __init__(self, parent, on_progress_full):
        super().__init__(parent)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.lbl_progress = cttk.CTkLabel(master=self, text="Progress: 0%", font=small_font(),
                                          justify=cttk.CENTER)
        self.lbl_progress.grid(row=0, column=0, sticky=cttk.EW, pady=(15, 0))

        self.progressbar = cttk.CTkProgressBar(master=self)
        self.progressbar.set(1)
        self.progressbar.grid(row=1, column=0, sticky=cttk.EW, padx=15, pady=(0, 15))

        self.on_progress_full = on_progress_full

    def update_progress(self, progress: float):
        self.progressbar.set(progress)
        self.lbl_progress.configure(text=f"Progress: {progress * 100:.0f}%")
        if progress == 1:
            self.on_progress_full(self)
