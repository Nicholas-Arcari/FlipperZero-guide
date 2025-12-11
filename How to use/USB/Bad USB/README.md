# **• BadUSB**

Sistema di automazione basato su script HID che permette al FlipperZero di comportarsi come una tastiera o mouse USB, eseguendo comandi su diversi sistemi operativi.

---

## Funzionalità:

* Emulazione completa tastiera HID.
* Supporto a payload complessi con ritardi, combinazioni e script multi-step.
* Compatibile con sistemi Windows, macOS, Linux, ChromeOS, Android, iOS (limitato).
* Inclusi payload dimostrativi e PoC didattici.

---

## Contenuto:

* **Demos:** android, chromeos, gnome, ios, macos, windows
* **CVE-2024-1086 Linux / wget** – dimostrazioni educative dell’exploit.
* **Install QFlipper** – installatore automatico (gnome/macos/windows).
* **Kiosk Evasion Bruteforce** – tentativi di uscita da modalità kiosk.
* **Rickroll** – apertura browser e avvio meme.
* **RogueMaster Code & Support** – link e tool correlati.
* **Test Mouse** – movimenti HID di test.
* **WiFi Stealer ORG** – demo educativa per recupero profili salvati.

---

### • Demos

Dimostrazioni per diversi sistemi operativi: Android, ChromeOS, GNOME, iOS, macOS, Windows.

Funzionalità ampliate:

- Script pronti per mostrare capacità HID.
- Apertura automatica terminali, browser e tool di sistema.
- Ideali per apprendere la logica dei payload.

Esempio pratico:

Eseguire demo_windows → apre PowerShell e mostra informazioni di sistema.

### • CVE‑2024‑1086 Linux / wget

Dimostrazioni educative dell’exploit CVE‑2024‑1086 su Linux.

Funzionalità ampliate:

- Versione standard e versione wget per download payload.
- Test di sicurezza e valutazioni didattiche.

Esempio pratico:

Eseguire script su distro vulnerabile → verifica risposta del kernel.

### • Install QFlipper

Installatori automatici per GNOME, macOS e Windows tramite script HID.

Funzionalità ampliate:

- Download automatico del pacchetto.
- Apertura finestre e conferme installazione.
- Nessun intervento manuale richiesto.

Esempio pratico:

Eseguire install_qflipper_windows → scarica e installa QFlipper in autonomia.

### • Kiosk Evasion Bruteforce

Script che tenta automaticamente combinazioni per uscire dalla modalità kiosk.

Funzionalità ampliate:

- Sequenze multi‑OS.
- Test di robustezza sistemi kiosk.

Esempio pratico:

Connettere Flipper su un kiosk → avvio script → verifica se alcune combinazioni riescono a sbloccare input.

### • Rickroll

Script comico che apre il browser e riproduce "Never Gonna Give You Up".

Funzionalità ampliate:

- Compatibile con più browser.
- Sequenza affidabile anche con ritardi.

Esempio pratico:

Lanciarlo su Windows → apre Chrome → avvia il video.

### • RogueMaster Code & Support

Materiale informativo e link utili relativi al firmware RogueMaster.

Funzionalità ampliate:

- Collegamenti a repository.
- Note aggiornamenti e strumenti.

Esempio pratico:

Aprire file di supporto → seguire istruzioni per aggiornare firmware.

### • Test Mouse

Script HID che muove il mouse automaticamente.

Funzionalità ampliate:

- Movimenti lineari, circolari o casuali.
- Test per verificare input HID su PC.

Esempio pratico:

Avviare lo script → il puntatore si muove → utile per debugging.

### • WiFi Stealer ORG

Demo educativa che esegue comandi per recuperare le password Wi‑Fi salvate.

Funzionalità ampliate:

- Esecuzione comandi di estrazione su OS supportati.
- Salvataggio output.

Esempio pratico:

Eseguirlo su Windows → apre Terminale → mostra profili Wi‑Fi memorizzati.