# Contributing - Guida per Contribuire

Grazie per l'interesse nel contribuire a questo progetto. Questa guida descrive come partecipare in modo efficace.

---

## Come Contribuire

### Segnalare Errori o Problemi
1. Apri una **Issue** su GitHub
2. Descrivi il problema con dettaglio sufficiente (file, sezione, cosa è sbagliato)
3. Se possibile, suggerisci la correzione

### Aggiungere Contenuto
1. Fai un **fork** del repository
2. Crea un **branch** con nome descrittivo (`add-subghz-scenario-parking`, `fix-nfc-typo`)
3. Fai le modifiche seguendo le linee guida sotto
4. Apri una **Pull Request** con descrizione di cosa hai cambiato e perche'

---

## Linee Guida di Stile

### Lingua
- **Italiano** per tutto il contenuto principale
- Termini tecnici in inglese dove non esiste un equivalente italiano consolidato (es: "replay attack", non "attacco di riproduzione")
- Accenti con apostrofo (`e'`, `piu'`, `perche'`) per compatibilità con tutti gli editor

### Struttura dei File
Ogni modulo principale segue la struttura a 8 file:

```
Modulo/
├── README.md                    ← Indice breve (~100-150 righe)
├── 01-Fondamenti-Tecnici.md     ← Come funziona il protocollo
├── 02-Hardware-e-Limiti.md      ← Specifiche e limiti reali
├── 03-Protocolli.md             ← Deep dive protocolli
├── 04-Guida-Operativa.md        ← Step-by-step per ogni tool
├── 05-Scenari-Reali.md          ← Scenari di pentest dal campo
├── 06-Attacchi-e-Difese.md      ← Vettori di attacco + contromisure
├── 07-Aspetti-Legali.md         ← Normativa IT/EU
└── 08-Esperienza-Personale.md   ← Note dal campo, troubleshooting
```

### Formattazione
- Tabelle markdown per dati strutturati
- Code block con linguaggio specificato dove applicabile
- `> Nota personale:` per esperienze dirette (blockquote)
- Evitare heading singoli (non un H2 con una sola riga sotto)
- Cross-reference ad altri moduli dove utile

### Scenari Reali
Ogni scenario deve includere:
1. **Contesto** - tipo di engagement, ambiente
2. **Obiettivo** - cosa si vuole testare
3. **Procedura** - step-by-step dettagliato
4. **Risultato/Finding** - cosa si è trovato
5. **Impatto** - classificazione CVSS o qualitativa
6. **Remediation** - raccomandazione per il cliente

### Payload BadUSB
I payload devono:
- Avere un header con: descrizione, target OS, prerequisiti, layout tastiera
- Essere commentati con `REM` per ogni blocco logico
- Includere `DELAY` realistici
- Specificare se richiedono privilegi elevati
- NON contenere IP/URL hardcoded dell'attaccante (usare placeholder `ATTACKER_IP`)

---

## Cosa NON Fare

- Non aggiungere file binari (firmware, eseguibili) - solo link alle release ufficiali
- Non includere dati reali di dispositivi altrui (UID, chiavi, credenziali)
- Non rimuovere contenuto esistente senza discussione in una Issue
- Non aggiungere contenuto in inglese (a meno che non sia codice o comandi)
- Non aggiungere watermark, loghi o branding personale

---

## Aree Dove Servono Contributi

- Nuovi scenari di pentest reali (con contesto anonimizzato)
- Payload BadUSB testati per diversi OS e configurazioni
- Correzioni tecniche (protocolli, specifiche, comandi)
- Traduzioni (quando/se si aprirà la sezione inglese)
- Miglioramenti ai diagrammi Mermaid
- Nuove entry nel glossario

---

## Licenza

Contribuendo accetti che il tuo lavoro sia distribuito sotto la stessa licenza del repository ([MIT License](LICENSE)).
