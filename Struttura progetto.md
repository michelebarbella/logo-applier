# 📁 Struttura del Progetto - Applicatore Logo su Immagini

## 🏗️ Architettura Modulare

Il progetto è stato ristrutturato seguendo i principi dell'ingegneria del software:
- **Modularità**: Separazione in moduli distinti
- **Separation of Concerns**: Ogni modulo ha una responsabilità specifica
- **Single Responsibility Principle**: Ogni classe ha un unico scopo
- **DRY (Don't Repeat Yourself)**: Codice riutilizzabile

## 📂 Struttura Directory

```
logo-applier/
│
├── main.py                          # Entry point dell'applicazione
├── config.py                        # Configurazioni globali
├── requirements.txt                 # Dipendenze Python
├── settings.json                    # Impostazioni utente (auto-generato)
│
├── gui/                             # Moduli interfaccia grafica
│   ├── __init__.py
│   ├── main_window.py              # Finestra principale
│   └── preview_window.py           # Finestra anteprima
│
├── utils/                           # Moduli utilità
│   ├── __init__.py
│   ├── image_processor.py          # Elaborazione immagini
│   └── settings_manager.py         # Gestione impostazioni
│
├── docs/                            # Documentazione
│   ├── README.md                   # Italiano
│   ├── README.en.md                # Inglese
│   └── ARCHITECTURE.md             # Documentazione architettura
│
└── examples/                        # Esempi e test
    ├── logo_esempio.png
    └── test_images/
```

## 📋 Descrizione Moduli

### 1. **main.py** - Entry Point
```python
#!/usr/bin/env python3
# Avvia l'applicazione
```
- Punto di ingresso dell'applicazione
- Inizializza la GUI principale
- Gestisce il ciclo eventi Tkinter

### 2. **config.py** - Configurazione Globale
```python
# Configurazioni centralizzate
APP_NAME = "Applicatore Logo su Immagini"
WINDOW_WIDTH = 750
BACKGROUND_COLORS = {...}
```
- Costanti applicazione
- Configurazioni GUI
- Opzioni disponibili (colori, forme, dimensioni)
- Parametri di elaborazione

### 3. **gui/main_window.py** - Finestra Principale
```python
class LogoApplierApp:
    def __init__(self, root)
    def build_gui()
    def start_processing()
    def process_all_images()
```
**Responsabilità:**
- Interfaccia grafica principale
- Gestione eventi utente
- Coordinamento workflow elaborazione
- Salvataggio/caricamento impostazioni

**Componenti GUI:**
- Frame selezione file (source, logo, destination)
- Frame impostazioni logo (dimensione, margine)
- Frame sfondo logo (colore, forma)
- Frame posizionamento (manuale/automatico)
- Progress bar con percentuale
- Menu informazioni

### 4. **gui/preview_window.py** - Finestra Anteprima
```python
class PreviewWindow:
    def __init__(self, parent, img, logo, ...)
    def on_canvas_hover(self, event)
    def on_canvas_click(self, event)
```
**Responsabilità:**
- Visualizzazione anteprima interattiva
- Gestione hover del mouse con logo
- Gestione click per posizionamento
- Progress bar secondaria
- Callback verso finestra principale

**Funzionalità:**
- Anteprima live del logo durante hover
- Protezione bordi automatica
- Ridimensionamento proporzionale
- Centratura automatica finestra

### 5. **utils/image_processor.py** - Elaborazione Immagini
```python
class ImageProcessor:
    @staticmethod
    def create_logo_with_background(logo, color, shape)
    @staticmethod
    def resize_logo(logo, target_img, size_percent)
    @staticmethod
    def calculate_fixed_position(...)
    @staticmethod
    def apply_logo_to_image(...)
```
**Responsabilità:**
- Creazione logo con sfondo colorato
- Ridimensionamento intelligente logo
- Calcolo posizioni fisse
- Applicazione logo su immagine
- Gestione formati e conversioni

**Algoritmi:**
- Ridimensionamento adattivo (orizzontale/verticale)
- Disegno forme geometriche (cerchio, rettangolo, ovale)
- Conversione colori esadecimali
- Gestione trasparenza alpha

### 6. **utils/settings_manager.py** - Gestione Impostazioni
```python
class SettingsManager:
    @staticmethod
    def save_settings(settings_dict)
    @staticmethod
    def load_settings()
    @staticmethod
    def get_setting(key, default)
```
**Responsabilità:**
- Salvataggio persistente impostazioni
- Caricamento impostazioni all'avvio
- Gestione file JSON
- Validazione dati

## 🆕 Nuove Funzionalità - Sfondo Logo

### Configurazione Sfondo (config.py)
```python
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
```

### GUI - Frame Sfondo Logo
```python
def _build_background_frame(self):
    # Combobox per selezione colore
    color_combo = ttk.Combobox(
        textvariable=self.bg_color,
        values=list(BACKGROUND_COLORS.keys())
    )
    
    # Radiobutton per forma
    for shape in BACKGROUND_SHAPES:
        ttk.Radiobutton(..., value=shape)
```

### Processore - Creazione Sfondo
```python
def create_logo_with_background(logo, bg_color, bg_shape, padding=10):
    # Crea canvas trasparente
    result = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(result)
    
    # Disegna forma in base a selezione
    if bg_shape == 'Circolare':
        draw.ellipse([...], fill=bg_rgb)
    elif bg_shape == 'Ovale':
        draw.ellipse([...], fill=bg_rgb)
    elif bg_shape == 'Rettangolare':
        draw.rectangle([...], fill=bg_rgb)
    
    # Incolla logo al centro
    result.paste(logo, (padding, padding), logo)
```

## 🔄 Flusso di Esecuzione

### 1. **Avvio Applicazione**
```
main.py → LogoApplierApp.__init__() → load_settings() → build_gui()
```

### 2. **Workflow Modalità Manuale**
```
start_processing() 
  → show_next_image_for_positioning()
    → _load_logo_with_background() [NUOVO]
      → create_logo_with_background() [se colore selezionato]
    → PreviewWindow.__init__()
      → on_canvas_hover() [anteprima live]
      → on_canvas_click() [conferma posizione]
        → position_callback()
          → show_next_image_for_positioning() [ricorsivo]
  → process_all_images() [quando tutte posizionate]
    → save_settings()
```

### 3. **Workflow Modalità Automatica**
```
start_processing()
  → process_all_images()
    → _load_logo_with_background() [NUOVO]
    → resize_logo() [per ogni immagine]
    → calculate_fixed_position()
    → apply_logo_to_image()
    → save_settings()
```

## 📦 Dipendenze

### requirements.txt
```
Pillow>=10.0.0
```

### Librerie Standard Utilizzate
- `tkinter` - Interfaccia grafica
- `json` - Gestione settings
- `os` - Operazioni filesystem
- `pathlib` - Gestione percorsi

## 🎨 Design Pattern Utilizzati

### 1. **Singleton-like Pattern**
```python
class SettingsManager:
    @staticmethod
    def save_settings(...)
```
Metodi statici per accesso globale alle impostazioni

### 2. **Callback Pattern**
```python
PreviewWindow(..., position_callback, close_callback)
```
Comunicazione tra finestre tramite callbacks

### 3. **Factory-like Pattern**
```python
ImageProcessor.create_logo_with_background(...)
```
Creazione oggetti complessi (logo con sfondo)

### 4. **Strategy Pattern**
```python
if bg_shape == 'Circolare':
    draw.ellipse(...)
elif bg_shape == 'Ovale':
    draw.ellipse(...)
elif bg_shape == 'Rettangolare':
    draw.rectangle(...)
```
Selezione algoritmo basata su input utente

## 🚀 Come Eseguire

### 1. Installa dipendenze
```bash
pip install -r requirements.txt
```

### 2. Crea struttura directory
```bash
mkdir -p gui utils docs examples
```

### 3. Crea file __init__.py
```bash
touch gui/__init__.py utils/__init__.py
```

### 4. Esegui applicazione
```bash
python main.py
```

## 📝 File da Creare

### File Essenziali
1. ✅ `main.py`
2. ✅ `config.py`
3. ✅ `gui/__init__.py` (vuoto)
4. ✅ `gui/main_window.py`
5. ✅ `gui/preview_window.py`
6. ✅ `utils/__init__.py` (vuoto)
7. ✅ `utils/image_processor.py`
8. ✅ `utils/settings_manager.py`
9. ✅ `requirements.txt`

### File Opzionali
10. 📄 `README.md`
11. 📄 `README.en.md`
12. 📄 `LICENSE`
13. 📄 `.gitignore`

## 🔍 Vantaggi Architettura Modulare

### ✅ Manutenibilità
- Facile individuare e correggere bug
- Modifiche isolate a singoli moduli
- Test più semplici

### ✅ Riusabilità
- `ImageProcessor` riutilizzabile in altri progetti
- `SettingsManager` generico
- Separazione GUI da logica business

### ✅ Scalabilità
- Facile aggiungere nuove funzionalità
- Estendibile con plugin
- Possibilità di sostituire moduli

### ✅ Leggibilità
- Codice organizzato logicamente
- File di dimensioni gestibili
- Chiare responsabilità

## 🆕 Estensioni Future Possibili

### Facili da Implementare (modularità)
1. **Nuovi colori sfondo**: Aggiungere in `config.py` → `BACKGROUND_COLORS`
2. **Nuove forme**: Aggiungere metodo in `ImageProcessor.create_logo_with_background()`
3. **Filtri immagine**: Nuovo metodo in `ImageProcessor`
4. **Export batch**: Nuovo modulo `utils/batch_exporter.py`
5. **Preset configurazioni**: Estensione `SettingsManager` con preset multipli

### Moduli Aggiuntivi Suggeriti
```
├── utils/
│   ├── validators.py          # Validazione input
│   ├── file_handler.py        # Gestione file avanzata
│   └── image_effects.py       # Effetti speciali
│
├── gui/
│   ├── settings_dialog.py     # Finestra impostazioni avanzate
│   ├── preview_grid.py        # Griglia thumbnail
│   └── help_window.py         # Finestra aiuto
│
└── tests/
    ├── test_image_processor.py
    ├── test_settings_manager.py
    └── test_integration.py
```

## 🔧 Configurazione Avanzata

### Personalizzazione Colori Sfondo

Per aggiungere nuovi colori, modifica `config.py`:

```python
BACKGROUND_COLORS = {
    'Nessuno': None,
    'Bianco': '#FFFFFF',
    'Giallo': '#FFFF00',
    'Arancione': '#FFA500',
    'Rosso': '#FF0000',
    'Celeste': '#87CEEB',
    # Aggiungi qui nuovi colori
    'Verde': '#00FF00',
    'Blu': '#0000FF',
    'Viola': '#800080',
    'Rosa': '#FFC0CB',
    'Nero': '#000000',
    'Grigio': '#808080'
}
```

### Personalizzazione Forme

Per aggiungere nuove forme, modifica `utils/image_processor.py`:

```python
def create_logo_with_background(logo, bg_color, bg_shape, padding=10):
    # ... codice esistente ...
    
    if bg_shape == 'Circolare':
        draw.ellipse([...], fill=bg_rgb)
    elif bg_shape == 'Ovale':
        draw.ellipse([...], fill=bg_rgb)
    elif bg_shape == 'Rettangolare':
        draw.rectangle([...], fill=bg_rgb)
    
    # Aggiungi nuove forme qui
    elif bg_shape == 'Rombo':
        points = [(new_width//2, 0), (new_width, new_height//2), 
                  (new_width//2, new_height), (0, new_height//2)]
        draw.polygon(points, fill=bg_rgb)
    
    elif bg_shape == 'Stella':
        # Implementa disegno stella
        pass
```

Poi aggiungi in `config.py`:
```python
BACKGROUND_SHAPES = ['Circolare', 'Rettangolare', 'Ovale', 'Rombo', 'Stella']
```

## 📊 Diagramma Classi (UML)

```
┌─────────────────────┐
│   LogoApplierApp    │
│    (main_window)    │
├─────────────────────┤
│ - source_folder     │
│ - logo_file         │
│ - bg_color [NEW]    │
│ - bg_shape [NEW]    │
├─────────────────────┤
│ + build_gui()       │
│ + start_processing()│
│ + save_settings()   │
└──────┬──────────────┘
       │ usa
       │
       ├──────────────────────────┐
       │                          │
       ▼                          ▼
┌──────────────────┐    ┌─────────────────────┐
│ PreviewWindow    │    │  ImageProcessor     │
├──────────────────┤    ├─────────────────────┤
│ - canvas         │    │ + create_logo_      │
│ - preview_logo   │    │   with_background() │
├──────────────────┤    │   [NEW]             │
│ + on_hover()     │    │ + resize_logo()     │
│ + on_click()     │    │ + calculate_pos()   │
└──────────────────┘    └─────────────────────┘
       │
       │ callback
       ▼
┌──────────────────────┐
│  SettingsManager     │
├──────────────────────┤
│ + save_settings()    │
│ + load_settings()    │
└──────────────────────┘
```

## 🧪 Testing

### Unit Test Esempio (`tests/test_image_processor.py`)

```python
import unittest
from utils.image_processor import ImageProcessor
from PIL import Image

class TestImageProcessor(unittest.TestCase):
    
    def setUp(self):
        self.processor = ImageProcessor()
        self.logo = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
    
    def test_create_logo_with_background_rectangle(self):
        result = self.processor.create_logo_with_background(
            self.logo, '#FFFFFF', 'Rettangolare', padding=10
        )
        self.assertEqual(result.width, 120)
        self.assertEqual(result.height, 120)
    
    def test_create_logo_with_background_circle(self):
        result = self.processor.create_logo_with_background(
            self.logo, '#FF0000', 'Circolare', padding=10
        )
        self.assertIsNotNone(result)
    
    def test_resize_logo_horizontal(self):
        target = Image.new('RGB', (1920, 1080))
        result = self.processor.resize_logo(self.logo, target, 10)
        expected_width = int(1920 * 0.1)
        self.assertEqual(result.width, expected_width)

if __name__ == '__main__':
    unittest.main()
```

## 📝 File __init__.py

### `gui/__init__.py`
```python
"""
Modulo GUI dell'applicazione
"""

from .main_window import LogoApplierApp
from .preview_window import PreviewWindow

__all__ = ['LogoApplierApp', 'PreviewWindow']
```

### `utils/__init__.py`
```python
"""
Modulo utilità dell'applicazione
"""

from .image_processor import ImageProcessor
from .settings_manager import SettingsManager

__all__ = ['ImageProcessor', 'SettingsManager']
```

## 🎯 Best Practices Implementate

### 1. **Naming Conventions**
- Classi: `PascalCase` (es. `LogoApplierApp`)
- Funzioni/Metodi: `snake_case` (es. `create_logo_with_background`)
- Costanti: `UPPER_CASE` (es. `BACKGROUND_COLORS`)
- Private: prefisso `_` (es. `_build_gui`)

### 2. **Docstrings**
```python
def create_logo_with_background(logo, bg_color, bg_shape, padding=10):
    """
    Crea un logo con sfondo colorato
    
    Args:
        logo: Immagine PIL del logo
        bg_color: Colore esadecimale dello sfondo
        bg_shape: Forma dello sfondo
        padding: Padding attorno al logo (pixel)
        
    Returns:
        Immagine PIL con logo e sfondo
    """
```

### 3. **Error Handling**
```python
try:
    logo = Image.open(self.logo_file.get())
except Exception as e:
    messagebox.showerror("Errore", f"Impossibile caricare: {str(e)}")
    return
```

### 4. **Type Hints (opzionale per Python 3.8+)**
```python
from typing import Optional, Tuple

def create_logo_with_background(
    logo: Image.Image, 
    bg_color: Optional[str], 
    bg_shape: str, 
    padding: int = 10
) -> Image.Image:
    pass
```

## 🔐 Sicurezza e Validazione

### Validazione Input Percorsi
```python
def validate_inputs(self):
    if not os.path.exists(self.source_folder.get()):
        raise ValueError("Cartella sorgente non esiste")
    
    if not os.access(self.dest_folder.get(), os.W_OK):
        raise PermissionError("Nessun permesso scrittura")
```

### Sanitizzazione Nome File
```python
import re

def sanitize_filename(filename):
    # Rimuovi caratteri non validi
    return re.sub(r'[<>:"/\\|?*]', '_', filename)
```

## 📚 Risorse Aggiuntive

### Documentazione Librerie
- [Pillow Docs](https://pillow.readthedocs.io/)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- [Python JSON](https://docs.python.org/3/library/json.html)

### Tutorial Consigliati
- Design Patterns in Python
- GUI Best Practices
- Image Processing with Pillow

## ⚡ Performance Tips

### Ottimizzazioni Possibili
1. **Caching logo ridimensionato** per immagini stessa dimensione
2. **Thread separato** per elaborazione (evita freeze GUI)
3. **Generator** invece di liste per file molto grandi
4. **PIL ottimizzato** con `pillow-simd` su Linux

### Esempio Thread Processing
```python
import threading

def process_async(self):
    thread = threading.Thread(target=self.process_all_images)
    thread.daemon = True
    thread.start()
```

## 🎓 Principi SOLID Applicati

1. **S**ingle Responsibility: Ogni classe ha un compito specifico
2. **O**pen/Closed: Estendibile senza modificare codice esistente
3. **L**iskov Substitution: Callback pattern permette sostituzioni
4. **I**nterface Segregation: Interfacce minimali e chiare
5. **D**ependency Inversion: Dipendenza da astrazioni (callbacks)

---

## 📞 Supporto

Per domande o problemi:
- **Email**: m.barbella5@gmail.com
- **GitHub**: https://github.com/michelebarbella
- **LinkedIn**: https://www.linkedin.com/in/michele-barbella

---

**Versione**: 1.0.0  
**Ultimo aggiornamento**: Ottobre 2025  
**Autore**: Michele Barbella