#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finestra principale dell'applicazione
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

from config import *
from utils.settings_manager import SettingsManager
from utils.image_processor import ImageProcessor
from gui.preview_window import PreviewWindow


class LogoApplierApp:
    """Classe principale dell'applicazione"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(True, False)
        
        # Variabili GUI
        self.source_folder = tk.StringVar()
        self.logo_file = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.position_mode = tk.StringVar(value="manual")
        self.fixed_position = tk.StringVar(value="top_left")
        self.logo_size_percent = tk.IntVar(value=10)
        self.margin_percent = tk.IntVar(value=2)
        
        # Variabili per sfondo logo
        self.bg_color = tk.StringVar(value='Nessuno')
        self.bg_shape = tk.StringVar(value='Rettangolare')
        
        # Variabili per modalità manuale
        self.current_image_index = 0
        self.image_files = []
        self.manual_positions = {}
        self.preview_window_obj = None
        
        # Processore immagini
        self.processor = ImageProcessor()
        
        # Carica impostazioni salvate
        self.load_settings()
        
        # Costruisci GUI
        self.build_gui()
        
    def build_gui(self):
        """Costruisce l'interfaccia grafica"""
        # Frame selezione file
        self._build_selection_frame()
        
        # Frame impostazioni logo
        self._build_settings_frame()
        
        # Frame impostazioni sfondo logo
        self._build_background_frame()
        
        # Frame modalità posizionamento
        self._build_positioning_frame()
        
        # Progress bar
        self._build_progress_frame()
        
        # Pulsante avvia
        self.start_button = ttk.Button(
            self.root, 
            text="Avvia Elaborazione", 
            command=self.start_processing
        )
        self.start_button.pack(pady=10)
        
        # Menu bar
        self._build_menu_bar()
        
        self.update_mode()
    
    def _build_selection_frame(self):
        """Costruisce frame selezione file"""
        frame = ttk.LabelFrame(self.root, text="Selezione File e Cartelle", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        frame.columnconfigure(1, weight=1)
        
        # Cartella sorgente
        ttk.Label(frame, text="Cartella immagini:").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.source_folder).grid(row=0, column=1, sticky="ew", padx=5, pady=3)
        ttk.Button(frame, text="Sfoglia", command=self.select_source_folder).grid(row=0, column=2, pady=3)
        
        # File logo
        ttk.Label(frame, text="File logo:").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.logo_file).grid(row=1, column=1, sticky="ew", padx=5, pady=3)
        ttk.Button(frame, text="Sfoglia", command=self.select_logo_file).grid(row=1, column=2, pady=3)
        
        # Cartella destinazione
        ttk.Label(frame, text="Cartella destinazione:").grid(row=2, column=0, sticky="w", pady=3)
        ttk.Entry(frame, textvariable=self.dest_folder).grid(row=2, column=1, sticky="ew", padx=5, pady=3)
        ttk.Button(frame, text="Sfoglia", command=self.select_dest_folder).grid(row=2, column=2, pady=3)
    
    def _build_settings_frame(self):
        """Costruisce frame impostazioni logo"""
        frame = ttk.LabelFrame(self.root, text="Impostazioni Logo", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        # Dimensione logo
        size_frame = ttk.Frame(frame)
        size_frame.pack(fill="x", pady=5)
        ttk.Label(size_frame, text="Dimensione logo - (%) rispetto all'immagine:").pack(side="left", padx=5)
        for size in LOGO_SIZE_OPTIONS:
            ttk.Radiobutton(
                size_frame, 
                text=f"{size}%", 
                variable=self.logo_size_percent, 
                value=size
            ).pack(side="left", padx=5)
        
        # Margine
        margin_frame = ttk.Frame(frame)
        margin_frame.pack(fill="x", pady=5)
        ttk.Label(margin_frame, text="Margine dai bordi (%) - solo modalità automatica:").pack(side="left", padx=5)
        for margin in MARGIN_OPTIONS:
            ttk.Radiobutton(
                margin_frame, 
                text=f"{margin}%", 
                variable=self.margin_percent, 
                value=margin
            ).pack(side="left", padx=5)
    
    def _build_background_frame(self):
        """Costruisce frame impostazioni sfondo logo"""
        frame = ttk.LabelFrame(self.root, text="Sfondo Logo", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        # Colore sfondo
        color_frame = ttk.Frame(frame)
        color_frame.pack(fill="x", pady=5)
        ttk.Label(color_frame, text="Colore sfondo:").pack(side="left", padx=5)
        
        color_combo = ttk.Combobox(
            color_frame, 
            textvariable=self.bg_color, 
            values=list(BACKGROUND_COLORS.keys()),
            state="readonly",
            width=15
        )
        color_combo.pack(side="left", padx=5)
        
        # Forma sfondo
        ttk.Label(color_frame, text="Forma:").pack(side="left", padx=(20, 5))
        
        for shape in BACKGROUND_SHAPES:
            ttk.Radiobutton(
                color_frame, 
                text=shape, 
                variable=self.bg_shape, 
                value=shape
            ).pack(side="left", padx=5)
    
    def _build_positioning_frame(self):
        """Costruisce frame modalità posizionamento"""
        frame = ttk.LabelFrame(self.root, text="Modalità Posizionamento", padding=10)
        frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Radiobutton(
            frame, 
            text="Posizionamento manuale (clicca su ogni immagine)", 
            variable=self.position_mode, 
            value="manual",
            command=self.update_mode
        ).grid(row=0, column=0, sticky="w", pady=3)
        
        ttk.Radiobutton(
            frame, 
            text="Posizione fissa per tutte le immagini:", 
            variable=self.position_mode, 
            value="fixed",
            command=self.update_mode
        ).grid(row=1, column=0, sticky="w", pady=3)
        
        # Frame per posizioni fisse
        self.fixed_pos_frame = ttk.Frame(frame)
        self.fixed_pos_frame.grid(row=2, column=0, sticky="w", padx=20)
        
        self.rb_top_left = ttk.Radiobutton(
            self.fixed_pos_frame, 
            text="Alto sinistra", 
            variable=self.fixed_position, 
            value="top_left"
        )
        self.rb_top_left.grid(row=0, column=0, sticky="w")
        
        self.rb_top_right = ttk.Radiobutton(
            self.fixed_pos_frame, 
            text="Alto destra", 
            variable=self.fixed_position, 
            value="top_right"
        )
        self.rb_top_right.grid(row=0, column=1, sticky="w", padx=10)
        
        self.rb_bottom_left = ttk.Radiobutton(
            self.fixed_pos_frame, 
            text="Basso sinistra", 
            variable=self.fixed_position, 
            value="bottom_left"
        )
        self.rb_bottom_left.grid(row=1, column=0, sticky="w")
        
        self.rb_bottom_right = ttk.Radiobutton(
            self.fixed_pos_frame, 
            text="Basso destra", 
            variable=self.fixed_position, 
            value="bottom_right"
        )
        self.rb_bottom_right.grid(row=1, column=1, sticky="w", padx=10)
    
    def _build_progress_frame(self):
        """Costruisce frame barra di progresso"""
        frame = ttk.Frame(self.root)
        frame.pack(fill="x", padx=10, pady=10)
        
        self.progress = ttk.Progressbar(frame, mode='determinate')
        self.progress.pack(fill="x")
        
        self.progress_label = ttk.Label(frame, text="")
        self.progress_label.pack(pady=5)
    
    def _build_menu_bar(self):
        """Costruisce barra menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label="Informazioni", command=self.show_about)
    
    def show_about(self):
        """Mostra finestra informazioni"""
        about_text = f"""{APP_NAME}
Versione {APP_VERSION}

Sviluppato da: {AUTHOR}
Email: {EMAIL}
LinkedIn: {LINKEDIN}
GitHub: {GITHUB}

© 2025 {AUTHOR}. Tutti i diritti riservati.
Rilasciato sotto licenza {LICENSE}.

Applicazione per applicare automaticamente o manualmente
un logo su immagini con supporto per sfondi personalizzati."""
        
        messagebox.showinfo("Informazioni", about_text)
    
    # Metodi di selezione file
    def select_source_folder(self):
        folder = filedialog.askdirectory(title="Seleziona cartella immagini")
        if folder:
            self.source_folder.set(folder)
    
    def select_logo_file(self):
        file = filedialog.askopenfilename(
            title="Seleziona file logo",
            filetypes=[("Immagini", "*.png *.jpg *.jpeg"), ("Tutti i file", "*.*")]
        )
        if file:
            self.logo_file.set(file)
    
    def select_dest_folder(self):
        folder = filedialog.askdirectory(title="Seleziona cartella destinazione")
        if folder:
            self.dest_folder.set(folder)
    
    def update_mode(self):
        """Aggiorna stato radiobutton in base alla modalità"""
        state = "normal" if self.position_mode.get() == "fixed" else "disabled"
        self.rb_top_left.config(state=state)
        self.rb_top_right.config(state=state)
        self.rb_bottom_left.config(state=state)
        self.rb_bottom_right.config(state=state)# Continua classe LogoApplierApp...
    
    def validate_inputs(self):
        """Valida gli input dell'utente"""
        if not self.source_folder.get():
            messagebox.showerror("Errore", "Seleziona la cartella delle immagini")
            return False
        if not self.logo_file.get():
            messagebox.showerror("Errore", "Seleziona il file del logo")
            return False
        if not self.dest_folder.get():
            messagebox.showerror("Errore", "Seleziona la cartella di destinazione")
            return False
        if not os.path.exists(self.source_folder.get()):
            messagebox.showerror("Errore", "La cartella sorgente non esiste")
            return False
        if not os.path.exists(self.logo_file.get()):
            messagebox.showerror("Errore", "Il file logo non esiste")
            return False
        return True
    
    def start_processing(self):
        """Avvia l'elaborazione delle immagini"""
        if not self.validate_inputs():
            return
        
        # Crea cartella destinazione se non esiste
        os.makedirs(self.dest_folder.get(), exist_ok=True)
        
        # Ottieni lista immagini
        self.image_files = self.processor.get_image_files(
            self.source_folder.get(), 
            tuple(SUPPORTED_IMAGE_FORMATS)
        )
        
        if not self.image_files:
            messagebox.showwarning("Attenzione", "Nessuna immagine trovata")
            return
        
        self.manual_positions = {}
        self.current_image_index = 0
        
        # Inizializza progress bar
        self.progress['value'] = 0
        self.progress['maximum'] = len(self.image_files)
        
        if self.position_mode.get() == "manual":
            self.show_next_image_for_positioning()
        else:
            self.process_all_images()
    
    def show_next_image_for_positioning(self):
        """Mostra prossima immagine per posizionamento manuale"""
        if self.current_image_index >= len(self.image_files):
            self.process_all_images()
            return
        
        img_path = self.image_files[self.current_image_index]
        
        # Aggiorna progress bar
        self.progress['value'] = self.current_image_index
        percentage = int(self.current_image_index / len(self.image_files) * 100)
        self.progress_label.config(
            text=f"Posizionamento: {percentage}% ({self.current_image_index}/{len(self.image_files)})"
        )
        self.root.update()
        
        try:
            img = Image.open(img_path)
            filename = os.path.basename(img_path)
            
            # Carica logo con sfondo
            logo = self._load_logo_with_background()
            
            # Crea finestra preview
            self.preview_window_obj = PreviewWindow(
                self.root,
                img,
                logo,
                filename,
                self.current_image_index,
                len(self.image_files),
                self.logo_size_percent.get(),
                self.on_position_selected,
                self.on_preview_closed
            )
            
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare:\n{str(e)}")
            self.current_image_index += 1
            self.show_next_image_for_positioning()
    
    def _load_logo_with_background(self):
        """Carica il logo e applica sfondo se necessario"""
        logo = Image.open(self.logo_file.get())
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        # Applica sfondo se selezionato
        bg_color_value = BACKGROUND_COLORS.get(self.bg_color.get())
        if bg_color_value:
            logo = self.processor.create_logo_with_background(
                logo,
                bg_color_value,
                self.bg_shape.get(),
                padding=15
            )
        
        return logo

    
    def on_position_selected(self, position):
        """Callback quando posizione è selezionata"""
        img_path = self.image_files[self.current_image_index]
        self.manual_positions[img_path] = position
        self.current_image_index += 1
        self.show_next_image_for_positioning()
    
    def on_preview_closed(self, skip_to_next):
        """Callback quando finestra preview è chiusa"""
        if skip_to_next:
            self.current_image_index += 1
            self.show_next_image_for_positioning()
        else:
            self.progress_label.config(text="Elaborazione in corso...")
            self.process_positioned_images()
    
    def process_positioned_images(self):
        """Elabora solo le immagini posizionate manualmente"""
        if not self.manual_positions:
            messagebox.showinfo("Nessuna immagine", "Nessuna immagine è stata posizionata.")
            self.progress_label.config(text="")
            return
        
        try:
            logo = self._load_logo_with_background()
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare il logo:\n{str(e)}")
            return
        
        self.progress['value'] = 0
        self.progress['maximum'] = len(self.manual_positions)
        processed = 0
        
        for idx, (img_path, position) in enumerate(self.manual_positions.items()):
            try:
                img = Image.open(img_path)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Ridimensiona logo
                logo_resized = self.processor.resize_logo(
                    logo, 
                    img, 
                    self.logo_size_percent.get()
                )
                
                # Calcola posizione
                rel_x, rel_y = position
                x = int(rel_x * img.width) - logo_resized.width // 2
                y = int(rel_y * img.height) - logo_resized.height // 2
                
                # Applica logo
                img.paste(logo_resized, (x, y), logo_resized)
                
                # Salva
                img_rgb = img.convert('RGB')
                output_name = os.path.splitext(os.path.basename(img_path))[0] + ".jpg"
                output_path = os.path.join(self.dest_folder.get(), output_name)
                img_rgb.save(output_path, OUTPUT_FORMAT, quality=OUTPUT_QUALITY)
                
                processed += 1
                
            except Exception as e:
                messagebox.showerror("Errore", f"Errore elaborazione {os.path.basename(img_path)}:\n{str(e)}")
                continue
            
            # Aggiorna progress bar
            self.progress['value'] = idx + 1
            percentage = int((idx + 1) / len(self.manual_positions) * 100)
            self.progress_label.config(
                text=f"Elaborazione: {percentage}% ({idx + 1}/{len(self.manual_positions)})"
            )
            self.root.update()
        
        self.save_settings()
        
        total_images = len(self.image_files)
        msg = f"Elaborazione completata!\n\nImmagini elaborate: {processed}\nImmagini totali: {total_images}"
        messagebox.showinfo("Completato", msg)
        self.progress_label.config(text="")
    
    def process_all_images(self):
        """Elabora tutte le immagini (modalità automatica o dopo posizionamento manuale)"""
        try:
            logo = self._load_logo_with_background()
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare il logo:\n{str(e)}")
            return
        
        self.progress['value'] = 0
        self.progress['maximum'] = len(self.image_files)
        processed = 0
        skipped = []
        
        for idx, img_path in enumerate(self.image_files):
            # Controlla se immagine posizionata in modalità manuale
            if self.position_mode.get() == "manual" and img_path not in self.manual_positions:
                response = messagebox.askyesnocancel(
                    "Immagine non posizionata",
                    f"Non hai selezionato una posizione per:\n{os.path.basename(img_path)}\n\n"
                    "Vuoi saltare questa immagine?\n\n"
                    "Sì = Salta\nNo = Interrompi ed elabora\nAnnulla = Termina"
                )
                if response is None:
                    self.progress_label.config(text="Elaborazione annullata")
                    return
                elif response is False:
                    break
                else:
                    skipped.append(os.path.basename(img_path))
                    continue
            
            try:
                img = Image.open(img_path)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Ridimensiona logo
                logo_resized = self.processor.resize_logo(
                    logo, 
                    img, 
                    self.logo_size_percent.get()
                )
                
                # Determina posizione
                if self.position_mode.get() == "manual":
                    rel_x, rel_y = self.manual_positions[img_path]
                    x = int(rel_x * img.width) - logo_resized.width // 2
                    y = int(rel_y * img.height) - logo_resized.height // 2
                else:
                    x, y = self.processor.calculate_fixed_position(
                        img.width, 
                        img.height, 
                        logo_resized.width, 
                        logo_resized.height,
                        self.fixed_position.get(), 
                        self.margin_percent.get()
                    )
                
                # Applica logo
                img.paste(logo_resized, (x, y), logo_resized)
                
                # Salva
                img_rgb = img.convert('RGB')
                output_name = os.path.splitext(os.path.basename(img_path))[0] + ".jpg"
                output_path = os.path.join(self.dest_folder.get(), output_name)
                img_rgb.save(output_path, OUTPUT_FORMAT, quality=OUTPUT_QUALITY)
                
                processed += 1
                
            except Exception as e:
                messagebox.showerror("Errore", f"Errore elaborazione {os.path.basename(img_path)}:\n{str(e)}")
                continue
            
            # Aggiorna progress bar
            self.progress['value'] = idx + 1
            percentage = int((idx + 1) / len(self.image_files) * 100)
            self.progress_label.config(
                text=f"Elaborazione: {percentage}% ({idx + 1}/{len(self.image_files)})"
            )
            self.root.update()
        
        self.save_settings()
        
        msg = f"Elaborazione completata!\n\nImmagini elaborate: {processed}"
        if skipped:
            msg += f"\nImmagini saltate: {len(skipped)}"
        messagebox.showinfo("Completato", msg)
        self.progress_label.config(text="")
    
    def save_settings(self):
        """Salva le impostazioni correnti"""
        settings = {
            "source_folder": self.source_folder.get(),
            "logo_file": self.logo_file.get(),
            "dest_folder": self.dest_folder.get(),
            "position_mode": self.position_mode.get(),
            "fixed_position": self.fixed_position.get(),
            "logo_size_percent": self.logo_size_percent.get(),
            "margin_percent": self.margin_percent.get(),
            "bg_color": self.bg_color.get(),
            "bg_shape": self.bg_shape.get()
        }
        SettingsManager.save_settings(settings)
    
    def load_settings(self):
        """Carica le impostazioni salvate"""
        settings = SettingsManager.load_settings()
        self.source_folder.set(settings.get("source_folder", ""))
        self.logo_file.set(settings.get("logo_file", ""))
        self.dest_folder.set(settings.get("dest_folder", ""))
        self.position_mode.set(settings.get("position_mode", "manual"))
        self.fixed_position.set(settings.get("fixed_position", "top_left"))
        self.logo_size_percent.set(settings.get("logo_size_percent", 10))
        self.margin_percent.set(settings.get("margin_percent", 2))
        self.bg_color.set(settings.get("bg_color", "Nessuno"))
        self.bg_shape.set(settings.get("bg_shape", "Rettangolare"))