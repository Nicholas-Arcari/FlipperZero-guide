## Aspetti Legali

### Normativa Italiana Applicabile

L'utilizzo di strumenti come il Flipper Zero per la lettura, clonazione e fuzzing di chiavi iButton è regolato da diverse norme italiane:

**Codice Penale:**

- **Art. 615 ter c.p. - Accesso abusivo a sistema informatico o telematico:** "Chiunque abusivamente si introduce in un sistema informatico o telematico protetto da misure di sicurezza ovvero vi si mantiene contro la volontà espressa o tacita di chi ha il diritto di escluderlo, è punito con la reclusione da uno a cinque anni."
  - Un sistema di accesso iButton è considerato un sistema protetto da misure di sicurezza, anche se deboli
  - La clonazione di una chiave altrui e l'uso per accedere a un edificio può configurare questo reato
  - La pena è aumentata se il fatto è commesso da un pubblico ufficiale o da chi esercita la professione di investigatore privato

- **Art. 615 quater c.p. - Detenzione e diffusione abusiva di codici di accesso a sistemi informatici o telematici:** "Chiunque, al fine di procurare a sè o ad altri un profitto o di arrecare ad altri un danno, abusivamente si procura, riproduce, diffonde, comunica o consegna codici, parole chiave o altri mezzi idonei all'accesso ad un sistema informatico o telematico protetto da misure di sicurezza, o comunque fornisce indicazioni o istruzioni idonee al predetto scopo, è punito con la reclusione sino a un anno e con la multa sino a euro 5.164."
  - Il ROM code di una chiave iButton è un "codice di accesso"
  - La riproduzione (clonazione) senza autorizzazione configura il reato
  - Anche la mera detenzione del codice clonato può essere problematica

- **Art. 624 c.p. - Furto:** Se la chiave viene sottratta (anche temporaneamente) per la clonazione, può configurarsi furto d'uso.

- **Art. 640 ter c.p. - Frode informatica:** Se la clonazione e l'uso del clone producono un vantaggio patrimoniale ingiusto.

**Codice della Privacy (D.Lgs. 196/2003 e GDPR):**

- I log di accesso iButton contengono dati personali (chi accede, quando)
- La raccolta di questi dati deve rispettare il GDPR
- L'intercettazione dei codici di accesso di terzi viola la privacy

**D.Lgs. 231/2001 - Responsabilità amministrativa degli enti:**

- Un'azienda che commissiona test di sicurezza deve avere un'autorizzazione formale
- Il pentester deve operare nell'ambito di un contratto che definisce scope e limiti

### Cosa Puoi Fare Legalmente

**Sempre legale:**
- Leggere e clonare le TUE chiavi personali
- Testare sistemi iButton di TUA proprietà (es. il tuo sistema domotico)
- Studiare il protocollo 1-Wire a scopo educativo/di ricerca
- Possedere un Flipper Zero (non è illegale possedere lo strumento)
- Fare backup delle tue chiavi

**Legale con autorizzazione scritta:**
- Penetration testing su sistemi di terzi (contratto di pentest)
- Audit di sicurezza condominiale (delibera assembleare + contratto)
- Test di resilienza su lettori di clienti (contratto di consulenza)

**Sempre illegale:**
- Clonare chiavi altrui senza consenso
- Usare cloni per accedere a edifici non tuoi
- Fare fuzzing su lettori senza autorizzazione del proprietario
- Intercettare codici iButton di terzi
- Vendere o distribuire codici clonati

### Raccomandazioni per il Pentester

1. **Contratto scritto SEMPRE** - prima di toccare qualsiasi sistema, avere un contratto firmato che specifica:
   - Scope dell'assessment (quali lettori, quali chiavi)
   - Periodo temporale autorizzato
   - Limiti operativi (es. "no fuzzing dopo le 22:00")
   - Responsabilità in caso di danni
   - Clausola di confidenzialità

2. **Autorizzazione specifica per il fuzzing** - il fuzzing è più aggressivo della semplice lettura/emulazione. Serve autorizzazione esplicita nel contratto.

3. **Documentazione di tutto** - registra ogni azione con timestamp, screenshot, foto. In caso di contestazione, la documentazione è la tua difesa.

4. **Non conservare codici di terzi** - dopo l'audit, cancella tutti i file `.ibtn` contenenti codici del cliente. Conserva solo hash o screenshot censurati per il report.

5. **Report anonimizzato** - nel report, non includere i ROM code completi delle chiavi. Usa versioni censurate (es. `01:XX:XX:XX:XX:XX:XX:E7`).

> **Nota personale:** Ho sempre un contratto firmato prima di iniziare qualsiasi attività su sistemi di terzi - nessuna eccezione. Per gli audit condominiali, richiedo una copia della delibera assembleare che autorizza l'assessment, oltre al contratto con l'amministratore. Per il fuzzing, inserisco sempre una clausola specifica nel contratto che lo menziona esplicitamente. La burocrazia è noiosa ma ti salva la vita - un condomino spaventato che ti vede armeggiare col citofono e chiama la polizia non è una situazione in cui vuoi trovarti senza documentazione.

---

