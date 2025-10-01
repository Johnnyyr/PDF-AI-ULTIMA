# OCR Watcher Service

Automatischer Service zur Überwachung von `/Volumes/DataEX/inbox` und OCR-Verarbeitung von PDFs.

## Features

- **Automatische Überwachung**: Rekursive Überwachung des Inbox-Ordners
- **OCRmyPDF Integration**: Professionelle OCR-Verarbeitung mit konfigurierbaren Parametern
- **Intelligente Dateiorganisation**:
  - Originale → `inbox/archive`
  - Verarbeitete PDFs + Sidecar → `inbox/ocr`
- **macOS Tags**: Automatisches Setzen von Finder-Tags (`ocr`)
- **Debouncing**: Vermeidet mehrfache Verarbeitung bei schnellen Änderungen

## Voraussetzungen

1. **OCRmyPDF installieren**:
   ```bash
   brew install ocrmypdf
   ```

2. **Dependencies installieren**:
   ```bash
   cd /Volumes/DataEX/Apps/my-fastapi-ocr
   uv sync
   # oder mit pip:
   pip install -r requirements.txt
   ```

3. **Optional: `tag` CLI für bessere macOS Tag-Unterstützung**:
   ```bash
   brew install tag
   ```

## Konfiguration

### Option 1: Environment Variables (empfohlen)

Kopiere `.env.watcher` nach `.env` und passe an:

```bash
cp .env.watcher .env
nano .env
```

### Option 2: YAML-Konfiguration

Bearbeite `config/watcher.yaml`:

```yaml
watcher:
  inbox_path: "/Volumes/DataEX/inbox"
  ocrmypdf_path: "/opt/homebrew/bin/ocrmypdf"
  debounce_seconds: 2.0
  preserve_structure: false
  set_tags: true
  tags:
    - ocr
```

## Verwendung

### Manueller Start

```bash
# Mit Environment Variables
source .env
python watcher_service.py

# Oder direkt mit Parametern
INBOX_PATH=/Volumes/DataEX/inbox python watcher_service.py
```

### Als launchd Service (macOS - empfohlen)

