## 8. Troubleshooting

### 8.1 Problemi di Flash del Firmware

**Problema: "Failed to connect to ESP32: No serial data received"**

Cause possibili:
- Il dispositivo non e in modalita boot
- Cavo USB difettoso o solo di ricarica (senza linee dati)
- Driver USB non installati
- Porta seriale occupata da altro processo

Soluzioni:
1. Verificare la sequenza boot: tenere BOOT, premere RESET, rilasciare BOOT
2. Provare un altro cavo USB (possibilmente corto, < 1m)
3. Verificare driver: `dmesg | tail -20` su Linux dopo collegamento
4. Chiudere programmi che potrebbero usare la porta seriale (screen, minicom,
   Arduino IDE, altro terminale seriale)
5. Su Linux: `fuser /dev/ttyACM0` per identificare processi che usano la porta

**Problema: Flash completato ma il firmware non funziona**

Cause possibili:
- Firmware sbagliato per il modello di ESP32
- Offset di flash errati
- Flash corrotto da interruzione durante la scrittura

Soluzioni:
1. Verificare il modello esatto del chip: `esptool.py chip_id`
2. Cancellare completamente la flash: `esptool.py erase_flash`
3. Riflashare con il firmware corretto per il proprio modello
4. Verificare gli offset (diversi fra ESP32, ESP32-S2, ESP32-S3)

**Problema: "A fatal error occurred: Chip is esp32s2 not esp32"**

Causa: si sta specificando il chip sbagliato nel comando esptool.

Soluzione: usare `--chip auto` per il rilevamento automatico, o specificare
il chip corretto:
```bash
esptool.py --chip auto --port /dev/ttyACM0 chip_id
```

**Problema: Flash lentissimo o si blocca**

Cause possibili:
- Baud rate troppo alto per la connessione USB
- Hub USB che degrada il segnale
- Interferenze EMI sul cavo

Soluzioni:
1. Ridurre il baud rate: usare `--baud 115200` invece di 921600
2. Collegare direttamente alla porta USB del computer (no hub)
3. Usare un cavo USB schermato e corto

### 8.2 Problemi di Comunicazione Seriale Flipper-ESP32

**Problema: l'app WiFi Marauder mostra "Connecting..." all'infinito**

Cause possibili:
- Devboard non collegato correttamente ai pin GPIO
- Firmware non flashato sull'ESP32
- Baud rate mismatch tra Flipper e firmware Marauder
- Pin UART non allineati

Soluzioni:
1. Spegnere il Flipper, scollegare il devboard, ricollegare con fermezza,
   riaccendere
2. Verificare che il firmware Marauder sia effettivamente installato sull'ESP32
   (collegare l'ESP32 al PC e aprire un terminale seriale a 115200 baud --
   dovrebbe mostrare il prompt Marauder)
3. Verificare che il firmware del Flipper sia aggiornato
4. Provare a resettare l'ESP32 (pulsante RESET sul devboard)

**Problema: output illeggibile o caratteri corrotti sul Flipper**

Causa: baud rate mismatch.

Soluzione: il firmware Marauder usa 115200 baud di default. L'app sul Flipper
deve essere configurata sullo stesso baud rate. Se si e modificato il baud rate
nel firmware Marauder, adeguare l'app.

**Problema: comandi inviati dal Flipper non producono risposta**

Cause possibili:
- TX del Flipper non collegato a RX dell'ESP32 (o viceversa)
- ESP32 in stato di errore o crash

Soluzioni:
1. Verificare il mapping dei pin (TX <-> RX devono essere incrociati)
2. Reset dell'ESP32 (pulsante RESET o power cycle)
3. Se il problema persiste, riflashare il firmware

### 8.3 Problemi Durante l'Uso

**Problema: scansione non trova reti che si sa essere presenti**

Cause possibili:
- Antenna ESP32 troppo lontana dal target
- Canale non coperto dalla scansione
- Interferenza radio

Soluzioni:
1. Avvicinarsi al target
2. Verificare che la scansione copra tutti i canali (1-13)
3. In ambienti con forte interferenza (microonde, Bluetooth, ecc.),
   spostarsi o attendere

**Problema: cattura handshake/PMKID vuota o incompleta**

Cause possibili:
- AP non supporta PMKID (per sniffpmkid)
- Client non si e riconnesso dopo il deauth
- Sniffer non era attivo al momento del handshake
- Canale errato

Soluzioni:
1. Per PMKID: non tutti gli AP lo supportano, passare alla cattura handshake
2. Per handshake: verificare che lo sniffer fosse attivo PRIMA del deauth
3. Verificare il canale dello sniffer corrisponda al canale dell'AP target
4. Ripetere il tentativo con client diverso (se disponibile)
5. Avvicinarsi sia all'AP che al client

**Problema: Evil Portal non mostra la pagina di login**

Cause possibili:
- Template HTML non caricato correttamente sulla SD card
- File HTML troppo grande per la memoria ESP32
- Il device della vittima usa DNS-over-HTTPS (DoH) che bypassa il DNS spoofing

Soluzioni:
1. Verificare il percorso del file HTML sulla SD card
2. Ridurre la dimensione del template (rimuovere immagini pesanti, minimizzare CSS)
3. DoH: su device con DoH abilitato (Firefox, Chrome recente) il DNS spoofing non
   funziona. Non c'e soluzione diretta -- e una limitazione dell'attacco.

