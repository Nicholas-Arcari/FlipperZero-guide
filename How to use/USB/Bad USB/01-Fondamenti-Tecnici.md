## Fondamenti Tecnici

### Che cos'è BadUSB

BadUSB sfrutta il fatto che i computer si fidano ciecamente dei dispositivi USB che si identificano come tastiere. Quando colleghi il Flipper Zero via USB e attivi BadUSB, il computer lo vede come una **tastiera USB HID** e accetta tutti i "tasti premuti" come input legittimo dell'utente.

Il Flipper esegue script pre-programmati che digitano comandi a velocità sovrumana - tipicamente centinaia di caratteri al secondo. In meno di 3 secondi può:
- Aprire un terminale/PowerShell
- Digitare ed eseguire comandi arbitrari
- Scaricare ed eseguire malware
- Exfiltrare dati
- Modificare configurazioni di sistema

### Come Funziona a Livello USB

1. Il Flipper si presenta al PC come dispositivo **USB HID Keyboard** (class 0x03, subclass 0x01, protocol 0x01)
2. Il driver HID generico del sistema operativo lo riconosce automaticamente - nessun driver aggiuntivo necessario
3. Lo stack USB negozia: VID/PID, endpoint, descriptor
4. Il Flipper invia **HID reports** contenenti keycodes (es. 0x04 = 'à, 0x28 = ENTER)
5. Il sistema operativo processa i keycodes come se un utente fisico stesse premendo i tasti
6. Nessun antivirus o EDR intercetta input da tastiera USB - è un canale trusted

### Perchè è Cosi' Efficace

- **Trust implicito:** i sistemi operativi si fidano delle tastiere USB - non c'è modo nativo di distinguere una tastiera reale da un Flipper
- **Velocità:** il Flipper digita più velocemente di qualsiasi umano - l'utente non ha tempo di reagire
- **Universalità:** funziona su Windows, macOS, Linux, ChromeOS, Android (OTG), e parzialmente su iOS
- **Nessun file su disco:** i comandi vengono digitati, non scaricati come file - difficile da rilevare per AV tradizionali
- **Pre-lock screen:** alcuni payload funzionano anche sul lock screen (es. USB HID su login)

> **Nota personale:** BadUSB è lo strumento di pentest fisico più potente del Flipper. In un engagement tipico, se riesco ad avere 5 secondi di accesso fisico a un PC sbloccato, posso installare una reverse shell persistente. La chiave è la preparazione del payload - deve essere perfetto al primo tentativo perchè non avrai una seconda chance.

---

