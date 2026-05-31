## Tool per Tool - Guida Operativa

### BadUSB (Principale)

**Procedura operativa:**

1. Prepara lo script (.txt) e mettilo in `/ext/badusb/` sulla SD card del Flipper
2. Apri Apps → USB → Bad USB
3. Seleziona lo script
4. Il Flipper mostra un'anteprima del payload
5. Collega il Flipper al PC target via USB-C
6. Premi il pulsante centrale per **avviare l'esecuzione**
7. Il Flipper digita i comandi in sequenza
8. Al termine, scollega il Flipper

**Impostazioni importanti:**
- **Keyboard Layout:** DEVE corrispondere al layout del sistema target (IT, US, UK, DE, ecc.)
- **USB VID/PID:** personalizzabile per evasione
- **Device Name:** personalizzabile (es. "Logitech Keyboard")

### Demos

Script dimostrativi per diversi OS che mostrano le capacità HID:
- **demo_windows** - apre PowerShell, mostra info di sistema
- **demo_macos** - apre Terminal, mostra info di sistema
- **demo_linux_gnome** - apre terminale GNOME
- **demo_android** - apre browser
- **demo_chromeos** - apre Crosh
- **demo_ios** - funzionalità limitata

### CVE-2024-1086 Linux / wget

Dimostrazioni educative dell'exploit CVE-2024-1086 (Linux kernel nf_tables use-after-free):

- Script che scarica ed esegue il PoC su distribuzioni vulnerabili
- **ATTENZIONE:** solo per studio su VM proprie, mai su sistemi in produzione
- La versione wget scarica il payload da un server remoto

### Kiosk Evasion Bruteforce

Script che tentano automaticamente combinazioni di tasti per uscire da modalità kiosk:

**Combinazioni testate:**
```
ALT F4          - chiudi applicazione
CTRL W          - chiudi tab/finestra
ALT TAB         - switch applicazione
CTRL-ALT DELETE - task manager (Windows)
F11             - toggle fullscreen
CTRL ESC        - Start menu
GUI D           - mostra desktop
CTRL-SHIFT ESC  - task manager diretto
ALT SPACE       - menu finestra
F5              - refresh
CTRL L          - barra indirizzi (browser kiosk)
CTRL T          - nuova tab (browser kiosk)
CTRL-SHIFT T    - riapri tab chiusa
CTRL N          - nuova finestra
```

**Uso nel pentest:** testare la robustezza di terminali kiosk (ATM, totem informativi, check-in, terminali POS).

> **Nota personale:** L'evasione kiosk è sorprendentemente efficace. Ho testato kiosk in aeroporti, hotel e centri commerciali. Circa il 40% permette di uscire con semplici combinazioni di tasti. I più vulnerabili sono quelli basati su Chrome in modalità kiosk - Ctrl+L per accedere alla barra URL e poi navigare liberamente. Il Flipper rende il test automatico e veloce.

### WiFi Stealer ORG

Script educativo che estrae le password WiFi salvate sul sistema:

**Windows:**
```
netsh wlan show profiles
netsh wlan show profile name="SSID" key=clear
```

**macOS:**
```
security find-generic-password -wa "SSID"
```

**Linux:**
```
cat /etc/NetworkManager/system-connections/*.nmconnection | grep psk=
```

Il payload tipicamente salva l'output in un file temporaneo o lo invia a un server remoto.

### Test Mouse

Script HID che testa l'emulazione mouse:
- Movimenti lineari, circolari o casuali
- Click sinistro/destro
- Scroll
- Utile per verificare che l'emulazione HID funzioni correttamente

---


---

# Script e Payload - Riferimento Completo

Per la guida completa alla creazione di payload DuckyScript, inclusi template per Windows, macOS, Linux, ChromeOS e Android, vedi: [Script/README.md](Script/README.md)
