#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modulo per l'elaborazione delle immagini
"""

from PIL import Image, ImageDraw
import os
from config import OUTPUT_QUALITY, OUTPUT_FORMAT, BACKGROUND_COLORS


class ImageProcessor:
    """Classe per gestire l'elaborazione delle immagini"""
    
    @staticmethod
    def create_logo_with_background(logo, bg_color, bg_shape, padding=10):
        """
        Crea un logo con sfondo colorato
        
        Args:
            logo: Immagine PIL del logo
            bg_color: Colore esadecimale dello sfondo (es. '#FFFFFF')
            bg_shape: Forma dello sfondo ('Circolare', 'Rettangolare', 'Ovale')
            padding: Padding attorno al logo (pixel)
            
        Returns:
            Immagine PIL con logo e sfondo
        """
        if bg_color is None or bg_color == 'Nessuno':
            return logo
        
        # Dimensioni del canvas
        new_width = logo.width + padding * 2
        new_height = logo.height + padding * 2
        
        # Crea canvas trasparente
        result = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(result)
        
        # Converti colore esadecimale in RGB
        bg_rgb = ImageProcessor._hex_to_rgb(bg_color)
        
        # Disegna lo sfondo in base alla forma
        if bg_shape == 'Circolare':
            # Usa il diametro del lato più lungo per il cerchio
            diameter = max(new_width, new_height)
            offset_x = (diameter - new_width) // 2
            offset_y = (diameter - new_height) // 2
            draw.ellipse([0 - offset_x, 0 - offset_y, diameter - offset_x, diameter - offset_y], 
                        fill=bg_rgb)
            
        elif bg_shape == 'Ovale':
            # Ellisse "vera": allarga un po' la larghezza
            oval_width = int(new_width)
            oval_height = int(new_height * 0.8)
            offset_x = (oval_width - new_width) // 2
            offset_y = (oval_height - new_height) // 2
            draw.ellipse(
                [0 - offset_x, 0 - offset_y, oval_width - offset_x, oval_height - offset_y],
                fill=bg_rgb
            )

        elif bg_shape == 'Rettangolare':
            # Rettangolo allungato orizzontalmente
            rect_width = int(new_width)
            rect_height = int(new_height * 0.8)
            offset_x = (rect_width - new_width) // 2
            offset_y = (rect_height - new_height) // 2
            draw.rectangle(
                [0 - offset_x, 0 - offset_y, rect_width - offset_x, rect_height - offset_y],
                fill=bg_rgb
            )
        
        # Incolla il logo al centro
        result.paste(logo, (padding, padding), logo if logo.mode == 'RGBA' else None)
        
        return result
    
    @staticmethod
    def _hex_to_rgb(hex_color):
        """Converte colore esadecimale in tupla RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def resize_logo(logo, target_img, size_percent):
        """
        Ridimensiona il logo in base all'orientamento dell'immagine target
        
        Args:
            logo: Immagine PIL del logo
            target_img: Immagine PIL target
            size_percent: Percentuale di dimensione (5-20)
            
        Returns:
            Logo ridimensionato
        """
        is_horizontal = target_img.width >= target_img.height
        
        if is_horizontal:
            logo_width = int(target_img.width * (size_percent / 100))
            logo_ratio = logo_width / logo.width
            logo_height = int(logo.height * logo_ratio)
        else:
            logo_height = int(target_img.height * (size_percent / 100))
            logo_ratio = logo_height / logo.height
            logo_width = int(logo.width * logo_ratio)
        
        return logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def calculate_fixed_position(img_width, img_height, logo_width, logo_height, 
                                 position_type, margin_percent):
        """
        Calcola posizione fissa del logo
        
        Args:
            img_width: Larghezza immagine
            img_height: Altezza immagine
            logo_width: Larghezza logo
            logo_height: Altezza logo
            position_type: Tipo posizione ('top_left', 'top_right', etc.)
            margin_percent: Percentuale di margine
            
        Returns:
            Tupla (x, y) con coordinate
        """
        margin = int(min(img_width, img_height) * (margin_percent / 100))
        
        positions = {
            "top_left": (margin, margin),
            "top_right": (img_width - logo_width - margin, margin),
            "bottom_left": (margin, img_height - logo_height - margin),
            "bottom_right": (img_width - logo_width - margin, img_height - logo_height - margin)
        }
        
        return positions.get(position_type, (margin, margin))
    
    @staticmethod
    def apply_logo_to_image(img_path, logo, position, output_path):
        """
        Applica il logo all'immagine e salva
        
        Args:
            img_path: Percorso immagine sorgente
            logo: Immagine PIL del logo (già ridimensionato)
            position: Tupla (x, y) con posizione
            output_path: Percorso output
            
        Returns:
            True se successo, False altrimenti
        """
        try:
            img = Image.open(img_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Applica logo
            img.paste(logo, position, logo if logo.mode == 'RGBA' else None)
            
            # Converti in RGB e salva
            img_rgb = img.convert('RGB')
            img_rgb.save(output_path, OUTPUT_FORMAT, quality=OUTPUT_QUALITY)
            
            return True
        except Exception as e:
            print(f"Errore nell'applicazione del logo: {e}")
            return False
    
    @staticmethod
    def get_image_files(folder_path, extensions):
        """
        Ottiene lista di file immagine in una cartella
        
        Args:
            folder_path: Percorso cartella
            extensions: Tupla di estensioni supportate
            
        Returns:
            Lista ordinata di percorsi file
        """
        files = []
        for file in os.listdir(folder_path):
            if file.lower().endswith(extensions):
                files.append(os.path.join(folder_path, file))
        return sorted(files)