**Problema: batteria del Flipper si scarica rapidamente**

Causa: il devboard ESP32 consuma molta corrente, specialmente durante TX attivo.

Soluzioni:
1. Usare un powerbank collegato al Flipper via USB
2. Limitare il tempo di operazione attiva
3. Spegnere il devboard quando non in uso
4. Per operazioni lunghe (Evil Portal, wardriving), pianificare l'autonomia
   (la batteria del Flipper con devboard attivo dura circa 2-4 ore)

**Problema: file .pcap corrotto o non apribile in Wireshark**

Cause possibili:
- Cattura interrotta bruscamente (spegnimento Flipper o disconnessione devboard)
- SD card piena
- Corruzione del filesystem della SD

Soluzioni:
1. Fermare sempre la cattura con `stopscan` prima di scollegare il devboard
2. Verificare spazio libero sulla SD card prima di iniziare
3. Usare una SD card di buona qualita (classe 10 o superiore)
4. Se il file e parzialmente corrotto, provare: `pcapfix capture.pcap`

> Nota personale: il 50% dei problemi che ho avuto con Marauder erano legati
> al cavo USB durante il flash. Un cavo di ricarica senza linee dati sembra
> funzionare (il LED si accende) ma non viene riconosciuto dal PC. Ho perso
> ore a cercare problemi nel software quando il problema era un cavo da 2 euro.
> Ora tengo sempre un cavo USB marcato "DATI" nello zaino del pentesting.

---

## 9. Riferimenti e Risorse

### Repository e Documentazione

- **Marauder Firmware**: https://github.com/justcallmekoko/ESP32Marauder
- **Wiki Marauder**: https://github.com/justcallmekoko/ESP32Marauder/wiki
- **Flasher Windows**: https://github.com/UberGuidoZ/Flipper/tree/main/Wifi_DevBoard/FZ_Marauder_Flasher
- **Flasher Linux/macOS**: https://github.com/SkeletonMan03/FZEasyMarauderFlash
- **Flipper Zero Docs**: https://docs.flipper.net/

### Strumenti Complementari per il Crack

- **hashcat**: https://hashcat.net/hashcat/
- **aircrack-ng**: https://www.aircrack-ng.org/
- **hcxtools**: https://github.com/ZerBea/hcxtools
- **Wireshark**: https://www.wireshark.org/

### Wordlist e Risorse per il Crack

- **rockyou.txt**: incluso in Kali Linux, contiene ~14 milioni di password
- **SecLists**: https://github.com/danielmiessler/SecLists
- **CrackStation**: https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm

### Formazione e Certificazioni

Per chi vuole approfondire il wireless pentesting a livello professionale:
- **OSWP** (Offensive Security Wireless Professional) -- certificazione
  specifica per wireless pentesting
- **CEH** (Certified Ethical Hacker) -- copre wireless security fra i vari
  moduli
- **IEEE 802.11-2020** -- la specifica completa del protocollo WiFi
  (documento di riferimento, non e un corso)

### Standard e Normativa

- **IEEE 802.11-2020**: specifica completa del protocollo WiFi
- **IEEE 802.11w-2009**: Protected Management Frames
- **IEEE 802.11i-2004**: security enhancements (WPA2)
- **WPA3 Specification**: https://www.wi-fi.org/security
- **GDPR**: Regolamento UE 2016/679
- **Codice Penale Italiano**: artt. 615-ter, 617-quater, 617-quinquies, 640-ter

---

## Note Finali

WiFi Marauder con Flipper Zero e uno strumento potente ma con limitazioni
intrinseche. L'ESP32 non e un sostituto di un laptop con scheda WiFi
dedicata (Alfa AWUS036ACH, ASUS USB-AC68, ecc.) per penetration testing
professionale. I suoi punti di forza sono:

- **Discrezione**: entra in tasca, nessuno lo nota
- **Velocita di deploy**: operativo in secondi
- **Portabilita**: batteria integrata, nessun laptop necessario
- **Ricognizione**: eccellente per la fase iniziale di un engagement

I suoi limiti:

- **Raggio**: antenna piccola, portata limitata
- **Solo 2.4 GHz**: non vede le reti 5 GHz
- **Potenza di calcolo**: l'ESP32 non puo fare crack (quello avviene offline)
- **Storage**: SD card limitata per catture lunghe
- **Single-band**: non puo fare channel hopping veloce come schede multi-antenna

Il pentester esperto usa il Flipper come strumento complementare nel proprio
arsenale, non come strumento unico. E lo strumento perfetto per la ricognizione
iniziale, il PMKID grab veloce, e scenari di social engineering con Evil Portal
dove la discrezione e fondamentale.

> Nota personale: dopo 3 anni di utilizzo in engagement reali, la mia regola
> e semplice: Flipper per la ricognizione e il primo contatto, laptop per tutto
> il resto. Il Flipper mi dice cosa c'e e come e configurato. Il laptop fa il
> lavoro pesante. Insieme, sono una combinazione formidabile. Nessuno dei due
> da solo e sufficiente per un engagement wireless serio.

---

*Questa guida e mantenuta a scopo educativo e di formazione professionale
nel campo della cybersecurity. Ogni tecnica deve essere applicata nel
rispetto della legge e dell'etica professionale.*
