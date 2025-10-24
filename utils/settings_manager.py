#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modulo per la gestione delle impostazioni utente
"""

import json
import os
from config import SETTINGS_FILE


class SettingsManager:
    """Classe per gestire il salvataggio e caricamento delle impostazioni"""
    
    @staticmethod
    def save_settings(settings_dict):
        """
        Salva le impostazioni in un file JSON
        
        Args:
            settings_dict: Dizionario con le impostazioni
            
        Returns:
            True se successo, False altrimenti
        """
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings_dict, f, indent=2)
            return True
        except Exception as e:
            print(f"Errore nel salvataggio delle impostazioni: {e}")
            return False
    
    @staticmethod
    def load_settings():
        """
        Carica le impostazioni dal file JSON
        
        Returns:
            Dizionario con le impostazioni o dizionario vuoto se file non esiste
        """
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Errore nel caricamento delle impostazioni: {e}")
            return {}
    
    @staticmethod
    def get_setting(key, default=None):
        """
        Ottiene un singolo valore dalle impostazioni
        
        Args:
            key: Chiave dell'impostazione
            default: Valore di default se non trovato
            
        Returns:
            Valore dell'impostazione
        """
        settings = SettingsManager.load_settings()
        return settings.get(key, default)