1. **LaunchAgent erstellen**:

   ```bash
   nano ~/Library/LaunchAgents/com.ocr.watcher.plist
   ```

   Inhalt:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.ocr.watcher</string>

       <key>ProgramArguments</key>
       <array>
           <string>/usr/bin/python3</string>
           <string>/Volumes/DataEX/Apps/my-fastapi-ocr/watcher_service.py</string>
       </array>

       <key>EnvironmentVariables</key>
       <dict>
           <key>INBOX_PATH</key>
           <string>/Volumes/DataEX/inbox</string>
           <key>OCRMYPDF_PATH</key>
           <string>/opt/homebrew/bin/ocrmypdf</string>
           <key>LOG_LEVEL</key>
           <string>INFO</string>
       </dict>

       <key>RunAtLoad</key>
       <true/>

       <key>KeepAlive</key>
       <true/>

       <key>StandardOutPath</key>
       <string>/tmp/ocr-watcher.log</string>

       <key>StandardErrorPath</key>
       <string>/tmp/ocr-watcher.error.log</string>
   </dict>
   </plist>
   ```

2. **Service aktivieren**:

   ```bash
   launchctl load ~/Library/LaunchAgents/com.ocr.watcher.plist
   launchctl start com.ocr.watcher
   ```

3. **Status prüfen**:

   ```bash
   launchctl list | grep ocr.watcher
   tail -f /tmp/ocr-watcher.log
   ```

4. **Service stoppen**:

   ```bash
   launchctl stop com.ocr.watcher
   launchctl unload ~/Library/LaunchAgents/com.ocr.watcher.plist
   ```

## Workflow

1. **Neue PDF landet in `/Volumes/DataEX/inbox`** (oder Unterordner)
2. **Watcher erkennt Datei** nach `DEBOUNCE_SECONDS` (Standard: 2s)
3. **Original wird kopiert** nach `inbox/archive/`
4. **OCR-Verarbeitung** mit OCRmyPDF:
   - `--skip-text`: Vorhandener Text bleibt erhalten
   - `--rotate-pages`: Automatische Rotation
   - `--deskew`: Schiefe korrigieren
   - `--clean` + `--clean-final`: Hintergrund bereinigen
   - `--optimize 2`: Balance zwischen Größe und Qualität
   - `--language deu+eng`: Deutsch + Englisch
   - `--sidecar`: Textdatei neben PDF
5. **Verarbeitete PDF + Sidecar** → `inbox/ocr/`
6. **macOS Tags gesetzt**: `ocr` (oder konfigurierbar)
7. **Original aus Inbox gelöscht** (bereits im Archiv)

## OCRmyPDF Parameter

Die Standard-Parameter sind in [watcher_service.py](watcher_service.py) definiert:

```python
[
    "--skip-text",           # Vorhandenen Text nicht entfernen
    "--rotate-pages",        # Seiten automatisch drehen
    "--deskew",              # Schiefe Scans korrigieren
    "--clean",               # Hintergrund bereinigen
    "--clean-final",         # Finale Bereinigung
    "--optimize", "2",       # Level 2 Optimierung
    "--output-type", "pdf",  # PDF-Format
    "--language", "deu+eng", # Deutsch + Englisch
    "--sidecar",             # Sidecar-Textdatei
]
```

### Anpassungen

Du kannst die Parameter in `app/ocr_processor.py` oder via Environment Variables ändern.

## Logging

Logs werden nach stdout/stderr ausgegeben. Bei launchd werden sie in:
- `/tmp/ocr-watcher.log` (Info/Debug)
- `/tmp/ocr-watcher.error.log` (Errors)

Log-Level anpassen:

```bash
export LOG_LEVEL=DEBUG
python watcher_service.py
```

## Troubleshooting

### "ocrmypdf not found"

```bash
# Installiere OCRmyPDF
brew install ocrmypdf

# Finde Pfad
which ocrmypdf
# -> /opt/homebrew/bin/ocrmypdf

# Setze in .env
OCRMYPDF_PATH=/opt/homebrew/bin/ocrmypdf
```

### "tag command not found" (Warning)

Der Service verwendet einen Fallback mit `xattr`. Für bessere Tag-Unterstützung:

```bash
brew install tag
```

### Inbox-Ordner existiert nicht

```bash
mkdir -p /Volumes/DataEX/inbox
```

### Service läuft nicht

```bash
# Prüfe Logs
tail -f /tmp/ocr-watcher.log
tail -f /tmp/ocr-watcher.error.log

# Teste manuell
python watcher_service.py
```

## Entwicklung

### Projektstruktur

```
my-fastapi-ocr/
├── app/
│   ├── ocr_processor.py    # OCRmyPDF Wrapper
│   ├── file_mover.py       # Datei-Management + macOS Tags
│   ├── folder_watcher.py   # Watchdog-basierter Watcher
│   └── ...
├── watcher_service.py      # Standalone Service
├── config/
│   └── watcher.yaml        # YAML-Konfiguration
└── .env.watcher            # Environment Template
```

### Tests

```bash
# Test mit einer einzelnen Datei
cp test.pdf /Volumes/DataEX/inbox/
# -> Logs beobachten

# Prüfe Ergebnis
ls -la /Volumes/DataEX/inbox/ocr/
ls -la /Volumes/DataEX/inbox/archive/
```

## Integration mit FastAPI

Der Watcher-Service läuft **unabhängig** von der FastAPI-App. Du kannst beide parallel laufen lassen:

**Terminal 1 (FastAPI)**:
```bash
uvicorn app.main:app --reload
```

**Terminal 2 (Watcher)**:
```bash
python watcher_service.py
```

Oder beide als Services mit launchd/systemd.
