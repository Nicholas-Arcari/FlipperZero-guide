# Fondamenti Tecnici - RFID 125 kHz

## Che cos'è l'RFID 125 kHz

RFID (Radio-Frequency Identification) a 125 kHz è una tecnologia di identificazione a radiofrequenza che opera nella banda LF (Low Frequency). È la forma più antica e semplice di RFID ancora in uso massivo, nata negli anni '80 e diffusissima in:

- **Controllo accessi** - badge condominio, uffici, parcheggi, palestre
- **Identificazione animale** - microchip sottocutanei (ISO 11784/11785)
- **Controllo presenze** - timbrature dipendenti
- **Sistemi industriali** - identificazione asset, logistica legacy
- **Automazione** - macchinette del caffe', distributori automatici, armadietti
- **Hotel e strutture ricettive** - chiavi camera (spesso ormai migrate a NFC)

La frequenza 125 kHz (e la sua variante a 134.2 kHz usata in FDX-B) si colloca nella banda LF, molto al di sotto delle frequenze NFC (13.56 MHz) e Sub-GHz (300-900 MHz). Questo ha implicazioni fisiche precise.

---

## Come Funziona a Livello Fisico

Il principio di funzionamento è l'**accoppiamento induttivo in campo vicino** (near-field inductive coupling). Ecco cosa succede quando avvicini un badge a un lettore:

1. **Il lettore genera un campo magnetico oscillante a 125 kHz** tramite la sua antenna (una bobina). Questo campo trasporta energia, non dati.

2. **L'antenna del tag (una bobina stampata sul circuito del badge)** si trova immersa nel campo magnetico. Per la legge di Faraday, una variazione di flusso magnetico attraverso una bobina induce una forza elettromotrice (tensione).

3. **La tensione indotta alimenta il chip del tag**. Questo è il motivo per cui i tag passivi non hanno batteria: ricevono tutta l'energia dal campo del lettore. Un condensatore interno accumula la carica.

4. **Una volta alimentato, il chip inizia a trasmettere il suo ID** modulando il carico sull'antenna (load modulation). In pratica, il chip connette e disconnette un carico resistivo in parallelo alla sua bobina, variando l'impedenza vista dal lettore.

5. **Il lettore rileva queste variazioni di impedenza** come piccole fluttuazioni nell'ampiezza o nella frequenza del campo che sta generando. Demodula queste variazioni e ricostruisce la sequenza di bit dell'ID.

6. **Il lettore confronta l'ID ricevuto** con il suo database e decide se aprire o meno.

Questo processo avviene in pochi millisecondi e si ripete continuamente finchè il tag è nel campo.

> **Nota personale:** Il concetto chiave da capire è che il tag NON trasmette nulla in senso stretto. Si limita a modificare il carico visto dall'antenna del lettore. È come se qualcuno premesse e rilasciasse il freno di una ruota che stai facendo girare - sentiresti la variazione di resistenza. Questa è la "trasmissione" di un tag RFID passivo.

---

## Tag Passivi vs Tag Attivi

