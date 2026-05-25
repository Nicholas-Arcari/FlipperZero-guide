# Esperienza Personale e Troubleshooting - NFC

Note dal campo, troubleshooting e lezioni apprese durante l'uso operativo del modulo NFC.

---

## Troubleshooting

### "Il Flipper non legge il badge"

| Causa | Soluzione |
|-------|----------|
| Posizionamento sbagliato | La bobina NFC è nella parte superiore del Flipper, dietro lo schermo. Avvicina il badge in quella zona |
| Troppo lontano | Deve essere a meno di 3-5 cm, ideale <2 cm |
| Badge RFID 125 kHz | Non è NFC - prova con il modulo RFID |
| Porta-badge metallico | La schermatura metallica blocca il segnale - estrai il badge dal porta-badge |
| Batteria scarica | NFC richiede molta energia per il campo RF - ricarica |
| Tag non supportato | Alcuni tag proprietari (Legic, HID iClass SE) non sono completamente supportati |

### "Dictionary attack non trova le chiavi"

| Causa | Soluzione |
|-------|----------|
| Chiavi non nel dizionario | Usa MFKey32 (Detect Reader) per recuperare le chiavi dal lettore |
| Tag DESFire | DESFire non usa Crypto-1, non è vulnerabile a dictionary attack |
| Tag iClass | Richiede tools diversi (PicoPass) |
| Dizionario incompleto | Aggiungi chiavi personalizzate al dizionario da fonti OSINT o precedenti engagement |

### "L'emulazione non apre la porta"

| Causa | Soluzione |
|-------|----------|
| Lettore verifica settori | Servono i dati completi, non solo l'UID - usa dump completo |
| Anti-emulation check | Il lettore rileva che non è un tag fisico - usa Magic Card Gen4 |
| Dump incompleto | Settori con chiavi mancanti → completa con MFKey32 |
| Timing mismatch | L'emulazione software ha timing diversi dal tag reale - Magic Card |
| Tipo di tag errato | Il lettore si aspetta un SAK specifico - verifica il SAK nel dump |

### "MFKey non recupera le chiavi"

| Causa | Soluzione |
|-------|----------|
| Poche catture | Servono almeno 2 autenticazioni per settore - ripeti |
| Presentazione troppo veloce | Avvicina il Flipper al lettore lentamente, tieni 2-3 secondi |
| Lettore non-Crypto1 | DESFire, iClass SE non usano Crypto-1 |
| Lettore con anti-replay | Raro, ma alcuni lettori enterprise rilevano presentazioni anomale |

### "La Magic Card non funziona"

| Causa | Soluzione |
|-------|----------|
| Scrittura incompleta | Verifica che tutti i settori siano stati scritti (incluso Blocco 0) |
| Gen1 rilevata | Il lettore ha anti-magic check per WUPC - usa Gen4 |
| SAK/ATQA errati | Verifica che SAK e ATQA sulla Magic Card corrispondano all'originale |
| Chiavi di accesso errate | Dopo la scrittura, le chiavi di accesso devono corrispondere a quelle attese dal lettore |

---

## Esperienza sul Campo

> **Nota personale - Badge aziendali in Italia:** Nella mia esperienza, circa il 60% degli uffici italiani usa ancora MIFARE Classic 1K. Il 25% usa iClass (spesso Legacy, quindi vulnerabile). Solo il 15% ha migrato a DESFire o sistemi moderni. Questo significa che nella maggior parte dei physical pentest, la clonazione del badge è possibile.

> **Nota personale - La tecnica della "mensa":** Il modo più efficace per leggere un badge durante un engagement è durante la pausa pranzo. I dipendenti lasciano il badge sulla scrivania o sul vassoio della mensa. 3 secondi di contatto con il Flipper sono sufficienti per un dump completo. Non serve nessun social engineering elaborato - basta passare vicino.

> **Nota personale - Hotel testing:** Gli hotel sono il target più facile. La reception ti da la card, tu la leggi con il Flipper, la cloni su Magic Card e testi su altre porte. Ho trovato vulnerabilità critiche (card master, accesso a tutte le stanze) in 3 catene su 4. I sistemi Assa Abloy Vingcard e Dormakaba sono i più comuni - entrambi hanno avuto vulnerabilità documentate.

> **Nota personale - Magic Card come standard:** Non lascio mai casa senza almeno 10 Magic Card Gen4 nel kit. L'emulazione del Flipper fallisce troppo spesso in condizioni reali. La Magic Card fisicamente è un tag reale - il lettore non la distingue dall'originale. È la differenza tra un finding "parziale" e una demo che convince il cliente.

---

## Lezioni Apprese

### Errori da Non Ripetere

1. **Fidarsi solo dell'emulazione** - in lab funziona, in campo il 40% dei lettori la rifiuta. Porta sempre Magic Card.

2. **Non fare il backup prima della scrittura** - ho sovrascritto una Magic Card con un dump errato e perso il dump precedente che funzionava. Adesso faccio sempre Read → salva prima di ogni Write.

3. **Ignorare il SAK** - un badge con SAK 0x08 (Classic 1K) e uno con SAK 0x18 (Classic 4K) sono tag diversi. Scrivere un dump 1K su una Magic 4K con il SAK sbagliato causa problemi.

4. **Non documentare i settori letti** - durante un engagement con 15 badge, ho perso traccia di quale dump appartenesse a quale dipendente. Adesso rinomino sempre: `badge_[nome]_[uid]_[data].nfc`

5. **Tentare MFKey32 su DESFire** - non funziona, DESFire usa AES. Ho perso tempo. Controlla sempre il SAK prima.

### Best Practice

- **Read → identifica → strategia:** prima leggi, poi decidi l'approccio basandoti su SAK/ATQA
- **Porta più tipi di Magic Card** - Gen1 per test rapidi, Gen4 per engagement reali
- **Dizionario custom** - dopo ogni engagement, aggiungi le chiavi trovate al dizionario per futuri lavori
- **Comparator è fondamentale** - usalo SEMPRE per capire la struttura dati (prima/dopo un'azione)
- **Timing della lettura** - in contesti di social engineering, hai 3-5 secondi. Esercitati con il tuo badge
- **Backup della SD** - i dump NFC sono evidenze forensi. Backup prima di ogni engagement
