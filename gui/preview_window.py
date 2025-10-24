#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finestra di anteprima per posizionamento manuale del logo
"""

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk

from config import PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT, CLICK_DELAY
from utils.image_processor import ImageProcessor


class PreviewWindow:
    """Classe per gestire la finestra di anteprima"""
    
    def __init__(self, parent, img, logo, filename, current_idx, total_images, 
                 logo_size_percent, position_callback, close_callback):
        """
        Inizializza finestra di anteprima
        
        Args:
            parent: Finestra padre
            img: Immagine PIL da mostrare
            logo: Logo PIL (con sfondo se applicato)
            filename: Nome file immagine
            current_idx: Indice immagine corrente
            total_images: Totale immagini
            logo_size_percent: Percentuale dimensione logo
            position_callback: Callback quando posizione selezionata
            close_callback: Callback quando finestra chiusa
        """
        self.parent = parent
        self.original_img = img
        self.original_logo = logo
        self.logo_size_percent = logo_size_percent
        self.position_callback = position_callback
        self.close_callback = close_callback
        self.window_closed_manually = False
        self.click_position = None
        
        # Crea finestra
        self.window = tk.Toplevel(parent)
        self.window.title(f"Posiziona il logo - {filename}")
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Frame principale
        main_frame = ttk.Frame(self.window, padding=10)
        main_frame.pack(fill="both", expand=True)
        
        # Progress bar
        self._build_progress_bar(main_frame, current_idx, total_images)
        
        # Prepara immagine e logo per anteprima
        self._prepare_preview_images()
        
        # Canvas
        self.canvas = tk.Canvas(
            main_frame, 
            width=self.preview_image.width,
            height=self.preview_image.height, 
            bg="gray80"
        )
        self.canvas.pack(pady=5)
        self.canvas.create_image(0, 0, anchor="nw", image=self.preview_photo)
        
        # Bind eventi
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_canvas_hover)
        
        # Centra finestra
        self._center_window()
    
    def _build_progress_bar(self, parent, current_idx, total_images):
        """Costruisce barra di progresso"""
        progress_frame = ttk.Frame(parent)
        progress_frame.pack(fill="x", pady=5)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress.pack()
        self.progress['maximum'] = total_images
        self.progress['value'] = current_idx
        
        percentage = int((current_idx / total_images) * 100)
        self.progress_label = ttk.Label(
            progress_frame,
            text=f"Progresso: {percentage}% ({current_idx}/{total_images})"
        )
        self.progress_label.pack(pady=2)
    
    def _prepare_preview_images(self):
        """Prepara immagine e logo per anteprima"""
        # Ridimensiona immagine per anteprima
        display_img = self.original_img.copy()
        display_img.thumbnail((PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT))
        self.preview_image = display_img
        self.preview_photo = ImageTk.PhotoImage(display_img)
        
        # Ridimensiona logo per anteprima
        processor = ImageProcessor()
        logo_resized_orig = processor.resize_logo(
            self.original_logo,
            self.original_img,
            self.logo_size_percent
        )
        
        # Scala logo proporzionalmente all'anteprima
        scale_factor = display_img.width / self.original_img.width
        logo_width_preview = int(logo_resized_orig.width * scale_factor)
        logo_height_preview = int(logo_resized_orig.height * scale_factor)
        
        self.preview_logo = logo_resized_orig.resize(
            (logo_width_preview, logo_height_preview),
            Image.Resampling.LANCZOS
        )
        self.preview_logo_photo = ImageTk.PhotoImage(self.preview_logo)
    
    def _center_window(self):
        """Centra la finestra sullo schermo"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (self.window.winfo_width() // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.window.winfo_height() // 2)
        self.window.geometry(f"+{x}+{y}")
    
    def on_canvas_hover(self, event):
        """Mostra anteprima logo mentre mouse si muove"""
        if self.preview_logo is None:
            return
        
        # Calcola posizione logo centrata sul cursore
        x = event.x - self.preview_logo.width // 2
        y = event.y - self.preview_logo.height // 2
        
        # Limita ai bordi
        x = max(0, min(x, self.preview_image.width - self.preview_logo.width))
        y = max(0, min(y, self.preview_image.height - self.preview_logo.height))
        
        # Ridisegna
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.preview_photo)
        self.canvas.create_image(
            x + self.preview_logo.width // 2,
            y + self.preview_logo.height // 2,
            image=self.preview_logo_photo,
            tags="hover_logo"
        )
    
    def on_canvas_click(self, event):
        """Gestisce click sul canvas"""
        if self.preview_image is None:
            return
        
        # Calcola posizione relativa (0-1)
        rel_x = event.x / self.preview_image.width
        rel_y = event.y / self.preview_image.height
        
        # Limita ai bordi considerando dimensione logo
        logo_half_width_rel = (self.preview_logo.width / 2) / self.preview_image.width
        logo_half_height_rel = (self.preview_logo.height / 2) / self.preview_image.height
        
        rel_x = max(logo_half_width_rel, min(rel_x, 1 - logo_half_width_rel))
        rel_y = max(logo_half_height_rel, min(rel_y, 1 - logo_half_height_rel))
        
        self.click_position = (rel_x, rel_y)
        
        # Ridisegna con logo finale
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.preview_photo)
        
        x = int(rel_x * self.preview_image.width) - self.preview_logo.width // 2
        y = int(rel_y * self.preview_image.height) - self.preview_logo.height // 2
        self.canvas.create_image(
            x + self.preview_logo.width // 2,
            y + self.preview_logo.height // 2,
            image=self.preview_logo_photo,
            tags="final_logo"
        )
        
        # Chiama callback dopo delay
        self.window.after(CLICK_DELAY, self._on_position_confirmed)
    
    def _on_position_confirmed(self):
        """Conferma posizione e chiudi finestra"""
        if not self.window_closed_manually:
            self.window.destroy()
            self.position_callback(self.click_position)
    
    def on_window_close(self):
        """Gestisce chiusura finestra"""
        self.window_closed_manually = True
        self.window.destroy()
        
        response = messagebox.askyesno(
            "Finestra chiusa",
            "Hai chiuso la finestra senza selezionare una posizione.\n\n"
            "Vuoi passare all'immagine successiva?\n\n"
            "Sì = Continua\nNo = Termina ed elabora"
        )
        
        self.close_callback(response)