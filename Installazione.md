# 🚀 Guida Rapida - Installazione e Avvio

## 📋 Prerequisiti

- Python 3.8 o superiore
- pip (gestore pacchetti Python)

## 📥 Passo 1: Scarica il Codice

### Opzione A: Clone da GitHub (se hai Git)
```bash
git clone https://github.com/michelebarbella/logo-applier.git
cd logo-applier
```

### Opzione B: Download Manuale
1. Scarica tutti i file
2. Crea la seguente struttura:

```
logo-applier/
├── main.py
├── config.py
├── requirements.txt
├── gui/
│   ├── __init__.py
│   ├── main_window.py
│   └── preview_window.py
└── utils/
    ├── __init__.py
    ├── image_processor.py
    └── settings_manager.py
```

## 🔧 Passo 2: Crea File __init__.py

Crea due file vuoti (o con il contenuto indicato sotto):

### `gui/__init__.py`
```python
"""Modulo GUI"""
from .main_window import LogoApplierApp
from .preview_window import PreviewWindow

__all__ = ['LogoApplierApp', 'PreviewWindow']
```

### `utils/__init__.py`
```python
"""Modulo utilità"""
from .image_processor import ImageProcessor
from .settings_manager import SettingsManager

__all__ = ['ImageProcessor', 'SettingsManager']
```

## 📦 Passo 3: Installa Dipendenze

### Windows
```bash
pip install -r requirements.txt
```

### macOS/Linux
```bash
pip3 install -r requirements.txt
```

### Ambiente Virtuale (Consigliato)
```bash
# Crea ambiente virtuale
python -m venv venv

# Attiva ambiente
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
```

## ▶️ Passo 4: Avvia l'Applicazione

```bash
python main.py
```

## ✅ Verifica Installazione

Se tutto funziona correttamente, dovresti vedere la finestra principale dell'applicazione con:
- Sezione "Selezione File e Cartelle"
- Sezione "Impostazioni Logo"
- **Sezione "Sfondo Logo"**
- Sezione "Modalità Posizionamento"
- Barra di progresso
- Pulsante "Avvia Elaborazione"

## 🎨 Sfondo Logo

### Come Usare lo Sfondo

1. **Senza Sfondo** (Logo originale):
   - Colore: Seleziona "Nessuno"
   
2. **Con Sfondo Colorato**:
   - Colore: Seleziona tra Bianco, Giallo, Arancione, Rosso, Celeste
   - Forma: Scegli tra Circolare, Rettangolare, Ovale
   
### Esempio d'Uso

**Logo con sfondo bianco rettangolare:**
```
Colore sfondo: Bianco
Forma: Rettangolare
```

**Logo con sfondo celeste circolare:**
```
Colore sfondo: Celeste
Forma: Circolare
```

## 🐛 Risoluzione Problemi

### Errore: "No module named 'PIL'"
```bash
pip install Pillow
```

### Errore: "No module named 'gui'"
Verifica di aver creato i file `__init__.py` in entrambe le cartelle `gui/` e `utils/`

### Errore: "ModuleNotFoundError: No module named 'config'"
Assicurati che `config.py` sia nella stessa cartella di `main.py`

### Errore: "tkinter not found"
**Windows**: Reinstalla Python includendo tk/tcl  
**Ubuntu/Debian**: `sudo apt-get install python3-tk`  
**macOS**: Dovrebbe essere già incluso

### L'applicazione si avvia ma non vedo la sezione "Sfondo Logo"
Assicurati di aver copiato la versione più recente di `gui/main_window.py` che include il metodo `_build_background_frame()`

## 📝 File Generati Automaticamente

Dopo il primo utilizzo, l'applicazione creerà:
- `settings.json` - Contiene le tue preferenze salvate


Poi reinstalla le dipendenze (potrebbero esserci aggiornamenti):
```bash
pip install -r requirements.txt --upgrade
```

## 📚 Prossimi Passi

1. ✅ Leggi il file `STRUTTURA_PROGETTO.md` per capire l'architettura
2. ✅ Consulta `README.md` per la documentazione completa
3. ✅ Prova l'applicazione con immagini di test
4. ✅ Sperimenta con diversi colori e forme di sfondo

## 💡 Suggerimenti Primo Utilizzo

1. **Prepara le immagini**: Metti tutte le immagini in una cartella
2. **Prepara il logo**: Usa preferibilmente PNG con sfondo trasparente
3. **Scegli sfondo**: Se il tuo logo è piccolo o monocromatico, prova ad aggiungere uno sfondo
4. **Testa prima**: Prova con 2-3 immagini prima di elaborare tutto il batch
5. **Controlla risultato**: Verifica la cartella di destinazione dopo l'elaborazione

## 🎯 Workflow Consigliato

### Prima Volta
1. Avvia applicazione: `python main.py`
2. Seleziona cartella con 2-3 immagini di test
3. Seleziona il tuo logo
4. Seleziona cartella output
5. **Scegli colore e forma sfondo** (prova diverse combinazioni)
6. Scegli dimensione logo: 10-15%
7. Prova modalità automatica con posizione "Basso a destra"
8. Verifica risultati
9. Se soddisfatto, elabora tutte le immagini

### Uso Regolare
1. Avvia applicazione (le impostazioni precedenti sono già caricate)
2. Cambia solo la cartella sorgente se necessario
3. Avvia elaborazione

## 🆘 Supporto

In caso di problemi:
1. Verifica di aver seguito tutti i passi
2. Controlla che Python sia versione 3.8+: `python --version`
3. Controlla che Pillow sia installato: `pip show Pillow`
4. Leggi i messaggi di errore completi
5. Contatta: m.barbella5@gmail.com

## ⚡ Performance

### Tempi di Elaborazione Stimati
- **10 immagini (Full HD)**: ~20-30 secondi
- **50 immagini (Full HD)**: ~2-3 minuti
- **100 immagini (4K)**: ~10-15 minuti

*I tempi variano in base alla potenza del PC e alla dimensione delle immagini*

## 🎉 Pronto!

Ora sei pronto per usare l'applicazione con la funzionalità di sfondo personalizzato per il logo!

---

**Versione Guida**: 1.0.0  
**Data**: Ottobre 2025  
**Autore**: Michele Barbella