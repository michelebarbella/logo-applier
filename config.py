#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modulo di configurazione dell'applicazione
"""

# Informazioni applicazione
APP_NAME = "Applicatore Logo su Immagini"
APP_VERSION = "1.0.0"
AUTHOR = "Michele Barbella"
EMAIL = "m.barbella5@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/michele-barbella"
GITHUB = "https://github.com/michelebarbella"
LICENSE = "MIT"
COPYRIGHT = f"Copyright 2025, {AUTHOR}"

# Configurazione GUI
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 620
PREVIEW_MAX_WIDTH = 1000
PREVIEW_MAX_HEIGHT = 900

# Opzioni logo
LOGO_SIZE_OPTIONS = [5, 10, 15, 20]  # percentuali
MARGIN_OPTIONS = [1, 2, 5, 10, 15]  # percentuali

# Formati supportati
SUPPORTED_IMAGE_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

CLICK_DELAY = 200

OUTPUT_QUALITY = 100

OUTPUT_FORMAT = "JPEG"

BACKGROUND_COLORS = {
    'Nessuno': None,
    'Bianco': '#FFFFFF',
    'Grigio chiaro': '#D3D3D3',
    'Rosa pallido': '#FFD1DC',
    'Giallo chiaro': '#FFFACD',
    'Giallo': '#FFFF00',
    'Arancione chiaro': '#FFD580',
    'Arancione': '#FFA500',
    'Rosso': '#FF0000',
    'Azzurro pastello': '#ADD8E6',
    'Celeste': '#87CEEB',
    'Verde menta': '#98FB98',
}

BACKGROUND_SHAPES = ['Circolare', 'Rettangolare', 'Ovale']

# Posizioni fisse
FIXED_POSITIONS = {
    'top_left': 'In alto a sinistra',
    'top_right': 'In alto a destra',
    'bottom_left': 'In basso a sinistra',
    'bottom_right': 'In basso a destra'
}

# Qualità output
OUTPUT_QUALITY = 100
OUTPUT_FORMAT = 'JPEG'

# File di configurazione utente
SETTINGS_FILE = 'settings.json'

# Delay dopo click (millisecondi)
CLICK_DELAY = 200