# Programmazione - EEPROM, Flashing e Memoria

Questa sezione raccoglie gli strumenti GPIO dedicati alla programmazione di chip, lettura/scrittura EEPROM e flashing di firmware su microcontroller compatibili.

---

### • Coffee EEPROM

Strumento per accedere alle EEPROM presenti in macchine da caffè (DeLonghi, Nespresso, ecc.) utilizzate per memorizzare contatori, configurazioni e parametri di calibrazione.

Funzionalità ampliate:

- Identificazione automatica chip (24Cxx, 93Cxx, ecc.).
- Lettura completa della memoria.
- Backup binario.
- Editing sicuro delle aree note (volumi, cicli decalcificazione).
- Protezione "Safe Zone" per evitare corruzione firmware.

Esempio pratico

Reset contatore decalcificazione:

- Collegare SDA/SCL.
- Effettuare dump completo → salvare backup.
- Modificare byte relativo al contatore.
- Scrivere solo il settore modificato.
- Riavviare macchina e verificare reset.

### • WHC SWIO Flasher

Flasher per moduli SWIO tramite GPIO.

Funzionalità ampliate:

- Lettura e scrittura firmware SWIO.
- Backup completo modulo.
- Verifica checksum post-flash.
- Compatibile con diversi microcontroller compatibili SWIO.

Esempio pratico

Aggiornamento firmware:

- Collegare SWIO → alimentare target.
- Caricare firmware → flash.
- Verificare checksum → test funzionalità.
