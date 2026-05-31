## Troubleshooting e Limiti

### "Il payload non digita nulla"

- Verifica che il Flipper sia riconosciuto come tastiera USB (icona tastiera sul PC)
- Controlla il cavo USB-C (non tutti supportano dati)
- Verifica che il layout sia corretto nel menu BadUSB

### "I caratteri speciali sono sbagliati"

- Il layout del Flipper non corrisponde al layout del PC target
- Soluzione 1: cambia layout nel menu BadUSB
- Soluzione 2: usa ALTCHAR/ALTSTRING per inserire caratteri via Alt code (indipendente dal layout)
- Soluzione 3: usa codifica Base64 per evitare caratteri speciali

### "Il payload è troppo lento / troppo veloce"

- Regola DEFAULT_DELAY
- Usa DELAY specifici prima di comandi critici (apertura finestra, UAC, ecc.)
- Su macchine lente, usa delay di 1000-2000ms dopo GUI r

### "PowerShell viene bloccato"

- L'EDR ha rilevato il comando → usa tecniche di evasione
- Prova con cmd.exe invece di PowerShell
- Usa LOLBins (mshta, certutil, bitsadmin)
- Codifica il payload in Base64

### "Il PC ha USB disabilitato"

- Verifica se è un blocco hardware (BIOS) o software (GPO)
- Se software: potrebbe essere bypassabile (ma fuori scope del BadUSB)
- Se hardware: BadUSB non funzionerà - serve un approccio diverso

---

## Esperienza Personale

> **Nota personale - Il layout italiano:** Il problema più ricorrente in Italia è il layout della tastiera. Ho perso engagement interi perchè il payload aveva @ nella posizione sbagliata. Ora testo SEMPRE su una VM con layout IT prima di ogni engagement. La combinazione AltGr+chiocciola su layout IT è diversa da Shift+2 su layout US. Un singolo carattere sbagliato e il payload fallisce completamente.

> **Nota personale - Timing dei delay:** Il delay dopo GUI r (Win+R) è il più critico. Su un PC nuovo con SSD, 300ms bastano. Su un PC aziendale vecchio con disco meccanico e antivirus pesante, servono anche 2000ms. Io uso 500ms come default e aggiusto in base al target. Meglio aspettare mezzo secondo in più che perdere l'intero payload.

> **Nota personale - Drop attack efficace:** La tecnica più efficace che ho usato è il "coffee break attack": identifico un dipendente che va al bar/macchinetta del caffè lasciando il PC sbloccato, mi avvicino alla scrivania, collego il Flipper, eseguo il payload (8 secondi), scollego e mi allontano. Tempo totale di esposizione: meno di 15 secondi. Funziona sorprendentemente spesso perchè la gente non blocca il PC.

> **Nota personale - Kiosk escape nei totem:** Ho testato kiosk in 6 diversi contesti (aeroporto, hotel, ospedale, centro commerciale, banca, ristorante). 4 su 6 erano vulnerabili a semplici combinazioni di tasti (Ctrl+L sul browser, Alt+F4, F11). Il Flipper con lo script di bruteforce trova l'escape in meno di 30 secondi. Finding sempre apprezzato nei report perchè i kiosk spesso hanno accesso alla rete interna.

> **Nota personale - Evasione EDR:** CrowdStrike e SentinelOne bloccano la maggior parte dei payload PowerShell diretti. La tecnica che funziona meglio per me è usare certutil per scaricare un eseguibile legittimo (firmato) che a sua volta carica il payload via DLL sideloading. Il comando BadUSB iniziale appare innocuo e l'EDR non lo blocca. Richiede più preparazione ma ha un tasso di successo molto più alto.
