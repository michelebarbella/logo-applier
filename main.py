#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Applicatore Logo su Immagini - Main Entry Point
"""

__author__ = "Michele Barbella"
__version__ = "1.0.0"
__license__ = "MIT"

import tkinter as tk
from gui.main_window import LogoApplierApp

def main():
    """Punto di ingresso principale dell'applicazione"""
    root = tk.Tk()
    app = LogoApplierApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()