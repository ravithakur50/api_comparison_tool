import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from src.bert_processor import BertProcessor
from src.utils import load_api_spec, update_footer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class APIGui:
    def __init__(self):
        self.scaling_factor = 1.2
        self.app = ctk.CTk()
        self.app.title("API Comparison Tool")
        self.app.minsize(width=int(600 * self.scaling_factor), height=int(510 * self.scaling_factor))

        # Initialize BERT processor
        self.bert_processor = BertProcessor('bert-base-uncased')

        # Global paths
        self.api_spec1_path = ""
        self.api_spec2_path = ""

        # Setup GUI
        self._setup_gui()

    def _setup_gui(self):
        main_frame = ctk.CTkFrame(self.app)
        main_frame.pack(pady=int(10 * self.scaling_factor), padx=int(20 * self.scaling_factor), fill='both', expand=True)

        # Logo
        logo_image = Image.open('assets/hsbc_logo.png').resize(
            (int(50 * self.scaling_factor), int(25 * self.scaling_factor)), Image.LANCZOS
        )
        self.logo = ImageTk.PhotoImage(logo_image)
        ctk.CTkLabel(main_frame, image=self.logo, text="").grid(row=0, column=2, sticky='ne', pady=int(10 * self.scaling_factor))

        # API spec labels
        self.api_spec1_label = ctk.CTkLabel(main_frame, text="API Specification 1: None selected")
        self.api_spec1_label.grid(row=1, column=0, padx=(int(30 * self.scaling_factor), int(10 * self.scaling_factor)), pady=int(10 * self.scaling_factor))
        self.api_spec2_label = ctk.CTkLabel(main_frame, text="API Specification 2: None selected")
        self.api_spec2_label.grid(row=3, column=0, padx=(int(30 * self.scaling_factor), int(10 * self.scaling_factor)), pady=int(10 * self.scaling_factor))

        # Textboxes
        self.api_spec1_text = ctk.CTkTextbox(main_frame, width=int(400 * self.scaling_factor), height=int(200 * self.scaling_factor), state=tk.DISABLED)
        self.api_spec1_text.grid(row=2, column=0, padx=(int(110 * self.scaling_factor), int(10 * self.scaling_factor)), pady=int(10 * self.scaling_factor), sticky="nsew")
        self.api_spec2_text = ctk.CTkTextbox(main_frame, width=int(400 * self.scaling_factor), height=int(200 * self.scaling_factor), state=tk.DISABLED)
        self.api_spec2_text.grid(row=4, column=0, padx=(int(110 * self.scaling_factor), int(10 * self.scaling_factor)), pady=int(10 * self.scaling_factor), sticky="nsew")

        # Buttons
        ctk.CTkButton(main_frame, text="API Spec 1", command=self.select_api_spec1).grid(row=2, column=1, padx=(int(10 * self.scaling_factor), 0))
        ctk.CTkButton(main_frame, text="API Spec 2", command=self.select_api_spec2).grid(row=4, column=1, padx=(int(10 * self.scaling_factor), 0))
        self.compare_button = ctk.CTkButton(main_frame, text="Compare APIs", command=self.compare_apis, state=tk.DISABLED)
        self.compare_button.grid(row=5, column=0, padx=(int(100 * self.scaling_factor), 0))

        # Dropdown for model selection
        self.model_options = ["bert-base-uncased", "bert-base-cased", "bert-large-uncased", "bert-large-cased"]
        self.selected_model = tk.StringVar(value=self.model_options[0])
        ctk.CTkOptionMenu(main_frame, variable=self.selected_model, values=self.model_options).grid(row=5, column=0, padx=(int(10 * self.scaling_factor), 0), sticky='w')

        # Animation label
        self.animation_label = ctk.CTkLabel(main_frame, text="")
        self.animation_label.grid(row=0, column=0, padx=int(10 * self.scaling_factor), pady=int(10 * self.scaling_factor), sticky='w')

        # Similarity and output text
        self.similarity_text = ctk.CTkTextbox(main_frame, width=int(400 * self.scaling_factor), height=int(100 * self.scaling_factor), state=tk.DISABLED)
        self.similarity_text.grid(row=8, column=0, columnspan=3, pady=int(10 * self.scaling_factor), sticky="nsew")
        self.output_text = ctk.CTkTextbox(self.app, width=int(215 * self.scaling_factor), height=int(25 * self.scaling_factor), state=tk.DISABLED)
        self.output_text.pack(side="bottom", fill="x", padx=(int(30 * self.scaling_factor), int(50 * self.scaling_factor)), pady=int(10 * self.scaling_factor))

    def select_api_spec1(self):
        self.api_spec1_path = filedialog.askopenfilename(title="API Spec 1")
        if self.api_spec1_path:
            self.api_spec1_label.configure(text=f"API Spec 1: {os.path.basename(self.api_spec1_path)}")
            content = load_api_spec(self.api_spec1_path)
            self.api_spec1_text.configure(state=tk.NORMAL)
            self.api_spec1_text.delete('1.0', tk.END)
            self.api_spec1_text.insert(tk.END, content)
            self.api_spec1_text.configure(state=tk.DISABLED)
            self._check_enable_compare_button()

    def select_api_spec2(self):
        self.api_spec2_path = filedialog.askopenfilename(title="API Spec 2")
        if self.api_spec2_path:
            self.api_spec2_label.configure(text=f"API Spec 2: {os.path.basename(self.api_spec2_path)}")
            content = load_api_spec(self.api_spec2_path)
            self.api_spec2_text.configure(state=tk.NORMAL)
            self.api_spec2_text.delete('1.0', tk.END)
            self.api_spec2_text.insert(tk.END, content)
            self.api_spec2_text.configure(state=tk.DISABLED)
            self._check_enable_compare_button()

    def _check_enable_compare_button(self):
        if self.api_spec1_path and self.api_spec2_path:
            self.compare_button.configure(state=tk.NORMAL)
        else:
            self.compare_button.configure(state=tk.DISABLED)

    def compare_apis(self):
        self.bert_processor.set_model(self.selected_model.get())
        spec1 = load_api_spec(self.api_spec1_path)
        spec2 = load_api_spec(self.api_spec2_path)
        similarity = self.bert_processor.compare_specs(spec1, spec2)
        self.similarity_text.configure(state=tk.NORMAL)
        self.similarity_text.delete('1.0', tk.END)
        self.similarity_text.insert(tk.END, f"Similarity score: {similarity:.4f}")
        self.similarity_text.configure(state=tk.DISABLED)
        update_footer(self.output_text, distinct_api_count=2)

    def run(self):
        self.app.mainloop()