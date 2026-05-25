## Aspetti Legali

### Normativa Italiana

L'uso di dispositivi come il Flipper Zero per la lettura e clonazione di badge RFID è regolato da diverse normative:

**Codice Penale:**

- **Art. 615-ter** - Accesso abusivo a sistema informatico o telematico: la clonazione di un badge per accedere a un luogo protetto configura accesso abusivo. Pena: reclusione da 1 a 5 anni.

- **Art. 615-quater** - Detenzione e diffusione abusiva di codici di accesso: la detenzione di badge clonati senza autorizzazione può configurare questo reato. Pena: reclusione fino a 1 anno e multa.

- **Art. 617-quater** - Intercettazione, impedimento o interruzione illecita di comunicazioni informatiche: lo sniffing non autorizzato di comunicazioni RFID potrebbe rientrare in questa fattispecie.

- **Art. 640-ter** - Frode informatica: l'uso di badge clonati per ottenere un vantaggio (es. accesso a servizi) configura frode informatica. Pena: reclusione da 6 mesi a 3 anni e multa.

**Normativa EU:**

- **GDPR (Reg. UE 2016/679):** gli ID dei badge sono dati personali se associabili a persone fisiche. La lettura non autorizzata viola il GDPR.

- **Direttiva NIS2 (EU 2022/2555):** le infrastrutture critiche devono proteggere anche gli accessi fisici. Un pentest su questi sistemi richiede autorizzazione formale.

- **Regolamento RED (EU 2014/53):** i dispositivi radio (come il Flipper Zero) devono essere conformi alla normativa EU sulle apparecchiature radio. Il Flipper Zero è conforme (certificazione CE) ma l'uso improprio rimane illegale.

### Come Operare Legalmente

1. **Autorizzazione scritta SEMPRE:** prima di qualsiasi test, ottieni un contratto firmato che specifichi:
   - Scope del test (quali lettori, quali edifici, quali badge)
   - Periodo di validità
   - Azioni autorizzate (lettura, clonazione, fuzzing, tentativo di accesso)
   - Contatti di emergenza
   - Clausola di manleva

2. **Porta sempre con te:**
   - Copia del contratto
   - Documento di identità
   - Numero di telefono del referente aziendale
   - Badge "legittimo" fornito dal cliente per il rientro

3. **Limiti da rispettare:**
   - Non leggere badge di persone non coinvolte nel test
   - Non accedere ad aree fuori scope
   - Non conservare i dati oltre il periodo necessario
   - Distruggi i T5577 clonati alla fine dell'engagement
   - Non condividere gli ID letti con terzi

4. **Documentazione:**
   - Log dettagliato di ogni azione (ora, luogo, ID letto/usato, risultato)
   - Foto/video con timestamp
   - Report finale con finding, rischio e raccomandazioni
   - Consegna sicura del report al cliente

> **Nota personale:** Ho sempre in borsa un "kit legale" separato dal kit tecnico: copia del contratto, lettera di autorizzazione su carta intestata del cliente, e il numero del mio avvocato. In 8 anni di pentesting fisico non ho mai avuto problemi legali, ma una volta la guardia di un condominio ha chiamato la polizia vedendomi armeggiare con il Flipper vicino al lettore del cancello. Avere l'autorizzazione scritta del cliente ha risolto tutto in 10 minuti. Senza quel foglio, sarei stato nei guai. MAI operare senza autorizzazione scritta, nemmeno su sistemi che "tanto sono insicuri".

---