**Tag Passivi (la stragrande maggioranza a 125 kHz):**
- Nessuna batteria interna
- Alimentati esclusivamente dal campo del lettore
- Portata tipica: 2-15 cm (dipende dall'antenna del lettore)
- Vita illimitata (finchè il chip non si danneggia fisicamente)
- Costo: 0.05-0.50 EUR per tag
- Dimensioni: possono essere minuscoli (2mm per gli impianti animali)
- Tutti i badge condominio, carte accesso e microchip animali sono passivi

**Tag Attivi:**
- Batteria interna (litio, durata 3-10 anni)
- Portata: fino a 100 metri
- Costo: 5-50 EUR per tag
- Usati in logistica industriale, tracking veicoli, telepedaggio
- NON operano a 125 kHz (usano UHF 860-960 MHz o 2.4 GHz)
- Il Flipper Zero NON gestisce tag attivi

Per il 99.9% del lavoro con il Flipper Zero su RFID 125 kHz, parliamo esclusivamente di tag passivi.

---

## Modulazione del Segnale

I tag RFID 125 kHz usano diverse tecniche di modulazione per codificare i bit. Capire la modulazione è fondamentale per il debug e per capire perchè certi tag non vengono letti.

**ASK (Amplitude Shift Keying):**
- La tecnica più comune a 125 kHz
- Il tag varia l'ampiezza del segnale riflesso
- Bit 1 = ampiezza alta, Bit 0 = ampiezza bassa (o viceversa)
- Usata da: EM4100, HID Prox, la maggior parte dei tag economici
- Semplice da demodulare ma sensibile al rumore ambientale
- Variante OOK (On-Off Keying): caso speciale di ASK dove il bit 0 = nessun segnale

**FSK (Frequency Shift Keying):**
- Il tag varia la frequenza della sottoportante
- Due frequenze distinte rappresentano 0 e 1
- Usata da: HID Prox (FSK2 a 50 kHz / 40 kHz), Indala
- Più robusta al rumore rispetto ad ASK
- FSK1: frequenze RF/8 e RF/5 (15.625 kHz e 25 kHz)
- FSK2: frequenze RF/8 e RF/10 (15.625 kHz e 12.5 kHz)

**PSK (Phase Shift Keying):**
- Il tag varia la fase del segnale
- Bit 1 = inversione di fase, Bit 0 = nessuna inversione (o viceversa)
- Usata da: alcuni tag industriali, AWID, Pyramid
- La più robusta al rumore ma la più complessa da demodulare
- PSK1: cambio di fase su transizione 0->1
- PSK2: cambio di fase su ogni bit 1
- PSK3: variante bidirezionale

---

## Codifica dei Dati (Line Coding)

Oltre alla modulazione RF, i dati vengono codificati con schemi specifici per garantire la sincronizzazione del clock tra lettore e tag:

**Manchester Encoding:**
- Lo standard più diffuso (usato da EM4100)
- Ogni bit è rappresentato da una transizione a metà periodo
- Bit 1 = transizione basso->alto
- Bit 0 = transizione alto->basso
- Vantaggio: il clock è embedded nel segnale, auto-sincronizzante
- Svantaggio: richiede il doppio della bandwidth (ogni bit occupa due periodi di clock)

**Biphase (FM0/FM1):**
- Usato da HID, FDX-B
- Transizione all'inizio di ogni periodo di bit
- Bit 0 o 1 = transizione aggiuntiva a metà periodo (dipende dalla variante)

**NRZ (Non-Return-to-Zero):**
- Il più semplice: livello alto = 1, livello basso = 0
- Nessuna transizione garantita - problemi di sincronizzazione su sequenze lunghe di 0 o 1
- Usato raramente da solo, spesso combinato con scrambling

**Differential Manchester:**
- Variante del Manchester dove la codifica dipende dalla transizione rispetto al bit precedente
- Più robusto alla polarità invertita

---

## Data Rate

La velocità di trasmissione dei tag 125 kHz è estremamente bassa:

- **EM4100:** RF/64 = ~1.95 kbps (125000 / 64)
- **HID Prox:** RF/50 = 2.5 kbps
- **FDX-B:** RF/32 = ~3.9 kbps
- **T5577:** configurabile, tipicamente RF/32 o RF/64

Per confronto, NFC opera a 106-848 kbps e il Wi-Fi a centinaia di Mbps. La bassa velocità non è un problema perchè un ID è lungo pochi byte - la trasmissione completa richiede pochi millisecondi.

> **Nota personale:** Il data rate basso ha un vantaggio pratico: i tag 125 kHz sono estremamente tolleranti al disallineamento e alla distanza. Puoi leggere un EM4100 anche con il Flipper non perfettamente centrato sull'antenna del tag, cosa molto più difficile con NFC a 13.56 MHz. Questo rende la clonazione "al volo" (social engineering, passaggio rapido) decisamente più fattibile.
