# iButton

Strumenti e funzionalità dedicate alla lettura, emulazione, conversione e fuzzing dei iButton / Dallas Keys tramite Flipper Zero.

Il modulo iButton permette di:

- leggere chiavi fisiche (es. DS1990A / iButton 1-Wire)
- emulare una chiave iButton salvata
- convertire formati non standard
- testare e analizzare protocolli compatibili tramite fuzzer dedicati

---

## • iButton

Funzione principale dedicata alla lettura, salvataggio ed emulazione di chiavi iButton.

Funzionalità ampliate:

- Lettura chiavi Dallas/Maxim DS1990A / RW1990 / TM1990 / Cyfral / Metakom.
- Salvataggio in formato `.ibtn` con ID completo.
- Emulazione diretta tramite contatto fisico.
- Libreria interna per gestire più chiavi.
- Possibilità di clonare chiavi compatibili (solo per uso lecito / personale).

Esempio pratico:

Emulare una chiave DS1990A del tuo citofono:

1. Apri iButton → Read.
2. Tocca la chiave originale sul pad iButton del Flipper.
3. Salva il dump.
4. Vai su iButton → Emulate e seleziona la chiave.
5. Tocca il lettore del citofono → funziona come la chiave originale.

Quando usarlo:

- Accesso a cancelli, citofoni e sistemi basati su 1-Wire.
- Backup di chiavi personali.
- Test e verifica compatibilità con sistemi esistenti.

Dove usarlo:

- Sistemi condominiali.
- Serrature con iButton.
- Controller industriali che adottano chiavi Dallas.

## • iButton Converter

Strumento per convertire chiavi non standard o protocolli particolari in formati compatibili con la struttura del Flipper.

Funzionalità ampliate:

- Conversione tra formati Cyfral ↔ Dallas, Metakom ↔ Dallas, quando possibile.
- Normalizzazione ID per uso in emulazione.
- Correzione automatica checksum.
- Supporto a layout di memoria di chiavi compatibili.

Esempio pratico:

Convertire una chiave Cyfral in DS1990A per emularla:

1. Leggi la chiave Cyfral con il Flipper.
2. Apri iButton Converter.
3. Seleziona "Cyfral → Dallas ID".
4. Salva il risultato come nuova chiave emulabile.

Quando usarlo:

- Per sistemi che richiedono formato Dallas anche se la chiave è Cyfral/Metakom.
- Per creare una copia convertita a scopo di test.

Dove usarlo:

- Citofoni ex-URSS / Est Europa.
- Installazioni condominiali con protocolli misti.

## • iButton Fuzzer (DS1990 / Metakom / Cyfral)

Strumento avanzato per testare lettori iButton generando ID casuali, sequenziali o mirati, specifici per ogni tecnologia.

Funzionalità ampliate:

- Fuzzing dedicato per:
  - DS1990 - generazione ID 1-Wire random/validi.
  - Metakom - generazione ID compatibili con protocollo proprietario.
  - Cyfral - generazione codice in formato impulso/ciclo.
- Test di robustezza dei sistemi di accesso.
- Possibilità di scoprire pattern di accettazione (legalmente, su impianti propri!).
- Modalità sequenziale, random o custom.

Esempio pratico:

Test di un lettore Metakom per verificarne la sicurezza:

1. Entra in iButton Fuzzer → Metakom.
2. Seleziona modalità -Random ID-.
3. Appoggia il Flipper al lettore.
4. Osserva quali codici vengono accettati (solo su impianti di tua proprietà!).

Quando usarlo:

- Audit di sicurezza.
- Analisi comportamento lettori.
- Test compatibilità.

Dove usarlo:

- Sistemi condominiali e commerciali.
- Installazioni industriali basate su 1-Wire custom.